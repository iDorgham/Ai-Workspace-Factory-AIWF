import os
import unittest
import shutil
import tempfile
from factory.core.neural_sync.agent import NeuralSyncAgent
from factory.core.neural_sync.validator import SyncValidator

class TestNeuralSync(unittest.TestCase):
    """
    Industrial Unit Tests for Neural Fabric Sync Agent (unittest edition).
    """

    def setUp(self):
        self.sync_agent = NeuralSyncAgent(governor="Dorgham")
        self.validator = SyncValidator()
        self.source = tempfile.mkdtemp()
        self.target = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.source)
        shutil.rmtree(self.target)

    def test_agent_initialization(self):
        """Verifies that the agent initializes with correct OMEGA-tier metadata."""
        self.assertEqual(self.sync_agent.governor, "Dorgham")
        self.assertEqual(self.sync_agent.version, "20.0.0")
        self.assertIsNotNone(self.sync_agent.protocol)
        self.assertIsNotNone(self.sync_agent.validator)

    def test_naming_validation(self):
        """Verifies strict snake_case naming enforcement."""
        self.assertTrue(self.validator.validate_filename("valid_file_name.md"))
        self.assertFalse(self.validator.validate_filename("invalid-File-Name.MD"))
        self.assertTrue(self.validator.validate_filename("123_valid.py"))
        self.assertFalse(self.validator.validate_filename("space in name.txt"))

    def test_mirror_propagation(self):
        """Verifies physical file propagation between shards."""
        # Create test asset in source
        test_file = os.path.join(self.source, "test_asset.md")
        with open(test_file, "w") as f:
            f.write("# Industrial Asset\nVerified by Neural Sync.")
            
        # Execute sync
        result = self.sync_agent.sync_shard(self.source, self.target)
        
        # Verify results
        self.assertTrue(result)
        mirrored_file = os.path.join(self.target, "test_asset.md")
        self.assertTrue(os.path.exists(mirrored_file))
        with open(mirrored_file, "r") as f:
            self.assertIn("Verified by Neural Sync", f.read())

    def test_exclusion_rules(self):
        """Verifies that scratch and temporary files are excluded from sync."""
        # Create valid and excluded assets
        open(os.path.join(self.source, "valid_file.py"), 'a').close()
        open(os.path.join(self.source, ".DS_Store"), 'a').close()
        os.makedirs(os.path.join(self.source, "scratch"))
        open(os.path.join(self.source, "scratch/temporary.txt"), 'a').close()
        
        # Execute sync
        self.sync_agent.sync_shard(self.source, self.target)
        
        # Verify exclusions
        self.assertTrue(os.path.exists(os.path.join(self.target, "valid_file.py")))
        self.assertFalse(os.path.exists(os.path.join(self.target, ".DS_Store")))
        self.assertFalse(os.path.exists(os.path.join(self.target, "scratch")))

    def test_density_gate(self):
        """Verifies the 5-spec density gate for SDD planning phases."""
        # Create 3 specs (Failure case)
        for i in range(3):
            open(os.path.join(self.source, f"spec_test_{i}.md"), 'a').close()
        self.assertFalse(self.validator.validate_spec_density(self.source))
        
        # Add 2 more specs (Success case)
        for i in range(3, 5):
            open(os.path.join(self.source, f"spec_test_{i}.md"), 'a').close()
        self.assertTrue(self.validator.validate_spec_density(self.source))

    def test_residency_compliance(self):
        """Verifies Law 151/2020 geofencing logic."""
        # Sensitive path should be compliant if on MENA-SOIL
        self.assertTrue(self.validator.validate_path_residency("/Users/Dorgham/AIWF/workspaces/mena_client/legal/"))
        # Standard path should always be compliant
        self.assertTrue(self.validator.validate_path_residency("/Users/Dorgham/AIWF/docs/roadmap.md"))

if __name__ == "__main__":
    unittest.main()
