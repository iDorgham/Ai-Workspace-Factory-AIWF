#!/usr/bin/env python3
"""
AIWF Cloud-Gateway v1.0.0
Industrial routing layer for Multi-Cloud shard management.
Orchestrates deployment and synchronization across heterogeneous cloud providers.
"""

import os
import json
import sys
from datetime import datetime

# Add the factory root to the Python path to allow imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from factory.core.galaxy_sync import GalaxySync
from factory.core.regional_controller import RegionalController


class CloudGateway:
    def __init__(self, factory_root):
        self.factory_root = factory_root
        self.secrets_path = os.path.join(factory_root, ".ai/secrets/cloud_keys.json")
        self.providers = ["aws", "hetzner", "vercel", "digitalocean"]
        self.active_shards = []
        self.sync_engine = GalaxySync(factory_root)
        self.regional_engine = RegionalController()

    def _load_keys(self):
        """Securely load cloud credentials (placeholder for Galaxy-Secret-Manager)."""
        if not os.path.exists(self.secrets_path):
            return {}
        with open(self.secrets_path, "r") as f:
            return json.load(f)

    def provision_shard(self, provider, region, shard_name):
        """Provision a new industrial shard on a specific cloud provider."""
        if provider not in self.providers:
            print(f"❌ [GATEWAY] Unsupported provider: {provider}")
            return False

        print(
            f"🛰️  [GATEWAY] Provisioning {shard_name} on {provider.upper()} ({region})..."
        )

        # 1. Resolve Provider Adapter
        # 2. Trigger Cloud API (Terraform/SDK)
        # 3. Inject AIWF Shard DNA

        shard_metadata = {
            "shard_id": f"CLOUD-{provider[:3]}-{shard_name.lower()}",
            "provider": provider,
            "region": region,
            "status": "PROVISIONING",
            "last_heartbeat": datetime.now().isoformat(),
        }

        self.active_shards.append(shard_metadata)
        print(
            f"✅ [GATEWAY] Shard {shard_name} manifest created. Waiting for Shadow-Runner handshake."
        )
        return shard_metadata

    def sync_global_registry(self):
        """Broadcast the local command-system.yaml to all active cloud shards."""
        return self.sync_engine.broadcast_registry_update(self.active_shards)

    def validate_data_routing(
        self, data_classification, target_provider, target_region
    ):
        """
        Validate if data with a specific classification can be routed to a target cloud region.
        Implements Law 151/2020 MENA data residency requirements.

        Args:
            data_classification: "MENA-SENSITIVE" or "GLOBAL-PUBLIC"
            target_provider: Cloud provider (aws, hetzner, vercel, digitalocean)
            target_region: Target region identifier

        Returns:
            bool: True if routing is allowed, False if blocked
        """
        target_shard = f"{target_provider}:{target_region}"

        # Use the RegionalController to validate routing
        if data_classification == "MENA-SENSITIVE":
            data_tier = "MENA-LOCKED"
        elif data_classification == "GLOBAL-PUBLIC":
            data_tier = "GLOBAL-PUBLIC"
        else:
            print(
                f"⚠️ [GATEWAY] Unknown data classification: {data_classification}. Defaulting to BLOCK."
            )
            return False

        # Delegate to RegionalController for routing decision
        return self.regional_engine.validate_routing(data_tier, target_shard)

    def route_data_packet(self, data_packet, target_provider, target_region):
        """
        Route a data packet to the target region after validating compliance.

        Args:
            data_packet: Dict containing data metadata including classification
            target_provider: Target cloud provider
            target_region: Target cloud region

        Returns:
            dict: Routing result with status and details
        """
        # Extract data classification from packet
        classification = data_packet.get("classification", "GLOBAL-PUBLIC")
        data_id = data_packet.get("id", "unknown")

        # Validate routing compliance
        is_allowed = self.validate_data_routing(
            classification, target_provider, target_region
        )

        target_shard = f"{target_provider}:{target_region}"

        if is_allowed:
            print(f"✅ [GATEWAY] Data packet {data_id} routed to {target_shard}")
            return {
                "status": "ALLOWED",
                "data_id": data_id,
                "destination": target_shard,
                "classification": classification,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            print(
                f"🚨 [GATEWAY] Data packet {data_id} BLOCKED from routing to {target_shard}"
            )
            return {
                "status": "BLOCKED",
                "data_id": data_id,
                "destination": target_shard,
                "classification": classification,
                "timestamp": datetime.now().isoformat(),
                "reason": "Law 151/2020 MENA data residency violation",
            }


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    gateway = CloudGateway(root)
    # gateway.provision_shard("hetzner", "cairo-01", "MENA-PROD-01")

    # Test the new MENA routing logic
    print("\n🧪 Testing MENA Data Routing Logic:")

    # Test 1: MENA-sensitive data to UAE (should be ALLOWED)
    mena_packet = {"id": "MENA-USER-001", "classification": "MENA-SENSITIVE"}
    result1 = gateway.route_data_packet(mena_packet, "aws", "me-central-1")

    # Test 2: MENA-sensitive data to Germany (should be BLOCKED)
    result2 = gateway.route_data_packet(mena_packet, "hetzner", "fsn1")

    # Test 3: Global data to Germany (should be ALLOWED)
    global_packet = {"id": "GLOBAL-DATA-001", "classification": "GLOBAL-PUBLIC"}
    result3 = gateway.route_data_packet(global_packet, "hetzner", "fsn1")
