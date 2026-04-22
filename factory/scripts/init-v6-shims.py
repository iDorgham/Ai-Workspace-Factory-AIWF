import os
import json
import datetime

# AIWF v6.0.0 Initialization Script
# Prepares the filesystem and memory structures for the Antifragile Factory release.

def init_shims():
    print("🚀 Initializing AIWF v6.0.0 Shims...")
    
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ai_dir = os.path.join(root_dir, ".ai")
    memory_dir = os.path.join(ai_dir, "memory")
    logs_dir = os.path.join(ai_dir, "logs")
    
    # New v6 directory structure
    v6_dirs = [
        os.path.join(memory_dir, "skill-memory"),
        os.path.join(logs_dir, "healing-bot"),
        os.path.join(logs_dir, "chaos-testing"),
        os.path.join(root_dir, "factory", "manifests")
    ]
    
    for d in v6_dirs:
        if not os.path.exists(d):
            print(f"📁 Creating directory: {d}")
            os.makedirs(d, exist_ok=True)
        else:
            print(f"✅ Directory exists: {d}")

    # Initialize skill-memory index
    skill_index_path = os.path.join(memory_dir, "skill-memory", "manifest-index.json")
    if not os.path.exists(skill_index_path):
        print("📝 Initializing skill-memory index...")
        initial_index = {
            "version": "1.0.0",
            "last_updated": datetime.datetime.utcnow().isoformat(),
            "manifests": []
        }
        with open(skill_index_path, 'w') as f:
            json.dump(initial_index, f, indent=2)

    # Update factory-config.json
    config_path = os.path.join(root_dir, "factory", "registry", "factory-config.json")
    if os.path.exists(config_path):
        print("⚙️ Updating factory-config.json to v6.0.0 schema...")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        config["version"] = "6.0.0-alpha"
        config["antifragile"] = {
            "healing_enabled": True,
            "recursive_learning_enabled": True,
            "swarm_routing": "v3"
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    print("✅ AIWF v6.0.0 Shims initialized successfully!")

if __name__ == "__main__":
    init_shims()
