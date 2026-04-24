import os
import re
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class LibraryUtils:
    """Shared utilities for Sovereign Factory Library management."""
    
    def __init__(self, repo_root: Optional[str] = None):
        self.root = Path(repo_root) if repo_root else Path.cwd()
        self.library_path = self.root / "factory" / "library"
        self.taxonomy_path = self.library_path / "_taxonomy.json"
        self._taxonomy = None

    @property
    def taxonomy(self) -> Dict[str, Any]:
        """Loads and caches the taxonomy JSON."""
        if self._taxonomy is None:
            if self.taxonomy_path.exists():
                with open(self.taxonomy_path, 'r') as f:
                    self._taxonomy = json.load(f)
            else:
                self._taxonomy = {}
        return self._taxonomy

    def get_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """Extracts YAML frontmatter from a markdown file using regex/string parsing."""
        if not file_path.exists():
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return {}
            
        yaml_text = match.group(1)
        data = {}
        # Simple line-by-line parser for standard key: value or key: [list]
        for line in yaml_text.split('\n'):
            if ':' not in line: continue
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            
            if val.startswith('[') and val.endswith(']'):
                # Handle simple lists
                items = [i.strip().strip("'").strip('"') for i in val[1:-1].split(',')]
                data[key] = items
            else:
                # Handle simple strings/bools/numbers
                data[key] = val.strip("'").strip('"')
        return data

    def set_frontmatter(self, file_path: Path, metadata: Dict[str, Any]):
        """Updates or sets YAML frontmatter using string formatting."""
        if not file_path.exists():
            return
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Build YAML-like string
        lines = []
        for k, v in metadata.items():
            if isinstance(v, list):
                val_str = "[" + ", ".join(v) + "]"
                lines.append(f"{k}: {val_str}")
            else:
                lines.append(f"{k}: {v}")
        
        new_frontmatter = "---\n" + "\n".join(lines) + "\n---\n"
        
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            new_content = content[:match.start()] + new_frontmatter + content[match.end():]
        else:
            new_content = new_frontmatter + "\n" + content
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    def resolve_path_to_tags(self, file_path: Path) -> Dict[str, str]:
        """Maps a file path to its taxonomy tags (cluster, field/category)."""
        try:
            rel_path = file_path.relative_to(self.library_path)
        except ValueError:
            return {}
            
        parts = rel_path.parts
        
        # Standard structure: [cluster]/[field]/[type]/[slug]/...
        # Example: 01-software-engineering/backend/skills/...
        if len(parts) < 2:
            return {}
            
        meta = {
            "cluster": parts[0],
            "category": parts[1],
            "field": parts[1]
        }
        return meta

    def get_pretty_name(self, cluster_id: str, field_slug: str) -> str:
        """Looks up the pretty name (including icon) from the enterprise taxonomy."""
        clusters = self.taxonomy.get("clusters", {})
        cluster = clusters.get(cluster_id, {})
        fields = cluster.get("fields", {})
        
        # If field is a dict (V3+ taxonomy), look up the value
        if isinstance(fields, dict):
            return fields.get(field_slug, field_slug.replace('-', ' ').title())
            
        # Fallback for old taxonomy
        return field_slug.replace('-', ' ').title()
