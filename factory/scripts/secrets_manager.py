#!/usr/bin/env python3
"""
AIWF Galaxy-Secret-Manager v1.0.0
Industrial vault for managing multi-cloud API keys and sovereign secrets.
Uses local encryption (placeholder) to protect credentials in the .ai/secrets/ vault.
"""

import os
import json
import base64
from cryptography.fernet import Fernet
from pathlib import Path

class GalaxySecretManager:
    def __init__(self, factory_root):
        self.root = Path(factory_root)
        self.secrets_dir = self.root / ".ai" / "secrets"
        self.key_file = self.secrets_dir / "master.key"
        self.vault_file = self.secrets_dir / "vault.json"
        
        self.secrets_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_master_key()

    def _ensure_master_key(self):
        """Provision a master encryption key if it doesn't exist."""
        if not self.key_file.exists():
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            print("🔑 [SECRETS] Master key provisioned. Keep this file safe!")

    def _get_fernet(self):
        key = self.key_file.read_bytes()
        return Fernet(key)

    def store_secret(self, provider, key_name, value):
        """Encrypt and store a cloud secret."""
        vault = self.load_vault()
        f = self._get_fernet()
        
        encrypted_value = f.encrypt(value.encode()).decode()
        
        if provider not in vault:
            vault[provider] = {}
        
        vault[provider][key_name] = encrypted_value
        self.vault_file.write_text(json.dumps(vault, indent=2))
        print(f"🔒 [SECRETS] Secret '{key_name}' stored for provider '{provider}'.")

    def get_secret(self, provider, key_name):
        """Retrieve and decrypt a cloud secret."""
        vault = self.load_vault()
        if provider not in vault or key_name not in vault[provider]:
            return None
        
        f = self._get_fernet()
        encrypted_value = vault[provider][key_name]
        return f.decrypt(encrypted_value.encode()).decode()

    def load_vault(self):
        if not self.vault_file.exists():
            return {}
        return json.loads(self.vault_file.read_text())

if __name__ == "__main__":
    import sys
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    gsm = GalaxySecretManager(root)
    
    if len(sys.argv) > 3 and sys.argv[1] == "set":
        gsm.store_secret(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) > 2 and sys.argv[1] == "get":
        print(gsm.get_secret(sys.argv[2], sys.argv[3]))
    else:
        print("Usage: secrets_manager.py [set provider key value | get provider key]")
