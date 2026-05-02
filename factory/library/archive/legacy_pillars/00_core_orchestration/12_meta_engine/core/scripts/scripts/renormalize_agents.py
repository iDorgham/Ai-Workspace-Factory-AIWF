import os
import shutil
from pathlib import Path

TARGET_DIR = Path("/Users/Dorgham/Documents/Work/Devleopment/Sovereign/Sovereign Workspace Factory/factory/library")

def to_pascal_case(name):
    # Special cases for acronyms
    acronyms = {"qa": "QA", "dba": "DBA", "seo": "SEO", "ai": "AI", "mena": "MENA", "roi": "ROI", "gafi": "GAFI"}
    if name.lower() in acronyms:
        return acronyms[name.lower()]
    
    # Standard PascalCase
    parts = name.replace('-', ' ').replace('_', ' ').split()
    return "".join(p.capitalize() for p in parts)

def main():
    renamed_count = 0
    for r, d, f in os.walk(TARGET_DIR):
        if "agents" in Path(r).parts:
            for dirname in d:
                old_path = Path(r) / dirname
                new_name = to_pascal_case(dirname)
                new_path = Path(r) / new_name
                
                if old_path != new_path:
                    # Check if destination exists (e.g., if we are renaming 'qa' to 'QA')
                    if new_path.exists() and old_path.name.lower() == new_path.name.lower():
                        # Temp rename to avoid conflict on case-insensitive systems
                        temp_path = Path(r) / (dirname + "_temp")
                        os.rename(old_path, temp_path)
                        os.rename(temp_path, new_path)
                    else:
                        os.rename(old_path, new_path)
                    
                    print(f"Renamed: {dirname} -> {new_name}")
                    renamed_count += 1

    print(f"\nTotal agents renamed: {renamed_count}")

if __name__ == "__main__":
    main()
