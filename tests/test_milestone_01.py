#!/usr/bin/env python3
"""
Milestone 1: LED Control (25 points)
=====================================

This milestone verifies that the student has:
1. Created LED control scripts
2. Used RPi.GPIO correctly
3. Run local tests on the Raspberry Pi

These tests run in GitHub Actions (no hardware access).
Hardware validation is done locally via validate_pi.py.
"""

import os
import ast
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
# Test 1.1: LED Simple Script Exists (5 points)
# ---------------------------------------------------------------------------
def test_led_simple_script_exists():
    """
    Verify that led_simple.py exists in the repository.

    Expected: led_simple.py file present

    Suggestion: Create a file named led_simple.py at the repository root.
    This script should control a simple LED on/off.
    """
    script_path = REPO_ROOT / "led_simple.py"

    assert script_path.exists(), (
        f"\n\n"
        f"Expected: led_simple.py file in repository root\n"
        f"Actual: File not found at {script_path}\n\n"
        f"Suggestion: Create led_simple.py with your LED control code.\n"
        f"Example:\n"
        f"  import RPi.GPIO as GPIO\n"
        f"  GPIO.setmode(GPIO.BCM)\n"
        f"  GPIO.setup(17, GPIO.OUT)\n"
    )


# ---------------------------------------------------------------------------
# Test 1.2: LED Simple Script Syntax (5 points)
# ---------------------------------------------------------------------------
def test_led_simple_script_syntax():
    """
    Verify that led_simple.py has valid Python syntax.

    Expected: Python code that compiles without SyntaxError

    Suggestion: Run 'python3 -m py_compile led_simple.py' locally.
    """
    script_path = REPO_ROOT / "led_simple.py"

    if not script_path.exists():
        pytest.skip("led_simple.py not found - skipping syntax check")

    content = script_path.read_text()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(
            f"\n\n"
            f"Expected: Valid Python syntax\n"
            f"Actual: SyntaxError on line {e.lineno}: {e.msg}\n\n"
            f"Suggestion: Check line {e.lineno} for:\n"
            f"  - Missing colons after 'if', 'for', 'def', 'class'\n"
            f"  - Unbalanced parentheses, brackets, or quotes\n"
            f"  - Incorrect indentation\n"
        )


# ---------------------------------------------------------------------------
# Test 1.3: RPi.GPIO Import (5 points)
# ---------------------------------------------------------------------------
def test_rpi_gpio_import():
    """
    Verify that led_simple.py imports RPi.GPIO.

    Expected: 'import RPi.GPIO' or 'from RPi import GPIO'

    Suggestion: Add this import at the top of your script:
        import RPi.GPIO as GPIO
    """
    script_path = REPO_ROOT / "led_simple.py"

    if not script_path.exists():
        pytest.skip("led_simple.py not found - skipping import check")

    content = script_path.read_text()

    has_gpio = any([
        "import RPi.GPIO" in content,
        "from RPi import GPIO" in content,
        "from RPi.GPIO" in content,
    ])

    if not has_gpio:
        pytest.fail(
            f"\n\n"
            f"Expected: RPi.GPIO import for LED control\n"
            f"Actual: No RPi.GPIO import found\n\n"
            f"Suggestion: Add this import at the top of led_simple.py:\n"
            f"  import RPi.GPIO as GPIO\n"
        )


# ---------------------------------------------------------------------------
# Test 1.4: GPIO Mode Configuration (5 points)
# ---------------------------------------------------------------------------
def test_gpio_mode_configuration():
    """
    Verify that the script sets GPIO mode (BCM or BOARD).

    Expected: GPIO.setmode(GPIO.BCM) or GPIO.setmode(GPIO.BOARD)

    Suggestion: Set the GPIO mode before using pins:
        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    """
    script_path = REPO_ROOT / "led_simple.py"

    if not script_path.exists():
        pytest.skip("led_simple.py not found")

    content = script_path.read_text()

    has_setmode = any([
        "GPIO.setmode" in content,
        "setmode(" in content,
    ])

    if not has_setmode:
        pytest.fail(
            f"\n\n"
            f"Expected: GPIO mode configuration (BCM or BOARD)\n"
            f"Actual: No GPIO.setmode() found\n\n"
            f"Suggestion: Set the numbering mode before using GPIO pins:\n"
            f"  GPIO.setmode(GPIO.BCM)   # BCM numbering (GPIO17, GPIO27...)\n"
            f"  # or\n"
            f"  GPIO.setmode(GPIO.BOARD)  # Physical pin numbers (pin 11...)\n"
            f"\n"
            f"We recommend GPIO.BCM for this course.\n"
        )


# ---------------------------------------------------------------------------
# Test 1.5: LED Control Tests Executed (5 points)
# ---------------------------------------------------------------------------
def test_led_markers_exist():
    """
    Verify that local LED tests were executed on Raspberry Pi.

    Expected: .test_markers/led_scripts_verified.txt

    Suggestion: On your Raspberry Pi, run:
        python3 validate_pi.py
    Then commit and push the .test_markers/ folder.
    """
    markers_dir = REPO_ROOT / ".test_markers"

    if not markers_dir.exists():
        pytest.fail(
            f"\n\n"
            f"Expected: .test_markers/ directory with local test results\n"
            f"Actual: Directory not found\n\n"
            f"Suggestion: Run local hardware validation on your Raspberry Pi:\n"
            f"  python3 validate_pi.py\n"
            f"\n"
            f"Then add the markers to git:\n"
            f"  git add .test_markers/\n"
            f"  git commit -m \"feat: validation locale executee\"\n"
            f"  git push\n"
        )

    led_marker = markers_dir / "led_scripts_verified.txt"

    if not led_marker.exists():
        existing = [f.name for f in markers_dir.glob("*.txt")]
        pytest.fail(
            f"\n\n"
            f"Expected: led_scripts_verified.txt marker\n"
            f"Actual: Found markers: {existing}\n\n"
            f"Suggestion: Run validate_pi.py again to generate LED markers.\n"
        )
