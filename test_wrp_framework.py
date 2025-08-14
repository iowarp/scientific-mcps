"""
WRP Test Framework - Pytest-based test runner
Tests WRP (bin/wrp.py) by feeding prompts and validating JSON responses
"""
import yaml
import asyncio
import sys
import argparse
import json
import time
import os

from pathlib import Path
from typing import Dict, Any, List
from test_wrp_helpers import (
    extract_response_content,
    extract_json_from_response,
    validate_json_response
)

# Global test yaml path prefix
TEST_YAML_PATH_PREFIX = "./bin/confs/test/"

# Available providers from factory.py
AVAILABLE_PROVIDERS = [
    "gemini", "ollama", "openai", "claude", "opencode", "claudecode"
]


class WRPTestTurn:
    """A single prompt/response turn in a test case"""

    def __init__(self, prompt: str, expected_json, json_schema):
        self.prompt = prompt
        self.expected_json = expected_json
        self.json_schema = json_schema


class WRPTestCase:
    """A test case for WRP client"""

    def __init__(self, test_data: Dict[str, Any]):
        self.name = test_data['name']
        self.description = test_data['description']
        # TBD: The 'mcps' field here is duplicating info from the YAML
        # just to meet wrp.py expected config interface.
        # It would be nice to rework this if/when MCP discovery is reworked
        self.mcps = test_data['mcps']
        self.timeout = test_data.get('timeout', 30)
        turns_data = test_data.get('turns', [])

        self.turns = []

        for turn_data in turns_data:
            turn = WRPTestTurn(turn_data['prompt'],
                                turn_data.get('expected_json', {}),
                                turn_data.get('json_schema', {}))

            self.turns.append(turn)


