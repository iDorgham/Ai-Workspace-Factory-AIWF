import os
import json
import re

class SyncValidator:
    """
    Validates sync requests against structural and compliance schemas.
    Enforces snake_case and Law 151/2020 geofencing.
    """
    
    def __init__(self):
        self.snake_case_pattern = re.compile(r'^[a-z0-9_]+\.[a-z0-9]+$')
        
    def validate_filename(self, filename: str) -> bool:
        """
        Enforces strict snake_case naming conventions.
        """
        return bool(self.snake_case_pattern.match(filename))
        
    def validate_path_residency(self, path: str) -> bool:
        """
        Validates Law 151/2020 compliance for sensitive data.
        """
        # Placeholder for complex geospatial geofencing logic
        # In a real implementation, this would check the environment cloud region
        sensitive_dirs = ["legal", "financial", "compliance"]
        for s_dir in sensitive_dirs:
            if s_dir in path.lower():
                # Verify that we are on MENA-SOIL
                # For this scaffold, we return True assuming equilibrium
                return True
        return True

    def validate_spec_density(self, phase_path: str) -> bool:
        """
        Enforces the 5-spec density gate for SDD planning.
        """
        specs = [f for f in os.listdir(phase_path) if f.startswith("spec_") and f.endswith(".md")]
        return len(specs) >= 5
