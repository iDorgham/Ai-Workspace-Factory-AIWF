#!/bin/bash
# .ai/scripts/factory_materialize.sh
# Industrial Materialization Engine: Spawns new workspaces from OMEGA templates.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Repo root: walk up until factory/ + workspaces/ exist (AIWF layout).
FACTORY_ROOT="$SCRIPT_DIR"
while [[ "$FACTORY_ROOT" != "/" ]]; do
    if [[ -d "$FACTORY_ROOT/factory" ]] && [[ -d "$FACTORY_ROOT/workspaces" ]]; then
        break
    fi
    FACTORY_ROOT="$(cd "$FACTORY_ROOT/.." && pwd)"
done
CANON_TEMPLATES="$FACTORY_ROOT/factory/shards"
if [[ ! -d "$CANON_TEMPLATES" ]] || [[ -z "$(find "$CANON_TEMPLATES" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | head -1)" ]]; then
    echo "❌ No industrial OS template directories under:"
    echo "   $CANON_TEMPLATES"
    echo "   Add trees such as CORE_OS_SAAS, WEB_OS_TITAN, … — see factory/shards/README.md"
    exit 1
fi
TEMPLATE_DIR="$CANON_TEMPLATES"
CLIENTS_DIR="$FACTORY_ROOT/workspaces/clients"
PERSONAL_DIR="$FACTORY_ROOT/workspaces/personal"

tolower() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]'; }

echo "🪐 AIWF INDUSTRIAL MATERIALIZATION ENGINE"
echo "----------------------------------------"

# --- Build template list (sorted for stable indices) ---
if [[ ! -d "$TEMPLATE_DIR" ]]; then
    echo "❌ Missing template directory: $TEMPLATE_DIR"
    exit 1
fi

templates=()
while IFS= read -r d; do
    [[ -n "$d" ]] && templates+=("$d")
done < <(find "$TEMPLATE_DIR" -mindepth 1 -maxdepth 1 -type d | LC_ALL=C sort)
if [[ "${#templates[@]}" -eq 0 ]]; then
    echo "❌ No templates under $TEMPLATE_DIR"
    exit 1
fi

echo "📋 Templates — enter index number or template folder name (e.g. CORE_OS_SAAS, saas):"
for i in "${!templates[@]}"; do
    echo "  [$i] $(basename "${templates[$i]}")"
done
echo ""

read -r -p "👉 Template (index or name): " template_raw
template_raw="${template_raw#"${template_raw%%[![:space:]]*}"}"
template_raw="${template_raw%"${template_raw##*[![:space:]]}"}"

SELECTED_TEMPLATE=""
if [[ "$template_raw" =~ ^[0-9]+$ ]]; then
    if (( template_raw >= 0 && template_raw < ${#templates[@]} )); then
        SELECTED_TEMPLATE="${templates[$template_raw]}"
    else
        echo "❌ Index out of range. Use 0-$((${#templates[@]} - 1)) or a template name."
        exit 1
    fi
else
    if [[ -z "${template_raw// }" ]]; then
        echo "❌ Template choice cannot be empty."
        exit 1
    fi
    q="$(tolower "$template_raw")"
    exact=""
    partial=()
    for t in "${templates[@]}"; do
        b="$(basename "$t")"
        bq="$(tolower "$b")"
        if [[ "$bq" == "$q" ]]; then
            exact="$t"
            break
        fi
    done
    if [[ -n "$exact" ]]; then
        SELECTED_TEMPLATE="$exact"
    else
        for t in "${templates[@]}"; do
            b="$(basename "$t")"
            bq="$(tolower "$b")"
            if [[ "$bq" == *"$q"* ]]; then
                partial+=("$t")
            fi
        done
        if [[ "${#partial[@]}" -eq 1 ]]; then
            SELECTED_TEMPLATE="${partial[0]}"
        elif [[ "${#partial[@]}" -eq 0 ]]; then
            echo "❌ No template matches \"$template_raw\". Try the exact folder name or a shorter substring."
            exit 1
        else
            echo "❌ Ambiguous template \"$template_raw\" — matches:"
            for t in "${partial[@]}"; do echo "     - $(basename "$t")"; done
            echo "   Use a longer name or the numeric index."
            exit 1
        fi
    fi
fi

echo "📂 Target layer — enter 0 / 1 or name:"
echo "  [0] clients   (MENA-locked production shards)"
echo "  [1] personal  (R&D / global-public)"
echo ""

read -r -p "👉 Layer (0, 1, clients, or personal): " layer_raw
layer_raw="${layer_raw#"${layer_raw%%[![:space:]]*}"}"
layer_raw="${layer_raw%"${layer_raw##*[![:space:]]}"}"
lr="$(tolower "$layer_raw")"

TARGET_PARENT=""
case "$lr" in
    0|clients|client|mena-locked)
        TARGET_PARENT="$CLIENTS_DIR"
        ;;
    1|personal|private|rnd|rd)
        TARGET_PARENT="$PERSONAL_DIR"
        ;;
    *)
        echo "❌ Unknown layer \"$layer_raw\". Use 0 or clients, or 1 or personal."
        exit 1
        ;;
esac

read -r -p "👉 New workspace name (slug): " TARGET_NAME
if [[ -z "${TARGET_NAME// }" ]]; then
    echo "❌ Workspace name cannot be empty or whitespace-only."
    exit 1
fi
# Trim leading/trailing whitespace only
TARGET_NAME="${TARGET_NAME#"${TARGET_NAME%%[![:space:]]*}"}"
TARGET_NAME="${TARGET_NAME%"${TARGET_NAME##*[![:space:]]}"}"

TARGET_PATH="$TARGET_PARENT/$TARGET_NAME"

if [[ -d "$TARGET_PATH" ]]; then
    echo "❌ Workspace '$TARGET_NAME' already exists at $TARGET_PATH."
    exit 1
fi

echo "🚀 Materializing '$TARGET_NAME' from $(basename "$SELECTED_TEMPLATE") → $(basename "$TARGET_PARENT")/ ..."
cp -R "$SELECTED_TEMPLATE" "$TARGET_PATH"

echo "🧬 Localizing intelligence fabric..."
TEMPLATE_NAME=$(basename "$SELECTED_TEMPLATE")
grep -rl "$TEMPLATE_NAME" "$TARGET_PATH" | xargs sed -i '' "s|$TEMPLATE_NAME|$TARGET_NAME|g" 2>/dev/null || true
# Intentionally do not rewrite factory/shards, workspaces/templates, or legacy
# factory/workspace_templates/os_shards to workspaces/<layer>: from inside
# workspaces/{clients,personal}/<slug>/ those targets are wrong and nested files
# would need depth-specific ../../... paths anyway. Keep canonical repo-root paths
# in copied docs; authors may add relative links where needed.

cd "$TARGET_PATH"
if [[ -x ./.ai/scripts/01_core/workspace_sanitize.sh ]]; then
    ./.ai/scripts/01_core/workspace_sanitize.sh
else
    echo "⚠️  Skipping sanitize: ./.ai/scripts/01_core/workspace_sanitize.sh not found or not executable."
fi
rm -rf .git
git init && git branch -m main
git add .
git commit -m "chore: initial materialization from $(basename "$SELECTED_TEMPLATE")"

echo "----------------------------------------"
echo "✅ Materialization complete: $TARGET_PATH"
echo "💡 Next: cd $TARGET_PATH && use shard onboarding (e.g. /git onboard if defined there)."