class WRPTestRunner:
    """Runs WRP tests by executing wrp.py as subprocess"""

    def __init__(self, test_cases_path: str = "test_wrp.yaml"):
        # Test iteration count for robustness checking
        self.iteration_count = 1

        # Wait time between iterations (seconds) to avoid rate limits
        self.wait_time = 3

        self.wrp_script = Path("bin/wrp.py")
        self.tests = self.load_tests(test_cases_path)

    def load_tests(self, test_cases_path) -> List[WRPTestCase]:
        """Load test configurations from YAML"""
        if not os.path.exists(test_cases_path):
            raise FileNotFoundError(f"Test file not found: {test_cases_path}")

        try:
            with open(test_cases_path, 'r') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failure while reading test yaml {test_cases_path}: {e}")   

        return [WRPTestCase(test) for test in data.get('tests', [])]

    async def _execute_wrp_subprocess(self, provider: str, input_text: str, timeout: int) -> str:
        """Execute WRP as subprocess with given input and return stdout"""
        # TBD - Expand handling if integration tests that use other MCPs are added
        wrp_config_path = TEST_YAML_PATH_PREFIX + provider.lower() + "_arxiv.yaml"

        try:
            cmd = [
                sys.executable, 
                str(self.wrp_script), 
                f"--conf={wrp_config_path}"
            ]

            # Create subprocess
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=Path.cwd()
            )

            try:
                # Send input and get output
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=input_text.encode()),
                    timeout=timeout
                )

                if process.returncode != 0:
                    raise RuntimeError(f"WRP failed with code {process.returncode}: {stderr.decode()}")

                return stdout.decode().strip()

            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise TimeoutError(f"WRP process timed out after {timeout} seconds")

        except Exception as e:
            raise RuntimeError(f"WRP execution failed: {e}")

    async def run_test(self, test_case: WRPTestCase, provider: str) -> Dict[str, Any]:
        """Run a single test N times for robustness checking and return aggregated results"""
        iterations = []
        successful_runs = 0

        # Run the test N times per provider
        for iteration in range(self.iteration_count):
            try:
                result = await self._run_single_test_iteration(test_case, provider)
                iterations.append(result)
                if result['passed']:
                    successful_runs += 1
            except Exception as e:
                iterations.append({
                    'passed': False,
                    'response': '',
                    'response_json': None,
                    'error': str(e),
                    'iteration': iteration + 1
                })
            # Add wait time between iterations (except for the first one)
            if self.wait_time > 0:
                await asyncio.sleep(self.wait_time)

        # Determine overall success (all iterations must pass)
        all_passed = successful_runs == self.iteration_count

        # Get the first successful result for backward compatibility
        successful_result = next((r for r in iterations if r['passed']), None)

        return {
            'passed': all_passed,
            'response': successful_result['response'] if successful_result else iterations[-1]['response'],
            'response_json': successful_result['response_json'] if successful_result else None,
            'error': None if all_passed else f"Only {successful_runs}/{self.iteration_count} iterations passed",
            'iterations': iterations,
            'successful_runs': successful_runs,
            'total_runs': self.iteration_count
        }

    async def _run_single_test_iteration(self, test_case: WRPTestCase, provider: str) -> Dict[str, Any]:
        """Run a single iteration of a test and return results"""
        try:
            if (len(test_case.turns) > 1):
                # Multi-turn test
                # Prepare input for WRP (all prompts + quit command)
                input = ""
                for turn in test_case.turns:
                    input += turn.prompt + "\n"
                input += "quit\n"
            else:
                # Single-turn test
                input = f"{test_case.turns[0].prompt}\nquit\n"

            # Execute WRP subprocess
            full_output = await self._execute_wrp_subprocess(provider, input, test_case.timeout)

            # Extract the response content
            responses = extract_response_content(full_output)

            if len(responses) != len(test_case.turns):
                raise RuntimeError(f"Expected {len(test_case.turns)} responses, got {len(responses)}")

            # Validate each turn's response
            all_response_json = []
            for i, (response, turn) in enumerate(zip(responses, test_case.turns)):
                try:
                    response_json = extract_json_from_response(response)
                    validate_json_response(
                        response_json,
                        turn.expected_json,
                        turn.json_schema
                    )
                    all_response_json.append(response_json)
                except Exception as e:
                    raise RuntimeError(f"Turn {i+1} failed: {e}")

            return {
                'passed': True,
                'response': responses,
                'response_json': all_response_json,
                'error': None
            }
        except Exception as e:
            return {
                'passed': False,
                'response': getattr(e, 'response', ''),
                'response_json': None,
                'error': str(e)
            }


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Run WRP test framework")
    parser.add_argument(
        "--provider",
        required=True,
        choices=AVAILABLE_PROVIDERS,
        help=f"LLM provider to use. Available options: {', '.join(AVAILABLE_PROVIDERS)}"
    )
    parser.add_argument(
        "--debug",
        required=False,
        action='store_true',
        help="Whether to print debug output"
    )

    return parser.parse_args()


if __name__ == "__main__":
    async def main():
        args = parse_args()
        provider = args.provider.lower()
        debug = args.debug
        total_time = 0.0

        # Validate provider exists in available providers
        if provider not in AVAILABLE_PROVIDERS:
            print(f"Error: Invalid provider '{provider}'. Available providers: {', '.join(AVAILABLE_PROVIDERS)}")
            sys.exit(1)
        
        print(f"Running tests with provider: {provider}")
        
        runner = WRPTestRunner()

        for test_case in runner.tests:
            print(f"\n=== Running {test_case.name} ({provider}, {runner.iteration_count} iterations) ===")

            start_time = time.time()
            result = await runner.run_test(test_case, provider)
            elapsed_time = (time.time() - start_time) - ((runner.iteration_count - 1) * runner.wait_time)
            total_time += elapsed_time

            print(f"Passed: {result['passed']} ({result['successful_runs']}/{result['total_runs']} iterations successful, {elapsed_time}s)")
            if not result['passed']:
                print(f"Error: {result['error']}")

            # Show details on failure
            if result['response_json'] and not result['passed']:
                print(f"JSON: {json.dumps(result['response_json'], indent=2)}")

            if result['successful_runs'] < result['total_runs']:
                print(f" Iteration Details:")
                for i, iteration in enumerate(result['iterations']):
                    print(f"  Iteration {i+1}: {'PASS' if iteration['passed'] else 'FAIL'}")
                    if not iteration['passed']:
                        print(f"    Error: {iteration['error']}")

        print(f"Total time: {total_time}")

    asyncio.run(main())