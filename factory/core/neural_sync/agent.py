import os
import time
import hashlib
import logging
from typing import List, Dict, Optional
from .mirror_protocol import OutboundMirrorProtocol
from .validator import SyncValidator

class NeuralSyncAgent:
    """
    Main T1 Agent for bidirectional, event-driven synchronization.
    Enforces the Outbound Mirror Protocol across sovereign shards.
    """
    
    def __init__(self, governor: str = "Dorgham"):
        self.governor = governor
        self.version = "20.0.0"
        self.protocol = OutboundMirrorProtocol()
        self.validator = SyncValidator()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        logger = logging.getLogger("NeuralSyncAgent")
        logger.setLevel(logging.INFO)
        # Industrial log path within the workspace
        log_path = os.path.join(os.getcwd(), "factory/logs/neural_sync.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def sync_shard(self, source_path: str, target_path: str, mode: str = "outbound"):
        """
        Synchronizes a specific shard between source and target.
        """
        self.logger.info(f"Initiating {mode} sync: {source_path} -> {target_path}")
        
        # 1. Validation Phase
        if not self.validator.validate_path_residency(source_path):
            self.logger.error(f"Residency Violation: {source_path} is non-compliant with Law 151/2020.")
            return False
            
        # 2. Execution Phase
        try:
            result = self.protocol.execute_mirror(source_path, target_path)
            if result:
                self.logger.info(f"Sync Successful: {source_path} equilibrium achieved.")
                return True
        except Exception as e:
            self.logger.error(f"Sync Failed: {str(e)}")
            return False

    def watch_active_set(self, active_path: str = ".ai/"):
        """
        Enables real-time neural propagation for the active-set.
        """
        self.logger.info(f"Neural Watchdog initialized on {active_path}")
        # Implementation for inotify / fsevents would go here
        pass

    def get_evolution_hash(self, file_path: str) -> str:
        """
        Generates SHA-256 Reasoning Hash for a synchronized asset.
        """
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return f"sha256:{hasher.hexdigest()}"

if __name__ == "__main__":
    agent = NeuralSyncAgent()
    print(f"NeuralSyncAgent v{agent.version} initialized by {agent.governor}.")
