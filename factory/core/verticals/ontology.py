from typing import Dict

class UniversalOntology:
    """
    Code-level mapping for the Universal Industrial Ontology.
    Ensures cross-sector terminology normalization.
    """
    
    def __init__(self):
        self.mappings = {
            "hospitality": {
                "guest_id": "global_user_id",
                "room_number": "resource_shard_id"
            },
            "legal": {
                "case_file": "legal_shard_id",
                "counsel_id": "authorized_agent_id"
            },
            "finance": {
                "invoice": "financial_transaction_id",
                "merchant_id": "node_identity"
            }
        }

    def translate_to_uif(self, sector: str, data: Dict) -> Dict:
        """
        Translates sector-specific keys into Universal Industrial Format (UIF).
        """
        sector_map = self.mappings.get(sector.lower(), {})
        uif_data = {}
        for key, value in data.items():
            uif_key = sector_map.get(key, key)
            uif_data[uif_key] = value
        return uif_data
