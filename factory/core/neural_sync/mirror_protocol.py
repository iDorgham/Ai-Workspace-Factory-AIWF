import os
import shutil
from typing import List

class OutboundMirrorProtocol:
    """
    Implementation of the Outbound Mirror Protocol (v2.0).
    Enforces active-set priority and bidirectional reconciliation.
    """
    
    def __init__(self):
        self.exclusions = [".DS_Store", "scratch", "tmp", "node_modules", ".git"]
        
    def execute_mirror(self, source: str, target: str) -> bool:
        """
        Executes the physical mirroring of files from source to target.
        """
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source path {source} does not exist.")
            
        if not os.path.exists(target):
            os.makedirs(target, exist_ok=True)
            
        for item in os.listdir(source):
            if item in self.exclusions:
                continue
                
            s = os.path.join(source, item)
            d = os.path.join(target, item)
            
            if os.path.isdir(s):
                self.execute_mirror(s, d)
            else:
                shutil.copy2(s, d)
                
        return True

    def resolve_conflict(self, active_file: str, archive_file: str) -> str:
        """
        Resolves sync conflicts using Active-Set Priority.
        """
        return active_file
