# Industrial OS shards (`factory/shards/`)

Copy source trees for **`/mat`** / **`bash .ai/scripts/factory_materialize.sh`**. Expected top-level folders include **`CORE_OS_SAAS`**, **`WEB_OS_TITAN`**, **`MOBILE_OS_FORGE`**, **`MENA_OS_BILINGUAL`**, **`ASSET_OS_LAB`**, **`BRAND_OS_STRATEGY`** (six OMEGA-style templates).

## Local bodies (gitignored)

Large template bodies live here in your working copy only (see root **`.gitignore`**: `factory/shards/*` with **`!factory/shards/.gitkeep`**).

## If this folder is empty

Shard trees are **not** restored from Git when missing. Re-copy them from a backup, another clone, or your distribution pipeline, then run **`/mat`** again.
