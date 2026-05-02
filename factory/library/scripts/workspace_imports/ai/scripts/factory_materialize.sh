#!/bin/bash
# .ai/scripts/factory_materialize.sh
# Industrial Materialization Engine: Spawns new workspaces from OMEGA templates.

FACTORY_ROOT="/Users/Dorgham/Documents/Work/Devleopment/AIWF"
TEMPLATE_DIR="$FACTORY_ROOT/workspaces/templates"
CLIENTS_DIR="$FACTORY_ROOT/workspaces/clients"
PERSONAL_DIR="$FACTORY_ROOT/workspaces/personal"

echo "🪐 AIWF INDUSTRIAL MATERIALIZATION ENGINE"
echo "----------------------------------------"

# 1. Choose Template
echo "📋 Available Industrial OS Templates:"
templates=($(ls -d "$TEMPLATE_DIR"/*/))
for i in "${!templates[@]}"; do
    echo "  [$i] $(basename "${templates[$i]}")"
done

read -p "👉 Choose a template index [0-$((${#templates[@]}-1))]: " template_idx
SELECTED_TEMPLATE="${templates[$template_idx]}"

if [ -z "$SELECTED_TEMPLATE" ]; then
    echo "❌ Invalid selection. Aborting."
    exit 1
fi

# 2. Choose Target Location
echo "📂 Target Shard Layer:"
echo "  [0] Clients"
echo "  [1] Personal"
read -p "👉 Choose target layer [0-1]: " layer_idx

if [ "$layer_idx" == "0" ]; then
    TARGET_PARENT="$CLIENTS_DIR"
else
    TARGET_PARENT="$PERSONAL_DIR"
fi

# 3. Choose Shard Name
read -p "👉 Enter new workspace name (slug): " TARGET_NAME
TARGET_PATH="$TARGET_PARENT/$TARGET_NAME"

if [ -d "$TARGET_PATH" ]; then
    echo "❌ Error: Workspace '$TARGET_NAME' already exists at $TARGET_PATH."
    exit 1
fi

# 4. Materialize Shard
echo "🚀 Materializing '$TARGET_NAME' from $(basename "$SELECTED_TEMPLATE")..."
cp -R "$SELECTED_TEMPLATE" "$TARGET_PATH"

# 5. Localize Shard (Global Path Replacement)
echo "🧬 Localizing Intelligence Fabric..."
TEMPLATE_NAME=$(basename "$SELECTED_TEMPLATE")
grep -rl "$TEMPLATE_NAME" "$TARGET_PATH" | xargs sed -i '' "s|$TEMPLATE_NAME|$TARGET_NAME|g"
grep -rl "workspaces/templates" "$TARGET_PATH" | xargs sed -i '' "s|workspaces/templates|workspaces/$(basename "$TARGET_PARENT")|g"

# 6. Final Sanitization
cd "$TARGET_PATH"
./.ai/scripts/01_core/workspace_sanitize.sh
rm -rf .git
git init && git branch -m main
git add .
git commit -m "chore: initial materialization from $(basename "$SELECTED_TEMPLATE")"

echo "----------------------------------------"
echo "✅ Materialization Complete: $TARGET_PATH"
echo "💡 Next Step: cd $TARGET_PATH && /git onboard"
EOF
