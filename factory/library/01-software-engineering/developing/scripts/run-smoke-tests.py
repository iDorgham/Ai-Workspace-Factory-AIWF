#!/usr/bin/env python3
"""
Day 4 Smoke Tests — End-to-End Integration Testing
Tests Phase 2a (flag parsing) + Phase 1 (tool routing) together

Usage:
  python3 .ai/scripts/run-smoke-tests.py              # Summary
  python3 .ai/scripts/run-smoke-tests.py --verbose    # Detailed
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

# Import the flag parser
test_flag_parser_path = Path(__file__).parent / "test-flag-parser.py"
spec2 = importlib.util.spec_from_file_location("test_flag_parser", test_flag_parser_path)
test_flag_parser_module = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(test_flag_parser_module)


class SmokeTestRunner:
    """Execute end-to-end smoke tests for Phase 2a + Phase 1 integration."""

    def __init__(self, test_file, verbose=False):
        self.test_file = test_file
        self.verbose = verbose
        self.results = {
            "run_date": datetime.now().isoformat(),
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": [],
            "logs_generated": []
        }
        self.execution_logs = []
        self.load_tests()
        self.setup_test_environment()

    def load_tests(self):
        """Load smoke test cases from JSON."""
        try:
            with open(self.test_file, 'r') as f:
                self.test_data = json.load(f)
            print(f"✅ Loaded {len(self.test_data['tests'])} smoke tests from {self.test_file}")
        except FileNotFoundError:
            print(f"❌ Test file not found: {self.test_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            sys.exit(1)

    def setup_test_environment(self):
        """Setup tool registry and command routing."""
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

        self.command_routing = {
            "create_blog_posts": {
                "optimization": "quality_over_speed",
                "ranking": ["copilot", "codex", "gemini", "qwen"]
            },
            "optimize_images": {
                "optimization": "multimodal_required",
                "ranking": ["gemini", "codex", "copilot", "qwen"]
            },
            "export": {
                "optimization": "speed_cost",
                "ranking": ["qwen", "codex", "copilot", "gemini"]
            }
        }

    def run_test(self, test_case):
        """Execute a single smoke test."""
        test_id = test_case["test_id"]
        name = test_case["name"]
        user_input = test_case["input"]
        expected = test_case["expected"]

        if self.verbose:
            print(f"\n{'='*70}")
            print(f"Test {test_id}: {name}")
            print(f"Input: {user_input}")

        try:
            # Parse CLI input (Phase 2a)
            tokens = self._tokenize(user_input)
            command, flag_tokens = self._extract_command_and_flags(tokens)
            parse_result = self._parse_and_validate_flags(flag_tokens)

            if not parse_result["valid"]:
                # Phase 2a validation failed - this is expected for error tests
                return self._verify_error_result(test_id, name, parse_result, expected)

            # Phase 2a successful - now route to Phase 1
            flags = parse_result["flags"]
            setup = test_case.get("setup", {})
            test_results = self._apply_setup(setup) if setup else {}

            # Create router and route command (Phase 1)
            router = ToolRouter(self.tool_registry, self.command_routing,
                              test_mode=True, test_results=test_results)
            result = router.route_command(command, flags)

            # Log execution
            self._log_execution(user_input, command, flags, result)

            # Verify result
            return self._verify_result(test_id, name, result, expected)

        except Exception as e:
            return self.fail_test(test_id, name, "Exception", str(e))

    def _tokenize(self, user_input):
        """Tokenize user input."""
        tokens = []
        current_token = ""
        in_quotes = False

        for char in user_input:
            if char == '"':
                in_quotes = not in_quotes
            elif char == " " and not in_quotes:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
            else:
                current_token += char

        if current_token:
            tokens.append(current_token)

        return tokens

    def _extract_command_and_flags(self, tokens):
        """Extract command and flags from tokens."""
        command_tokens = []
        flag_tokens = []
        parsing_command = True

        for token in tokens:
            if token.startswith("--"):
                parsing_command = False
                flag_tokens.append(token)
            elif parsing_command:
                command_tokens.append(token)
            else:
                flag_tokens.append(token)

        return " ".join(command_tokens), flag_tokens

    def _parse_and_validate_flags(self, flag_tokens):
        """Parse and validate flags."""
        flags = {
            "tool": None,
            "tool_forced": False,
            "explain_routing": False,
            "prefer": None,
            "parallel": False
        }
        errors = []

        i = 0
        while i < len(flag_tokens):
            token = flag_tokens[i]
            if token == "--tool" and i + 1 < len(flag_tokens):
                flags["tool"] = flag_tokens[i + 1]
                flags["tool_forced"] = True
                i += 2
            elif token == "--explain-routing":
                flags["explain_routing"] = True
                i += 1
            elif token == "--prefer" and i + 1 < len(flag_tokens):
                flags["prefer"] = flag_tokens[i + 1]
                i += 2
            elif token == "--parallel":
                flags["parallel"] = True
                i += 1
            else:
                i += 1

        # Validate
        if flags["tool_forced"]:
            if flags["tool"] not in self.tool_registry["tool_specs"]:
                errors.append(f"Tool '{flags['tool']}' not found in registry")
            elif flags["tool_forced"] and flags["explain_routing"]:
                errors.append("--tool and --explain-routing are mutually exclusive")

        return {
            "flags": flags,
            "valid": len(errors) == 0,
            "errors": errors
        }

    def _apply_setup(self, setup):
        """Apply test setup for deterministic results."""
        test_results = {}
        available = self.tool_registry["available_tools"]

        if "rank_1_fails" in setup:
            test_results[available[0]] = "timeout"
        if "rank_2_succeeds" in setup and len(available) > 1:
            test_results[available[1]] = "success"

        return test_results

    def _log_execution(self, user_input, command, flags, result):
        """Log execution to workflow and tool-performance logs."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "command": command,
            "status": result.get("status"),
            "tool": result.get("tool"),
            "tool_rank": result.get("tool_rank"),
            "error_type": result.get("error_type")
        }
        self.execution_logs.append(log_entry)

    def _verify_error_result(self, test_id, name, parse_result, expected):
        """Verify error result from Phase 2a."""
        if expected.get("status") == "error":
            return self.pass_test(test_id, name)
        else:
            return self.fail_test(test_id, name, "Unexpected error", str(parse_result["errors"]))

    def _verify_result(self, test_id, name, result, expected):
        """Verify result against expected output."""
        if result.get("status") != expected.get("status"):
            return self.fail_test(
                test_id, name, "Status mismatch",
                f"Expected: {expected.get('status')}, Got: {result.get('status')}"
            )

        # Mode-specific checks
        category = self._get_test_category(test_id)

        if category == "integration":
            return self._verify_integration(test_id, name, result, expected)
        elif category == "error_handling":
            return self._verify_error(test_id, name, result, expected)
        elif category == "command_routing":
            return self._verify_routing(test_id, name, result, expected)
        elif category == "fallback_logic":
            return self._verify_fallback(test_id, name, result, expected)

        return self.pass_test(test_id, name)

    def _get_test_category(self, test_id):
        """Get test category from test data."""
        for test in self.test_data["tests"]:
            if test["test_id"] == test_id:
                return test.get("category")
        return "integration"

    def _verify_integration(self, test_id, name, result, expected):
        """Verify integration test."""
        if result.get("status") == "success":
            if result.get("tool") != expected.get("tool_selected"):
                return self.fail_test(test_id, name, "Tool mismatch",
                                     f"Expected: {expected.get('tool_selected')}, Got: {result.get('tool')}")
        return self.pass_test(test_id, name)

    def _verify_error(self, test_id, name, result, expected):
        """Verify error test."""
        if result.get("error_type") == expected.get("error_type"):
            return self.pass_test(test_id, name)
        return self.fail_test(test_id, name, "Error type mismatch",
                             f"Expected: {expected.get('error_type')}, Got: {result.get('error_type')}")

    def _verify_routing(self, test_id, name, result, expected):
        """Verify command routing."""
        if result.get("tool") == expected.get("tool_selected"):
            return self.pass_test(test_id, name)
        return self.fail_test(test_id, name, "Tool routing mismatch",
                             f"Expected: {expected.get('tool_selected')}, Got: {result.get('tool')}")

    def _verify_fallback(self, test_id, name, result, expected):
        """Verify fallback logic."""
        if result.get("fallback_used") == expected.get("fallback_used"):
            return self.pass_test(test_id, name)
        return self.fail_test(test_id, name, "Fallback mismatch", "Fallback logic incorrect")

    def pass_test(self, test_id, name):
        """Record passing test."""
        self.results["tests_passed"] += 1
        self.results["tests_run"] += 1
        result = {
            "test_id": test_id,
            "name": name,
            "status": "PASS",
            "message": "Test passed"
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
            print(f"\n❌ FAIL: {reason}")
        return False

    def run_all_tests(self):
        """Run all smoke tests."""
        tests = self.test_data["tests"]
        print(f"\nRunning {len(tests)} smoke tests...\n")

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
        print(f"SMOKE TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests:  {total}")
        print(f"Passed:       {passed} ✅")
        print(f"Failed:       {failed} ❌")
        print(f"Pass Rate:    {pass_rate:.1f}%")
        print(f"{'='*70}")

        if failed == 0:
            print(f"\n🎉 ALL SMOKE TESTS PASSED!")
        else:
            print(f"\n⚠️  {failed} test(s) failed.")

        return failed == 0

    def save_results(self, output_file):
        """Save test results to JSON."""
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)

            print(f"📄 Results saved to: {output_file}")
            self.results["logs_generated"].append(output_file)
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

    def save_execution_logs(self, log_file):
        """Append execution logs to workflow.jsonl."""
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            with open(log_file, 'a') as f:
                for log in self.execution_logs:
                    f.write(json.dumps(log) + '\n')

            print(f"📄 Execution logs appended to: {log_file}")
            self.results["logs_generated"].append(log_file)
        except Exception as e:
            print(f"❌ Failed to save logs: {e}")


def main():
    parser = argparse.ArgumentParser(description="Day 4 Smoke Tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--output", "-o", type=str, default=".ai/logs/day-4-smoke-tests-results.json",
                       help="Output file for test results")
    parser.add_argument("--logs", "-l", type=str, default=".ai/logs/workflow.jsonl",
                       help="Workflow log file")

    args = parser.parse_args()

    test_file = str(tests_data_dir() / "day-4-smoke-tests.json")
    runner = SmokeTestRunner(test_file, verbose=args.verbose)

    runner.run_all_tests()
    runner.save_results(args.output)
    runner.save_execution_logs(args.logs)

    sys.exit(0 if runner.results["tests_failed"] == 0 else 1)


if __name__ == "__main__":
    main()
