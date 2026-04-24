import unittest
import datetime
from ..core import PlanningWithFilesMastery

class TestPlanningWithFilesMastery(unittest.TestCase):
    def setUp(self):
        self.sdd = PlanningWithFilesMastery()

    def test_audit_artifact_sync_compliant(self):
        states = {"plan_approved": True, "task_list_exists": True, "code_drift_detected": False}
        result = self.sdd.audit_artifact_sync(states)
        self.assertTrue(result["is_synchronized"])
        self.assertEqual(result["status"], "SDD_COMPLIANT")

    def test_audit_artifact_sync_drift(self):
        states = {"plan_approved": True, "task_list_exists": True, "code_drift_detected": True}
        result = self.sdd.audit_artifact_sync(states)
        self.assertFalse(result["is_synchronized"])
        self.assertEqual(result["status"], "SPEC_DIVERGENCE")

    def test_validate_discovery_capture_safe(self):
        discovery = [{"fact": "api_v2_url", "is_in_spec": True}]
        result = self.sdd.validate_discovery_capture(discovery)
        self.assertTrue(result["is_spec_safe"])

    def test_validate_discovery_capture_unsafe(self):
        discovery = [{"fact": "new_dependency_requirement", "is_in_spec": False}]
        result = self.sdd.validate_discovery_capture(discovery)
        self.assertFalse(result["is_spec_safe"])
        self.assertEqual(result["required_action"], "UPDATE_PLAN_BEFORE_RESUMING")

    def test_verify_turn_transition_persistent(self):
        recent = datetime.datetime.now() - datetime.timedelta(minutes=5)
        meta = {"last_artifact_update_time": recent}
        result = self.sdd.verify_turn_transition(meta)
        self.assertTrue(result["is_state_persisted"])
        self.assertEqual(result["transition_health"], "OPTIMIZED")

    def test_verify_turn_transition_stale(self):
        stale = datetime.datetime.now() - datetime.timedelta(hours=1)
        meta = {"last_artifact_update_time": stale}
        result = self.sdd.verify_turn_transition(meta)
        self.assertFalse(result["is_state_persisted"])
        self.assertEqual(result["transition_health"], "RISKY_STATE_LOSS")

if __name__ == '__main__':
    unittest.main()
