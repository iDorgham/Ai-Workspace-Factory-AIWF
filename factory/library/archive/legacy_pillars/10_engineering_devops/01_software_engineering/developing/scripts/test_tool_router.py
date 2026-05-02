#!/usr/bin/env python3
"""
Day 3 Tool-Router Test Suite
Tests all 4 routing modes: normal, explain, forced, parallel

Usage:
  python3 .ai/scripts/test-tool-router.py                 # Summary
  python3 .ai/scripts/test-tool-router.py --verbose       # Detailed
  python3 .ai/scripts/test-tool-router.py --test 1        # Single test
  python3 .ai/scripts/test-tool-router.py --category normal_mode  # By category
"""

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path

_sd = Path(__file__).resolve().parent
if str(_sd) not in sys.path:
    sys.path.insert(0, str(_sd))
from paths import tests_data_dir  # noqa: E402

# Import the tool router
tool_router_path = Path(__file__).parent / "tool_router_v2.py"
spec = importlib.util.spec_from_file_location("tool_router", tool_router_path)
tool_router_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool_router_module)
ToolRouter = tool_router_module.ToolRouter


class ToolRouterTestRunner:
    """Execute tool-router tests against routing logic."""

    def __init__(self, test_file, verbose=False):
        self.test_file = test_file
        self.verbose = verbose
        self.results = {
            "run_date": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": []
        }
        self.load_tests()
        self.setup_test_environment()

    def load_tests(self):
        """Load test suite from JSON file."""
        try:
            with open(self.test_file, 'r') as f:
                self.test_data = json.load(f)
            print(f"✅ Loaded {len(self.test_data['tests'])} tests from {self.test_file}")
        except FileNotFoundError:
            print(f"❌ Test file not found: {self.test_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in test file: {e}")
            sys.exit(1)

    def setup_test_environment(self):
        """Setup tool registry and command routing for tests."""
        # Create default tool registry
        self.tool_registry = {
            "available_tools": ["copilot", "codex", "gemini", "qwen"],
            "tool_specs": {
                "copilot": {
                    "latency_ms": 3500,
                    "cost_usd": 0.003,
                    "success_rate": 0.97,
                    "rank": 1
                },
                "codex": {
                    "latency_ms": 2500,
                    "cost_usd": 0.002,
                    "success_rate": 0.96,
                    "rank": 2
                },
                "gemini": {
                    "latency_ms": 3100,
                    "cost_usd": 0.075,
                    "success_rate": 0.96,
                    "rank": 3
                },
                "qwen": {
                    "latency_ms": 4200,
                    "cost_usd": 0.0001,
                    "success_rate": 0.94,
                    "rank": 4
                }
            }
        }

        # Create command routing
        self.command_routing = {
            "create_blog_posts": {
                "optimization": "quality_over_speed",
                "ranking": ["copilot", "codex", "gemini", "qwen"]
            },
            "optimize_images": {
                "optimization": "multimodal_required",
                "ranking": ["gemini", "codex", "copilot", "qwen"]
            }
        }

    def run_test(self, test_case):
        """Execute a single test case."""
        test_id = test_case["test_id"]
        name = test_case["name"]
        command = test_case["command"]
        flags = test_case["flags"]
        setup = test_case.get("setup", {})
        expected = test_case["expected"]

        if self.verbose:
            print(f"\n{'='*70}")
            print(f"Test {test_id}: {name}")
            print(f"Command: {command}")
            print(f"Flags: {flags}")

        try:
            # Update tool registry based on setup
            test_results = {}
            if setup:
                test_results = self._apply_setup(setup)

            # Create router (with test mode enabled)
            router = ToolRouter(self.tool_registry, self.command_routing,
                               test_mode=True, test_results=test_results)

            # Route command
            result = router.route_command(command, flags)

            if self.verbose:
                print(f"Result status: {result.get('status')}")

            # Verify result
            return self._verify_result(test_id, name, result, expected, flags, test_case)

        except Exception as e:
            return self.fail_test(test_id, name, "Exception", str(e))

    def _apply_setup(self, setup):
        """Apply test setup (modify tool registry, etc.). Returns test_results dict."""
        if "available_tools" in setup:
            self.tool_registry["available_tools"] = setup["available_tools"]

        # Reset to specific tools for this test
        available = self.tool_registry["available_tools"]
        filtered_specs = {
            k: v for k, v in self.tool_registry["tool_specs"].items()
            if k in available
        }
        self.tool_registry["tool_specs"] = filtered_specs

        # Extract tool results from setup
        test_results = {}

        # Method 1: Explicit tool + result mapping
        for key in list(setup.keys()):
            if key.endswith("_result") and not key.startswith("rank"):
                # e.g., "forced_tool_result" -> "forced_tool"
                tool_key = key.replace("_result", "")
                if tool_key in setup:
                    tool_name = setup[tool_key]
                    test_results[tool_name] = setup[key]

        # Method 2: Rank-based results (for normal mode fallback testing)
        if "rank_1_result" in setup:
            # Get first available tool (Rank 1)
            rank_1_tool = available[0]
            test_results[rank_1_tool] = setup["rank_1_result"]

        if "rank_2_result" in setup and len(available) > 1:
            # Get second available tool (Rank 2)
            rank_2_tool = available[1]
            test_results[rank_2_tool] = setup["rank_2_result"]

        if "rank_3_result" in setup and len(available) > 2:
            # Get third available tool (Rank 3)
            rank_3_tool = available[2]
            test_results[rank_3_tool] = setup["rank_3_result"]

        return test_results

    def _verify_result(self, test_id, name, result, expected, flags, test_case):
        """Verify test result against expected output."""
        # Basic status check
        if result.get("status") != expected.get("status"):
            return self.fail_test(
                test_id, name, "Status mismatch",
                f"Expected: {expected.get('status')}, Got: {result.get('status')}"
            )

        # Mode-specific checks
        category = test_case.get("category")

        if category == "normal_mode":
            return self._verify_normal_mode(test_id, name, result, expected)
        elif category == "explain_mode":
            return self._verify_explain_mode(test_id, name, result, expected)
        elif category == "forced_mode":
            return self._verify_forced_mode(test_id, name, result, expected)
        elif category == "parallel_mode":
            return self._verify_parallel_mode(test_id, name, result, expected)

        return self.pass_test(test_id, name)

    def _verify_normal_mode(self, test_id, name, result, expected):
        """Verify normal mode results."""
        if result.get("status") == "success":
            if result.get("tool") != expected.get("tool_used"):
                return self.fail_test(
                    test_id, name, "Tool mismatch",
                    f"Expected: {expected.get('tool_used')}, Got: {result.get('tool')}"
                )
            if result.get("tool_rank") != expected.get("tool_rank"):
                return self.fail_test(
                    test_id, name, "Tool rank mismatch",
                    f"Expected: {expected.get('tool_rank')}, Got: {result.get('tool_rank')}"
                )

        return self.pass_test(test_id, name)

    def _verify_explain_mode(self, test_id, name, result, expected):
        """Verify explain mode results."""
        if result.get("status") != "explanation":
            return self.fail_test(
                test_id, name, "Not explanation mode",
                f"Status should be 'explanation', got: {result.get('status')}"
            )

        if not result.get("ranking"):
            return self.fail_test(
                test_id, name, "Missing ranking",
                "Explanation should include ranking list"
            )

        if result.get("selected_tool") != expected.get("selected_tool"):
            return self.fail_test(
                test_id, name, "Selected tool mismatch",
                f"Expected: {expected.get('selected_tool')}, Got: {result.get('selected_tool')}"
            )

        return self.pass_test(test_id, name)

    def _verify_forced_mode(self, test_id, name, result, expected):
        """Verify forced mode results."""
        if expected.get("status") == "success":
            if result.get("tool_forced") != True:
                return self.fail_test(
                    test_id, name, "Not forced",
                    "tool_forced should be True"
                )

        return self.pass_test(test_id, name)

    def _verify_parallel_mode(self, test_id, name, result, expected):
        """Verify parallel mode results."""
        expected_status = expected.get("status")
        actual_status = result.get("status")

        if actual_status != expected_status:
            return self.fail_test(
                test_id, name, "Status mismatch",
                f"Expected: {expected_status}, Got: {actual_status}"
            )

        if actual_status in ["success_both", "partial"]:
            if not result.get("outputs"):
                return self.fail_test(
                    test_id, name, "Missing outputs",
                    "Should have outputs dict"
                )

        return self.pass_test(test_id, name)

    def pass_test(self, test_id, name):
        """Record passing test."""
        self.results["tests_passed"] += 1
        self.results["tests_run"] += 1
        result = {
            "test_id": test_id,
            "name": name,
            "status": "PASS",
            "message": "All assertions passed"
        }
        self.results["test_results"].append(result)
        if not self.verbose:
            print(f"✅ Test {test_id}: {name}")
        else:
            print(f"\n✅ PASS")
        return True

    def fail_test(self, test_id, name, reason, details):
        """Record failing test."""
        self.results["tests_failed"] += 1
        self.results["tests_run"] += 1
        result = {
            "test_id": test_id,
            "name": name,
            "status": "FAIL",
            "reason": reason,
            "details": details
        }
        self.results["test_results"].append(result)
        if not self.verbose:
            print(f"❌ Test {test_id}: {name}")
            print(f"   Reason: {reason}")
        else:
            print(f"\n❌ FAIL")
            print(f"Reason: {reason}")
            print(f"Details: {details}")
        return False

    def run_all_tests(self, test_id=None, category=None):
        """Run all or filtered tests."""
        tests = self.test_data["tests"]

        if test_id:
            tests = [t for t in tests if t["test_id"] == test_id]

        if category:
            tests = [t for t in tests if t["category"] == category]

        print(f"\nRunning {len(tests)} tests...\n")

        for test in tests:
            self.run_test(test)

        self.print_summary()

    def print_summary(self):
        """Print test summary."""
        total = self.results["tests_run"]
        passed = self.results["tests_passed"]
        failed = self.results["tests_failed"]
        pass_rate = (passed / total * 100) if total > 0 else 0

        print(f"\n{'='*70}")
        print(f"TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests:  {total}")
        print(f"Passed:       {passed} ✅")
        print(f"Failed:       {failed} ❌")
        print(f"Pass Rate:    {pass_rate:.1f}%")
        print(f"{'='*70}")

        if failed == 0:
            print(f"\n🎉 ALL TESTS PASSED!")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Review details above.")

        return failed == 0

    def save_results(self, output_file):
        """Save test results to JSON file."""
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)

            print(f"\n📄 Results saved to: {output_file}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Day 3 Tool-Router Test Suite"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output (detailed test results)")
    parser.add_argument("--test", "-t", type=int,
                       help="Run specific test by ID")
    parser.add_argument("--category", "-c", type=str,
                       help="Run tests by category")
    parser.add_argument("--output", "-o", type=str,
                       default=".ai/logs/day-3-test-results.json",
                       help="Output file for test results")

    args = parser.parse_args()

    # Determine test file location
    test_file = str(tests_data_dir() / "day-3-tool-router-tests.json")

    # Create runner
    runner = ToolRouterTestRunner(test_file, verbose=args.verbose)

    # Run tests
    runner.run_all_tests(test_id=args.test, category=args.category)

    # Save results
    runner.save_results(args.output)

    # Exit with appropriate code
    sys.exit(0 if runner.results["tests_failed"] == 0 else 1)


if __name__ == "__main__":
    main()
