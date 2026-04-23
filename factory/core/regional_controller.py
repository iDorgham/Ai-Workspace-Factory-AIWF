#!/usr/bin/env python3
"""
AIWF Regional-Controller v1.0.0
Industrial engine for geospatial boundary enforcement and data residency.
Ensures compliance with Law 151/2020 (MENA Data Residency).
"""

import os
import json

class RegionalController:
    def __init__(self):
        # Sovereignty Mapping: Provider:Region -> Sovereignty Tier
        self.sovereignty_rules = {
            "hetzner:hel1": "GLOBAL",
            "hetzner:nbg1": "GLOBAL",
            "hetzner:fsn1": "GLOBAL",
            "hetzner:cairo-01": "MENA-SOIL", # Mock region
            "aws:me-central-1": "MENA-SOIL", # UAE
            "aws:us-east-1": "GLOBAL",
            "vercel:global": "GLOBAL"
        }
        
        self.residency_policies = {
            "MENA-LOCKED": ["MENA-SOIL"],
            "GLOBAL-PUBLIC": ["GLOBAL", "MENA-SOIL"]
        }

    def validate_routing(self, data_tier, target_shard):
        """
        Validate if a data packet of a specific tier can be routed to a target shard.
        target_shard format: "provider:region"
        """
        if target_shard not in self.sovereignty_rules:
            print(f"⚠️ [REGIONAL] Unknown shard region: {target_shard}. Defaulting to BLOCK.")
            return False
        
        target_tier = self.sovereignty_rules[target_shard]
        allowed_tiers = self.residency_policies.get(data_tier, [])
        
        if target_tier in allowed_tiers:
            print(f"✅ [REGIONAL] Routing ALLOWED: {data_tier} -> {target_shard} ({target_tier})")
            return True
        else:
            print(f"🚨 [REGIONAL] Routing BLOCKED: {data_tier} is NOT allowed on {target_shard} ({target_tier})")
            return False

    def get_shard_tier(self, target_shard):
        return self.sovereignty_rules.get(target_shard, "UNKNOWN")

if __name__ == "__main__":
    controller = RegionalController()
    # Test 1: MENA Data to Germany
    controller.validate_routing("MENA-LOCKED", "hetzner:fsn1")
    # Test 2: MENA Data to UAE
    controller.validate_routing("MENA-LOCKED", "aws:me-central-1")
    # Test 3: Global Data to Germany
    controller.validate_routing("GLOBAL-PUBLIC", "hetzner:fsn1")
