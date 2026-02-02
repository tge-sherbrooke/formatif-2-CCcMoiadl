#!/usr/bin/env python3
"""
Milestone 2: DHT22 Sensor with Retry Logic (35 points)
======================================================

This milestone verifies that the student has:
1. Created DHT22 sensor reading script
2. Implemented RETRY LOGIC (critical for DHT22!)
3. Used Adafruit libraries correctly

IMPORTANT: DHT22 errors are NORMAL! The one-wire protocol is timing-sensitive
and fails 10-20% of the time. Students MUST implement retry logic.
"""

import os
import ast
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helper: Get repository root
# ---------------------------------------------------------------------------
def get_repo_root():
    """Find the repository root by looking for .github folder."""
    current = Path(__file__).parent.parent
    if (current / ".github").exists():
        return current
    return current


REPO_ROOT = get_repo_root()


# ---------------------------------------------------------------------------
# Test 2.1: DHT22 Script Exists (5 points)
# ---------------------------------------------------------------------------
def test_dht22_script_exists():
    """
    Verify that dht22.py exists in the repository.

    Expected: dht22.py file present

    Suggestion: Create dht22.py with your DHT22 sensor reading code.
    """
    script_path = REPO_ROOT / "dht22.py"

    assert script_path.exists(), (
        f"\n\n"
        f"Expected: dht22.py file in repository root\n"
        f"Actual: File not found at {script_path}\n\n"
        f"Suggestion: Create dht22.py with your DHT22 sensor code.\n"
    )


# ---------------------------------------------------------------------------
# Test 2.2: DHT22 Script Syntax (5 points)
# ---------------------------------------------------------------------------
def test_dht22_script_syntax():
    """
    Verify that dht22.py has valid Python syntax.

    Expected: Python code that compiles without SyntaxError

    Suggestion: Run 'python3 -m py_compile dht22.py' locally.
    """
    script_path = REPO_ROOT / "dht22.py"

    if not script_path.exists():
        pytest.skip("dht22.py not found")

    content = script_path.read_text()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(
            f"\n\n"
            f"Expected: Valid Python syntax\n"
            f"Actual: SyntaxError on line {e.lineno}: {e.msg}\n\n"
            f"Suggestion: Check line {e.lineno} for syntax errors.\n"
        )


# ---------------------------------------------------------------------------
# Test 2.3: Adafruit DHT Import (5 points)
# ---------------------------------------------------------------------------
def test_adafruit_dht_import():
    """
    Verify that dht22.py imports the required Adafruit libraries.

    Expected: 'import board' and 'adafruit_dht'

    Suggestion: Add these imports at the top of your script:
        import board
        import adafruit_dht
    """
    script_path = REPO_ROOT / "dht22.py"

    if not script_path.exists():
        pytest.skip("dht22.py not found")

    content = script_path.read_text()

    missing = []
    if "import board" not in content and "from board" not in content:
        missing.append("board")
    if "adafruit_dht" not in content:
        missing.append("adafruit_dht")

    if missing:
        pytest.fail(
            f"\n\n"
            f"Expected: Required imports for DHT22 sensor\n"
            f"Actual: Missing imports: {', '.join(missing)}\n\n"
            f"Suggestion: Add these imports at the top of dht22.py:\n"
            f"  import board\n"
            f"  import adafruit_dht\n"
        )


# ---------------------------------------------------------------------------
# Test 2.4: DHT22 Sensor Creation (5 points)
# ---------------------------------------------------------------------------
def test_dht22_sensor_creation():
    """
    Verify that the script creates a DHT22 sensor object.

    Expected: adafruit_dht.DHT22(board.D4) or similar

    Suggestion: Create the sensor object:
        dht = adafruit_dht.DHT22(board.D4)
    """
    script_path = REPO_ROOT / "dht22.py"

    if not script_path.exists():
        pytest.skip("dht22.py not found")

    content = script_path.read_text()

    has_dht22 = any([
        "DHT22(" in content,
        "DHT11(" in content,  # Accept DHT11 as well
        "adafruit_dht." in content,
    ])

    if not has_dht22:
        pytest.fail(
            f"\n\n"
            f"Expected: DHT22 sensor object creation\n"
            f"Actual: No DHT22/DHT11 sensor creation found\n\n"
            f"Suggestion: Create the sensor object:\n"
            f"  import adafruit_dht\n"
            f"  import board\n"
            f"  dht = adafruit_dht.DHT22(board.D4)  # GPIO 4\n"
        )


