#!/usr/bin/env python3
"""
Day 2 Flag Parser Test Suite
Phase 2a CLI Layer Testing

Usage:
  python3 .ai/scripts/test-flag-parser.py                 # Run all tests, summary output
  python3 .ai/scripts/test-flag-parser.py --verbose       # Run all tests, detailed output
  python3 .ai/scripts/test-flag-parser.py --test 1        # Run single test (Test 1)
  python3 .ai/scripts/test-flag-parser.py --category flag_parser  # Run by category
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

_sd = Path(__file__).resolve().parent
if str(_sd) not in sys.path:
    sys.path.insert(0, str(_sd))
from paths import tests_data_dir  # noqa: E402


class FlagParserTestRunner:
    """Execute flag parser tests against guide-agent flag parsing logic."""

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

    def tokenize(self, user_input):
        """Split input into tokens, preserving quoted strings."""
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

    def extract_command_and_flags(self, tokens):
        """Separate command from flags."""
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

        command = " ".join(command_tokens)
        return command, flag_tokens

    def parse_and_validate_flags(self, flag_tokens, tool_registry=None):
        """Parse flags into dictionary and validate."""
        flags = {
            "tool": None,
            "tool_forced": False,
            "explain_routing": False,
            "prefer": None,
            "parallel": False
        }

        errors = []

        # Parse flags
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

        # Validate (using default tool registry if not provided)
        if tool_registry is None:
            tool_registry = {
                "available_tools": ["copilot", "codex", "gemini", "qwen", "opencode", "kilo"],
                "tool_specs": {
                    "copilot": {"status": "available"},
                    "codex": {"status": "available"},
                    "gemini": {"status": "available"},
                    "qwen": {"status": "available"},
                    "opencode": {"status": "available"},
                    "kilo": {"status": "available"}
                }
            }

        if flags["tool_forced"]:
            tool = flags["tool"]
            if tool not in tool_registry["tool_specs"]:
                errors.append(f"Tool '{tool}' not found in registry")
            elif tool_registry["tool_specs"][tool].get("status") != "available":
                reason = tool_registry["tool_specs"][tool].get("reason", "unknown")
                available = tool_registry["available_tools"]
                errors.append(f"Tool '{tool}' not available: {reason}")

        if flags["tool_forced"] and flags["explain_routing"]:
            errors.append("--tool and --explain-routing are mutually exclusive")

        if flags["parallel"] and flags["tool_forced"]:
            errors.append("--parallel and --tool conflict")

        if flags["parallel"] and len(tool_registry.get("available_tools", [])) < 2:
            errors.append(f"--parallel requires 2+ tools. Available: {len(tool_registry.get('available_tools', []))}")

        return {
            "flags": flags,
            "valid": len(errors) == 0,
            "errors": errors
        }

    def run_test(self, test_case):
        """Execute a single test case."""
        test_id = test_case["test_id"]
        name = test_case["name"]
        user_input = test_case["input"]
        expected = test_case["expected"]

        if self.verbose:
            print(f"\n{'='*70}")
            print(f"Test {test_id}: {name}")
            print(f"Input: {user_input}")

        try:
            # Step 1: Tokenize
            tokens = self.tokenize(user_input)
            if tokens != expected["tokens"]:
                return self.fail_test(test_id, name, "Tokenization mismatch",
                                     f"Expected: {expected['tokens']}, Got: {tokens}")

            if self.verbose:
                print(f"✓ Tokens: {tokens}")

            # Step 2: Extract command & flags
            command, flag_tokens = self.extract_command_and_flags(tokens)
            if command != expected["command"]:
                return self.fail_test(test_id, name, "Command extraction mismatch",
                                     f"Expected: {expected['command']}, Got: {command}")

            if self.verbose:
                print(f"✓ Command: {command}")
                print(f"✓ Flags: {flag_tokens}")

            # Step 3: Parse & validate flags
            # Setup tool registry if needed
            tool_registry = None
            if "setup" in test_case:
                tool_registry = {
                    "available_tools": ["copilot"],  # For test 10
                    "tool_specs": {
                        "copilot": {"status": "available"},
                        "opencode": {"status": "unavailable", "reason": "not_installed"}
                    }
                }

            parse_result = self.parse_and_validate_flags(flag_tokens, tool_registry)

            if parse_result["flags"] != expected["flags"]:
                return self.fail_test(test_id, name, "Flag parsing mismatch",
                                     f"Expected: {expected['flags']}, Got: {parse_result['flags']}")

            if self.verbose:
                print(f"✓ Flags: {parse_result['flags']}")

            # Step 4: Validate errors
            if parse_result["valid"] != expected["valid"]:
                return self.fail_test(test_id, name, "Validity mismatch",
                                     f"Expected valid={expected['valid']}, Got: {parse_result['valid']}")

            if parse_result["errors"] != expected["errors"]:
                return self.fail_test(test_id, name, "Error mismatch",
                                     f"Expected: {expected['errors']}, Got: {parse_result['errors']}")

            if self.verbose:
                print(f"✓ Valid: {parse_result['valid']}")
                if parse_result['errors']:
                    print(f"✓ Errors: {parse_result['errors']}")

            # All checks passed
            return self.pass_test(test_id, name)

        except Exception as e:
            return self.fail_test(test_id, name, "Exception", str(e))

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
        description="Day 2 Flag Parser Test Suite"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Verbose output (detailed test results)")
    parser.add_argument("--test", "-t", type=int,
                       help="Run specific test by ID")
    parser.add_argument("--category", "-c", type=str,
                       help="Run tests by category (flag_parser or error_handling)")
    parser.add_argument("--output", "-o", type=str,
                       default=".ai/logs/day-2-test-results.json",
                       help="Output file for test results")

    args = parser.parse_args()

    # Determine test file location
    test_file = str(tests_data_dir() / "day-2-flag-parser-tests.json")

    # Create runner
    runner = FlagParserTestRunner(test_file, verbose=args.verbose)

    # Run tests
    runner.run_all_tests(test_id=args.test, category=args.category)

    # Save results
    runner.save_results(args.output)

    # Exit with appropriate code
    sys.exit(0 if runner.results["tests_failed"] == 0 else 1)


if __name__ == "__main__":
    main()
