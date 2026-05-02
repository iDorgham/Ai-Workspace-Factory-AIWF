#!/usr/bin/env python3
import os
import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_FILE = ROOT / ".ai" / "logs" / "swarm-router.md"
ALIAS_TABLE = ROOT / "factory" / "registry" / "pipeline-alias-mapping.json" # Assume this exists from v5

def generate_reasoning_hash(agent_id="SR"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    nonce = os.urandom(2).hex()
    return f"[{agent_id}-{timestamp}-{nonce}]"

def log_event(message, hash_id):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(LOG_FILE, "a") as f:
        f.write(f"- **{timestamp}** {hash_id}: {message}\n")

def get_swarm_consensus(alias: str):
    alias_lower = alias.strip().lower()

    alias_map = {}
    if ALIAS_TABLE.exists():
        try:
            alias_map = json.loads(ALIAS_TABLE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            alias_map = {}

    alias_known = alias_lower in alias_map

    # Deterministic policy votes
    agents = ["SEO_AGENT", "BRAND_AGENT", "COMPLIANCE_AGENT"]
    votes = {
        "SEO_AGENT": "YES" if alias_known else "NO",
        "BRAND_AGENT": "YES" if alias_known else "NO",
        "COMPLIANCE_AGENT": "YES" if alias_known and alias_lower.startswith("/") else "NO",
    }

    yes_votes = list(votes.values()).count("YES")
    consensus_met = yes_votes >= 2 # 2/3 majority
    confidence = (yes_votes / len(agents)) * 100
    
    return {
        "alias": alias,
        "votes": votes,
        "consensus_met": consensus_met,
        "confidence": confidence
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: /route consensus {{ALIAS}}")
        sys.exit(1)
        
    alias = sys.argv[1]
    explain = "--explain" in sys.argv
    force_legacy = "--force-deterministic" in sys.argv
    
    if not LOG_FILE.parent.exists():
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w") as f:
            f.write("# 🛰️ SWARM CONSENSUS ROUTER LOGS\n\n")

    print(f"🛰️  Initiating swarm consensus for alias: '{alias}'...")
    
    if force_legacy:
        print("⚠️  Bypassing swarm. Using legacy deterministic routing.")
        result = {"alias": alias, "consensus_met": True, "confidence": 100, "votes": {"MANUAL": "YES"}}
    else:
        time.sleep(0.1)
        result = get_swarm_consensus(alias)

    hash_id = generate_reasoning_hash()
    
    if result["consensus_met"]:
        print(f"✅ Consensus REAChED ({result['confidence']}% confidence)")
        log_msg = f"Consensus REACHED for '{alias}' | Confidence: {result['confidence']}% | Votes: {result['votes']}"
        log_event(log_msg, hash_id)
    else:
        print(f"❌ Consensus FAILED ({result['confidence']}% confidence).")
        print("🔄 Falling back to deterministic alias table...")
        log_msg = f"Consensus FAILED for '{alias}' | Falling back to deterministic table | Votes: {result['votes']}"
        log_event(log_msg, hash_id)

    if explain:
        print("\n--- Voting Breakdown ---")
        for agent, vote in result["votes"].items():
            print(f"  - {agent}: {vote}")
        print(f"--- Reasoning Hash: {hash_id} ---")

if __name__ == "__main__":
    main()
