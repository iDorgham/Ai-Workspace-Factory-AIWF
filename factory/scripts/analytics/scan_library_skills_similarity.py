#!/usr/bin/env python3
"""
Scan factory/library/skills for likely duplicate / overlapping skill bundles.

Heuristics (name + token overlap + fuzzy slug); does not embed SKILL.md bodies.
Outputs JSON (--json) or a short Markdown report (--md-out PATH).

Usage:
  python3 factory/scripts/analytics/scan_library_skills_similarity.py
  python3 factory/scripts/analytics/scan_library_skills_similarity.py --json > /tmp/skills_sim.json
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass, asdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[3] / "factory" / "library" / "skills"

STOP = frozenset(
    "a an the and or for to of in on at by with from into over under "
    "skill skills using use io sdk api cli v2 v3 pro ai ml official github "
    "import imports references scripts".split()
)


def tokens(slug: str) -> set[str]:
    parts = re.split(r"[-_/]+", slug.lower())
    return {p for p in parts if len(p) > 1 and p not in STOP}


def norm_join(slug: str) -> str:
    return "".join(re.split(r"[-_/]+", slug.lower()))


def skill_roots(base: Path) -> list[Path]:
    """Avoid rglob over huge trees: one SKILL/skill per immediate bundle folder."""
    out: list[Path] = []
    seen: set[str] = set()

    def add_folder(folder: Path) -> None:
        key = str(folder.resolve())
        if key in seen:
            return
        if (folder / "SKILL.md").is_file() or (folder / "skill.md").is_file():
            seen.add(key)
            out.append(folder)

    gi = base / "github_imports"
    if gi.is_dir():
        for child in gi.iterdir():
            if child.is_dir():
                add_folder(child)
    for child in base.iterdir():
        if not child.is_dir() or child.name == "github_imports":
            continue
        add_folder(child)
    return out


def md_path(folder: Path) -> Path | None:
    for n in ("SKILL.md", "skill.md"):
        c = folder / n
        if c.is_file():
            return c
    return None


@dataclass
class SkillInfo:
    rel: str  # relative to library/skills
    leaf: str
    md_bytes: int
    under_github_imports: bool


def collect(base: Path) -> list[SkillInfo]:
    rows: list[SkillInfo] = []
    for folder in skill_roots(base):
        md = md_path(folder)
        if not md:
            continue
        rel = str(folder.relative_to(base)).replace("\\", "/")
        leaf = folder.name
        rows.append(
            SkillInfo(
                rel=rel,
                leaf=leaf,
                md_bytes=md.stat().st_size,
                under_github_imports=rel.startswith("github_imports/"),
            )
        )
    return rows


def similarity(a: SkillInfo, b: SkillInfo) -> float:
    ta, tb = tokens(a.leaf), tokens(b.leaf)
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    jacc = inter / union if union else 0.0
    na, nb = norm_join(a.leaf), norm_join(b.leaf)
    seq = SequenceMatcher(None, na, nb).ratio()
    # Substring / containment (whole slug as token boundary)
    score = max(jacc, seq)
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    if len(shorter) >= 6 and shorter in longer:
        score = max(score, 0.82)
    return score


def cluster_union_find(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b in edges:
        union(a, b)
    groups: dict[int, set[int]] = defaultdict(set)
    for i in range(n):
        groups[find(i)].add(i)
    return [g for g in groups.values() if len(g) > 1]


def leaf_collisions(infos: list[SkillInfo]) -> dict[str, list[str]]:
    by_leaf: dict[str, list[str]] = defaultdict(list)
    for s in infos:
        by_leaf[s.leaf.lower()].append(s.rel)
    return {k: v for k, v in by_leaf.items() if len(v) > 1}


def build_candidate_pairs(
    infos: list[SkillInfo],
    min_shared_tokens: int = 2,
    max_token_freq: int = 35,
) -> Iterable[tuple[int, int, float]]:
    tok_to_idx: dict[str, set[int]] = defaultdict(set)
    for i, s in enumerate(infos):
        for t in tokens(s.leaf):
            tok_to_idx[t].add(i)
    # Drop ultra-common tokens (e.g. "official", "shopify" if hundreds of dirs share it)
    rare_tokens = {t for t, idxs in tok_to_idx.items() if len(idxs) <= max_token_freq}
    seen_pairs: set[tuple[int, int]] = set()
    for i, s in enumerate(infos):
        st = tokens(s.leaf)
        cand: set[int] = set()
        for t in st:
            if t not in rare_tokens:
                continue
            cand |= tok_to_idx[t]
        cand.discard(i)
        for j in cand:
            a, b = (i, j) if i < j else (j, i)
            if (a, b) in seen_pairs:
                continue
            shared = st & tokens(infos[j].leaf)
            shared_rare = shared & rare_tokens
            if len(shared) < min_shared_tokens and len(shared_rare) < max(1, min_shared_tokens - 1):
                continue
            sim = similarity(s, infos[j])
            if sim < 0.42:
                continue
            seen_pairs.add((a, b))
            yield a, b, sim


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md-out", type=Path, default=None)
    ap.add_argument("--min-sim", type=float, default=0.72, help="pair score floor for reporting")
    ap.add_argument(
        "--cluster-sim",
        type=float,
        default=0.0,
        help="if >0, also emit small transitive clusters using this stricter edge threshold",
    )
    ap.add_argument("--max-token-freq", type=int, default=25)
    args = ap.parse_args()

    if not ROOT.is_dir():
        raise SystemExit(f"Missing skills root: {ROOT}")

    infos = sorted(collect(ROOT), key=lambda x: x.rel)
    pairs: list[tuple[int, int, float]] = [
        (a, b, sim)
        for a, b, sim in build_candidate_pairs(
            infos, min_shared_tokens=2, max_token_freq=args.max_token_freq
        )
        if sim >= args.min_sim
    ]
    pairs.sort(key=lambda t: -t[2])
    collisions = leaf_collisions(infos)

    clusters_sorted: list[dict] = []
    if args.cluster_sim > 0:
        strong_edges = [(a, b) for a, b, sim in pairs if sim >= args.cluster_sim]
        clusters = cluster_union_find(len(infos), strong_edges)
        for group in clusters:
            if len(group) < 2 or len(group) > 12:
                continue
            members = [infos[i] for i in group]
            members.sort(key=lambda x: -x.md_bytes)
            idxs = list(group)
            sims = [
                similarity(infos[idxs[ii]], infos[idxs[jj]])
                for ii in range(len(idxs))
                for jj in range(ii + 1, len(idxs))
            ]
            avg_sim = sum(sims) / len(sims) if sims else 0.0
            winner = members[0]
            clusters_sorted.append(
                {
                    "size": len(members),
                    "avg_pairwise_sim": round(avg_sim, 3),
                    "keep_recommendation": {
                        "rel": winner.rel,
                        "md_bytes": winner.md_bytes,
                        "reason": "largest SKILL.md/skill.md in cluster",
                    },
                    "members": [asdict(m) for m in members],
                }
            )
        clusters_sorted.sort(key=lambda x: (-x["size"], -x["avg_pairwise_sim"]))

    pair_rows = []
    seen: set[tuple[int, int]] = set()
    for a, b, sim in pairs[:200]:
        key = (a, b) if a < b else (b, a)
        if key in seen:
            continue
        seen.add(key)
        ia, ib = infos[a], infos[b]
        pair_rows.append(
            {
                "similarity": round(sim, 3),
                "a": asdict(ia),
                "b": asdict(ib),
            }
        )
        if len(pair_rows) >= 80:
            break

    payload = {
        "skills_root": str(ROOT),
        "total_skill_roots": len(infos),
        "leaf_name_collisions": collisions,
        "top_pairs": pair_rows,
        "tight_clusters": clusters_sorted,
        "notes": [
            "Pair list avoids bogus mega-clusters from transitive chaining.",
            "Prefer merge_key + import script for github_imports dedup; use pairs for human review.",
            "Leaf collisions are definite naming duplicates across paths.",
        ],
    }

    if args.json:
        print(json.dumps(payload, indent=2))
        return

    lines = [
        "# Library skills — similarity scan (heuristic)",
        "",
        f"- Root: `{ROOT.relative_to(ROOT.parents[3])}`",
        f"- Skill bundles: **{len(infos)}**",
        f"- High-sim pairs (≥{args.min_sim}, top 80): **{len(pair_rows)}**",
        "",
        "## Same folder name, different path (merge candidates)",
        "",
    ]
    if not collisions:
        lines.append("_None found._")
    else:
        for leaf, paths in sorted(collisions.items(), key=lambda x: -len(x[1]))[:40]:
            lines.append(f"### `{leaf}` ({len(paths)} copies)")
            for p in sorted(paths):
                lines.append(f"- `{p}`")
            lines.append("")
    lines.extend(
        [
            "",
            "## Highest-similarity pairs (review; keep larger or merge prose)",
            "",
        ]
    )
    for row in pair_rows[:50]:
        a, b, sm = row["a"], row["b"], row["similarity"]
        lines.append(f"- **{sm}** — `{a['rel']}` ({a['md_bytes']} B) ↔ `{b['rel']}` ({b['md_bytes']} B)")
    if args.cluster_sim > 0 and clusters_sorted:
        lines.extend(["", "## Tight clusters (transitive, small only)", ""])
        for c in clusters_sorted[:25]:
            w = c["keep_recommendation"]
            lines.append(
                f"- **{c['size']}** skills, avg sim {c['avg_pairwise_sim']} — keep `{w['rel']}`"
            )
            for m in c["members"]:
                lines.append(f"  - `{m['rel']}` ({m['md_bytes']} B)")

    text = "\n".join(lines)
    print(text)
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(text, encoding="utf-8")
        print(f"\nWrote: {args.md_out}", file=__import__("sys").stderr)


if __name__ == "__main__":
    main()
