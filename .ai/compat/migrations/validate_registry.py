#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "AGENTS.md").is_file():
            return p
    return here.parents[4]


ROOT = _repo_root()


def load_json(path: Path):
    return json.loads(path.read_text())


def assert_no_dupes(items, label):
    ids = [x["id"] for x in items]
    dupes = [k for k, v in Counter(ids).items() if v > 1]
    if dupes:
        raise ValueError(f"{label} duplicate IDs: {dupes}")


def assert_paths_exist(items, label):
    missing = []
    for item in items:
        path = ROOT / item["path"]
        if not path.exists():
            missing.append(str(path))
    if missing:
        raise ValueError(f"{label} missing paths: {missing}")


def main():
    agents = load_json(ROOT / ".ai/registry/agents.registry.json")["agents"]
    subagents = load_json(ROOT / ".ai/registry/subagents.registry.json")["subagents"]
    skills = load_json(ROOT / ".ai/registry/skills.registry.json")["skills"]
    bindings = load_json(ROOT / ".ai/registry/command_bindings.registry.json")["bindings"]

    assert_no_dupes(agents, "agents")
    assert_no_dupes(subagents, "subagents")
    assert_no_dupes(skills, "skills")
    assert_no_dupes(bindings, "bindings")

    assert_paths_exist(agents, "agents")
    assert_paths_exist(subagents, "subagents")
    assert_paths_exist(skills, "skills")

    agent_ids = {a["id"] for a in agents}
    subagent_ids = {s["id"] for s in subagents}
    skill_ids = {s["id"] for s in skills}

    for binding in bindings:
        if binding["primary_agent"] not in agent_ids:
            raise ValueError(f"binding {binding['id']} references unknown agent {binding['primary_agent']}")
        missing_subagents = [s for s in binding["subagent_pipeline"] if s not in subagent_ids]
        if missing_subagents:
            raise ValueError(f"binding {binding['id']} missing subagents {missing_subagents}")
        missing_skills = [s for s in binding["skill_refs"] if s not in skill_ids]
        if missing_skills:
            raise ValueError(f"binding {binding['id']} missing skills {missing_skills}")

    print("registry_validation_ok")
    print(f"agents={len(agents)} subagents={len(subagents)} skills={len(skills)} bindings={len(bindings)}")


if __name__ == "__main__":
    main()
