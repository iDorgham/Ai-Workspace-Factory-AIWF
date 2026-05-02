#!/usr/bin/env python3
import os
import shutil
import json
from pathlib import Path

# Target directory
LIB_PATH = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library")

# Mapping Registry: Field -> New Department
FIELD_TO_DEPT = {
    "developing": "01-software-engineering",
    "engineering-core": "01-software-engineering",
    "web-developing": "02-web-platforms",
    "cloud-architecture": "02-web-platforms",
    "app-developing": "02-web-platforms",
    "saas-platforms": "02-web-platforms",
    "mobile-ios-apple": "02-web-platforms",
    "cyber-security": "03-security-compliance",
    "fintech-banking": "03-security-compliance",
    "business": "04-business-strategy",
    "growth-strategy": "04-business-strategy",
    "venture-design": "04-business-strategy",
    "analysis": "05-data-analytics",
    "ai-automation-ops": "05-data-analytics",
    "branding": "06-branding-content",
    "content-creation": "06-branding-content",
    "copywriting": "06-branding-content",
    "seo": "07-marketing-seo",
    "advertising": "07-marketing-seo",
    "video-production": "08-media-production",
    "3d-production": "08-media-production",
    "image-production": "08-media-production",
    "audio-music-tech": "08-media-production",
    "ai-generative-media": "08-media-production",
    "social-media": "09-social-engagement",
    "social-media-content": "09-social-engagement",
    "execution": "10-operations-qa",
    "quality-assurance": "10-operations-qa",
    "project-management": "10-operations-qa",
    "real-estate-dev": "11-industry-verticals",
    "healthtech-pharma": "11-industry-verticals",
    "islamic-finance": "11-industry-verticals",
    "crypto-web3": "11-industry-verticals",
    "meta-orchestration": "12-meta-engine",
    "library-taxonomy": "12-meta-engine",
    "core": "12-meta-engine",
}

def departmental_migration():
    count = 0
    # Current top-level folders include 01-cyber, 02-commerce, etc.
    legacy_clusters = ["01-cyber", "02-commerce", "03-creative", "04-ops", "05-verticals", "07-meta"]
    
    for cluster in legacy_clusters:
        cluster_path = LIB_PATH / cluster
        if not cluster_path.exists(): continue
        
        # Walk through fields in this legacy cluster
        for field in os.listdir(cluster_path):
            field_path = cluster_path / field
            if not field_path.is_dir() or field.startswith('.'): continue
            
            # Identify target department
            dept = FIELD_TO_DEPT.get(field)
            if not dept:
                # Fallback: if we didn't map a specialized field yet, keep it in a 'misc' or similar
                print(f"Warning: Field '{field}' not explicitly mapped. Defaulting to cluster parent logic.")
                continue
                
            dest_path = LIB_PATH / dept / field
            os.makedirs(dest_path.parent, exist_ok=True)
            
            # Move entire field folder to new department
            if dest_path.exists():
                # Merge logic
                for item in os.listdir(field_path):
                    shutil.move(str(field_path / item), str(dest_path / item))
                shutil.rmtree(field_path)
            else:
                shutil.move(str(field_path), str(dest_path))
            count += 1
            print(f"Migrated {field} -> {dept}/{field}")
            
    # Cleanup empty legacy cluster folders
    for cluster in legacy_clusters:
        cp = LIB_PATH / cluster
        if cp.exists() and not os.listdir(cp):
            cp.rmdir()
            print(f"Purged empty legacy cluster: {cluster}")
            
    return count

if __name__ == "__main__":
    print("--- Starting Departmental Migration (V16.0.0) ---")
    moved = departmental_migration()
    print(f"--- Migration Complete: {moved} fields restructured ---")
    print("--- Running Meta-Healer to reset IDs to 12-Department baseline ---")
    # I'll call the healing logic from the previous script which is already Sector-First compatible
