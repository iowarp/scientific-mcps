"""
Helper functions for WRP Test Framework
Contains utility functions for response parsing, JSON validation, and environment detection
"""
import json
import re
import os
from typing import Dict, Any, List
from jsonschema import validate, ValidationError


def extract_response_content(full_output: str) -> List[str]:
    """Extract the actual response content from WRP output using regex"""
    # Pattern: Query: followed by response until next Query: or session end
    pattern = r'Query:\s*\n(.*?)(?=\nQuery:|\nSession with|\nExiting\.\.\.|\Z)'
    matches = re.findall(pattern, full_output, re.DOTALL)
    responses = []

    for match in matches:
        cleaned = match.strip()
        if cleaned and not cleaned.startswith('Exiting') and not cleaned.startswith('Session with'):
            responses.append(cleaned)

    return responses


def extract_json_from_response(response: str) -> Dict[str, Any]:
    """Extract JSON from WRP response text with detailed error reporting"""
    extraction_attempts = []

    # Look for ```json blocks
    if "```json" in response:
        start = response.find("```json") + 7
        end = response.find("```", start)
        if end != -1:
            json_text = response[start:end].strip()
            try:
                return json.loads(json_text)
            except json.JSONDecodeError as e:
                extraction_attempts.append(f"Markdown JSON blocks: JSONDecodeError - {e}")
        else:
            extraction_attempts.append("Markdown JSON blocks: Found opening ```json but no closing ```")

    # Look for generic ``` blocks
    if "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        if end != -1:
            json_text = response[start:end].strip()
            try:
                return json.loads(json_text)
            except json.JSONDecodeError as e:
                extraction_attempts.append(f"Generic code blocks: JSONDecodeError - {e}")
        else:
            extraction_attempts.append("Generic code blocks: Found opening ``` but no closing ```")

    # Look for JSON object patterns
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, response, re.DOTALL)

    if matches:
        for i, match in enumerate(matches):
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError as e:
                extraction_attempts.append(f"Regex pattern match {i+1}: JSONDecodeError - {e}")
    else:
        extraction_attempts.append("Regex pattern search: No JSON-like patterns found")

    # Try parsing the entire response as JSON
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError as e:
        extraction_attempts.append(f"Direct parsing: JSONDecodeError - {e}")

    # Create detailed error message
    error_msg = f"No valid JSON found in response. Attempted extractions:\n"
    for attempt in extraction_attempts:
        error_msg += f"  - {attempt}\n"
    error_msg += f"\nResponse content (first 500 chars): {response[:500]}"

    raise ValueError(error_msg)


def validate_json_response(response_json: Dict[str, Any], expected_json: Dict[str, Any], 
                          json_schema: Dict[str, Any]) -> None:
    """Validate JSON response against expected values and schema"""

    # Validate against schema if provided
    if json_schema:
        try:
            validate(instance=response_json, schema=json_schema)
        except ValidationError as e:
            raise AssertionError(f"JSON schema validation failed: {e.message}")

    # Validate against expected values if provided
    if expected_json:
        for key, expected_value in expected_json.items():
            if key not in response_json:
                raise AssertionError(f"Missing expected key '{key}' in response")

            actual_value = response_json[key]
            if actual_value != expected_value:
                raise AssertionError(
                    f"Expected {key}='{expected_value}', got '{actual_value}'"
                )
