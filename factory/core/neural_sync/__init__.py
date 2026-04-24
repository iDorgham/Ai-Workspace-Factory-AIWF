"""
Neural Fabric Sync Agent - v20.0.0
Sovereign Industrial Engine for OMEGA-Tier Equilibrium.
"""

__version__ = "20.0.0"
__governor__ = "Dorgham"
__compliance__ = "Law 151/2020"

from .agent import NeuralSyncAgent
from .mirror_protocol import OutboundMirrorProtocol
from .validator import SyncValidator

__all__ = ["NeuralSyncAgent", "OutboundMirrorProtocol", "SyncValidator"]