# ---------------------------------------------------------------------------
# Test 2.5: CRITICAL - Retry Logic Implementation (10 points)
# ---------------------------------------------------------------------------
def test_dht22_retry_logic():
    """
    CRITICAL: Verify that DHT22 code includes retry logic.

    Expected: A loop with try/except that retries on RuntimeError

    WHY THIS MATTERS:
    The DHT22 uses a timing-sensitive one-wire protocol that NORMALLY
    fails 10-20% of the time. This is NOT a bug - it's how the sensor works.
    Professional code MUST implement retry logic.

    Suggestion: Implement retry like this:
        for attempt in range(5):
            try:
                temperature = dht.temperature
                humidity = dht.humidity
                break
            except RuntimeError as e:
                print(f"Retry {attempt + 1}/5: {e}")
                time.sleep(2)
    """
    script_path = REPO_ROOT / "dht22.py"

    if not script_path.exists():
        pytest.skip("dht22.py not found")

    content = script_path.read_text()

    # Check for retry patterns
    has_loop = any([
        "for " in content and "range(" in content,
        "while " in content,
    ])

    has_try_except = "try:" in content and "except" in content

    has_runtime_error = any([
        "RuntimeError" in content,
        "Exception" in content,
    ])

    has_retry_indicator = any([
        "retry" in content.lower(),
        "attempt" in content.lower(),
        "essai" in content.lower(),  # French
        "max_" in content.lower(),
        "range(3)" in content,
        "range(5)" in content,
        "range(10)" in content,
    ])

    # We need: loop + try/except + some retry indicator
    if not (has_loop and has_try_except and (has_runtime_error or has_retry_indicator)):
        pytest.fail(
            f"\n\n"
            f"CRITICAL: DHT22 retry logic not detected!\n\n"
            f"Expected: Loop with try/except to handle DHT22 read failures\n"
            f"Actual: Found loop={has_loop}, try/except={has_try_except}, "
            f"error handling={has_runtime_error or has_retry_indicator}\n\n"
            f"WHY THIS MATTERS:\n"
            f"  The DHT22 protocol is timing-sensitive and NORMALLY fails\n"
            f"  10-20% of the time. This is NOT a bug - it's how the sensor works.\n"
            f"  Professional code MUST implement retry logic.\n\n"
            f"Suggestion: Implement retry pattern:\n"
            f"  MAX_RETRIES = 5\n"
            f"  for attempt in range(MAX_RETRIES):\n"
            f"      try:\n"
            f"          temperature = dht.temperature\n"
            f"          humidity = dht.humidity\n"
            f"          if temperature is not None:\n"
            f"              break  # Success!\n"
            f"      except RuntimeError as e:\n"
            f"          print(f\"Retry {{attempt + 1}}/{{MAX_RETRIES}}: {{e}}\")\n"
            f"          time.sleep(2)  # DHT22 needs 2s between reads\n"
        )


# ---------------------------------------------------------------------------
# Test 2.6: DHT22 Markers Present (5 points)
# ---------------------------------------------------------------------------
def test_dht22_markers_exist():
    """
    Verify that DHT22 local tests were executed.

    Expected: .test_markers/dht22_script_verified.txt

    Suggestion: Run validate_pi.py on your Raspberry Pi.
    """
    markers_dir = REPO_ROOT / ".test_markers"

    if not markers_dir.exists():
        pytest.skip("No .test_markers/ directory")

    dht_marker = markers_dir / "dht22_script_verified.txt"

    if not dht_marker.exists():
        existing = [f.name for f in markers_dir.glob("*.txt")]
        pytest.fail(
            f"\n\n"
            f"Expected: dht22_script_verified.txt marker\n"
            f"Actual: Found markers: {existing}\n\n"
            f"Suggestion: Run validate_pi.py to generate DHT22 markers.\n"
        )
