import unittest
from ..core import AppDevelopingMastery

class TestAppDevelopingMastery(unittest.TestCase):
    def setUp(self):
        self.app = AppDevelopingMastery()

    def test_audit_expo_config_success(self):
        config = {
            "expo": {
                "name": "Test App",
                "slug": "test-app",
                "version": "1.0.0",
                "icon": "./assets/icon.png",
                "splash": {"image": "./assets/splash.png"},
                "sdkVersion": "51.0.0"
            }
        }
        result = self.app.audit_expo_config(config)
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["sdk_version"], "51.0.0")

    def test_audit_expo_config_missing_assets(self):
        config = {"expo": {"name": "Bad App"}}
        result = self.app.audit_expo_config(config)
        self.assertFalse(result["is_valid"])
        self.assertIn("splash", str(result["issues"]))

    def test_validate_eas_config(self):
        valid_eas = {"build": {"production": {"distribution": "store"}}}
        self.assertTrue(self.app.validate_eas_config(valid_eas))
        
        invalid_eas = {"build": {"development": {}}}
        self.assertFalse(self.app.validate_eas_config(invalid_eas))

    def test_check_universal_links_violations(self):
        config = {"expo": {"ios": {}, "android": {}}}
        violations = self.app.check_universal_links(config)
        self.assertEqual(len(violations), 2)
        self.assertIn("IOS", violations[0])
        self.assertIn("ANDROID", violations[1])

if __name__ == '__main__':
    unittest.main()
