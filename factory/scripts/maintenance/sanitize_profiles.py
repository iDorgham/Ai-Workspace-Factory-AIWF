import os
import json

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROFILES_DIR = os.path.join(BASE_DIR, "factory/profiles")


def sanitize_profile(path):
    with open(path, "r") as f:
        content = f.read()
    
    # Check for legacy dual-object structure
    if "---" in content:
        parts = content.split("---")
        obj1 = json.loads(parts[0].strip())
        obj2 = json.loads(parts[1].strip())
        data = {**obj1, **obj2}
    else:
        try:
            data = json.loads(content)
        except Exception as e:
            print(f"❌ Corrupted JSON in {os.path.basename(path)}: {str(e)}")
            return False

    # --- INDUSTRIAL RULE: NAME IDENTITY ---
    # Ensure profile has a 'name' field for the Scaffolder and Health Scorer
    if "name" not in data and "profile_name" not in data:
        profile_id = os.path.basename(path).replace(".json", "")
        data["name"] = profile_id.replace("-", " ").title()
        data["profile_id"] = profile_id
        print(f"🆔 Injected Identity: {profile_id}")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    
    return True

if __name__ == "__main__":
    if not os.path.isdir(PROFILES_DIR):
        print("ℹ️  factory/profiles/ was retired — nothing to sanitize.")
        raise SystemExit(0)
    profiles = [f for f in os.listdir(PROFILES_DIR) if f.endswith(".json")]
    processed = 0
    for p in profiles:
        if sanitize_profile(os.path.join(PROFILES_DIR, p)):
            processed += 1
    
    print(f"\n✅ Total Industrialized: {processed} / {len(profiles)}")
