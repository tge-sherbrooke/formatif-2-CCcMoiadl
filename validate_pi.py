#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["adafruit-circuitpython-dht", "adafruit-blinka", "RPi.GPIO"]
# ///
"""
Local Hardware Validation for Formatif F2
==========================================

Run this script ON YOUR RASPBERRY PI to validate hardware setup.
It creates marker files that GitHub Actions will verify.

Usage:
    python3 validate_pi.py

The script will:
1. Verify LED scripts exist and have valid syntax
2. Verify DHT22 script exists and has RETRY LOGIC
3. Check Git setup
4. Create marker files for GitHub Actions

After running successfully, commit and push the .test_markers/ folder.
"""

import os
import sys
import ast
import subprocess
from pathlib import Path
from datetime import datetime


# ---------------------------------------------------------------------------
# Terminal Colors
# ---------------------------------------------------------------------------
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def success(msg):
    print(f"{Colors.GREEN}[PASS] {msg}{Colors.END}")


def fail(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.END}")


def warn(msg):
    print(f"{Colors.YELLOW}[WARN] {msg}{Colors.END}")


def info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.END}")


def header(msg):
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f" {msg}")
    print(f"{'='*60}{Colors.END}\n")


# ---------------------------------------------------------------------------
# Marker Management
# ---------------------------------------------------------------------------
MARKERS_DIR = Path(__file__).parent / ".test_markers"


def create_marker(name, content):
    """Create a marker file for GitHub Actions verification."""
    MARKERS_DIR.mkdir(exist_ok=True)
    marker_path = MARKERS_DIR / f"{name}.txt"
    timestamp = datetime.now().isoformat()
    marker_path.write_text(f"Verified: {timestamp}\n{content}\n")
    info(f"Marker created: {marker_path.name}")


# ---------------------------------------------------------------------------
# Test: LED Scripts
# ---------------------------------------------------------------------------
def check_led_scripts():
    """Verify LED control scripts."""
    header("LED SCRIPTS VERIFICATION")

    script_path = Path(__file__).parent / "led_simple.py"

    if not script_path.exists():
        fail("led_simple.py not found")
        print("\n  Create led_simple.py with your LED control code.")
        return False

    success("led_simple.py exists")

    # Check syntax
    content = script_path.read_text()
    try:
        ast.parse(content)
        success("Python syntax is valid")
    except SyntaxError as e:
        fail(f"Syntax error on line {e.lineno}: {e.msg}")
        return False

    # Check for GPIO usage
    if "GPIO" not in content:
        fail("No GPIO usage found in led_simple.py")
        print("\n  Add: import RPi.GPIO as GPIO")
        return False

    success("RPi.GPIO import found")

    # Check led_rgb.py (optional)
    rgb_path = Path(__file__).parent / "led_rgb.py"
    if rgb_path.exists():
        success("led_rgb.py found (bonus)")
        try:
            ast.parse(rgb_path.read_text())
            success("led_rgb.py syntax valid")
        except SyntaxError as e:
            warn(f"led_rgb.py syntax error line {e.lineno}")

    create_marker("led_scripts_verified", "LED scripts validated")
    return True


# ---------------------------------------------------------------------------
# Test: DHT22 Script with Retry Logic
# ---------------------------------------------------------------------------
def check_dht22_script():
    """Verify DHT22 script with MANDATORY retry logic."""
    header("DHT22 SCRIPT VERIFICATION")

    script_path = Path(__file__).parent / "dht22.py"

    if not script_path.exists():
        fail("dht22.py not found")
        print("\n  Create dht22.py with your DHT22 sensor code.")
        return False

    success("dht22.py exists")

    # Check syntax
    content = script_path.read_text()
    try:
        ast.parse(content)
        success("Python syntax is valid")
    except SyntaxError as e:
        fail(f"Syntax error on line {e.lineno}: {e.msg}")
        return False

    # Check for required imports
    if "board" not in content or "adafruit_dht" not in content:
        fail("Missing required imports (board, adafruit_dht)")
        print("\n  Add these imports:")
        print("    import board")
        print("    import adafruit_dht")
        return False

    success("Required imports found")

    # CRITICAL: Check for retry logic
    has_loop = ("for " in content and "range(" in content) or "while " in content
    has_try_except = "try:" in content and "except" in content

    if not has_loop:
        fail("CRITICAL: No retry loop found!")
        print("\n" + "="*60)
        print("  IMPORTANT: DHT22 ERRORS ARE NORMAL!")
        print("="*60)
        print("\n  The DHT22 uses a timing-sensitive protocol that NORMALLY")
        print("  fails 10-20% of the time. This is NOT a bug.")
        print("\n  You MUST implement retry logic:")
        print("    for attempt in range(5):")
        print("        try:")
        print("            temperature = dht.temperature")
        print("            humidity = dht.humidity")
        print("            break")
        print("        except RuntimeError as e:")
        print("            print(f'Retry {attempt + 1}: {e}')")
        print("            time.sleep(2)")
        return False

    if not has_try_except:
        fail("CRITICAL: No try/except error handling found!")
        print("\n  DHT22 throws RuntimeError on read failures.")
        print("  Wrap your reading code in try/except.")
        return False

    success("Retry logic detected - GOOD!")
    info("DHT22 errors are normal. Your retry pattern will handle them.")

    create_marker("dht22_script_verified", "DHT22 script with retry logic validated")
    return True


# ---------------------------------------------------------------------------
# Test: Git Setup
# ---------------------------------------------------------------------------
def check_git_setup():
    """Verify basic Git configuration."""
    header("GIT VERIFICATION")

    try:
        # Check if we're in a git repo
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, text=True, timeout=5,
            cwd=str(Path(__file__).parent)
        )

        if result.returncode != 0:
            warn("Not in a git repository")
            return True  # Non-blocking

        success("Git repository detected")

        # Check for commits
        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True, text=True, timeout=5,
            cwd=str(Path(__file__).parent)
        )

        commits = [c for c in result.stdout.strip().split("\n") if c]
        info(f"Found {len(commits)} recent commits")

        # Check git config
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            success(f"Git user: {result.stdout.strip()}")
        else:
            warn("Git user.name not configured")
            print("  Run: git config --global user.name 'Your Name'")

        create_marker("git_verified", f"Git setup verified, {len(commits)} commits")
        return True

    except subprocess.TimeoutExpired:
        warn("Git command timed out")
        return True
    except FileNotFoundError:
        warn("Git not installed")
        return True


# ---------------------------------------------------------------------------
# Test: Hardware (Optional)
# ---------------------------------------------------------------------------
def check_hardware():
    """Test actual hardware if on Raspberry Pi."""
    header("HARDWARE TEST (Optional)")

    # Check if we're on a Raspberry Pi
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
            is_rpi = 'Raspberry Pi' in cpuinfo or 'Broadcom' in cpuinfo
    except:
        is_rpi = False

    if not is_rpi:
        warn("Not on Raspberry Pi - hardware tests skipped")
        info("This is OK for development. Run on Pi for full validation.")
        return True

    success("Raspberry Pi detected")

    # Test LED (if possible)
    info("LED hardware test requires manual verification")
    info("  - Connect LED to GPIO 17 (or your chosen pin)")
    info("  - Run your led_simple.py to verify")

    # Test DHT22 (if possible)
    info("DHT22 hardware test:")
    info("  - Connect DHT22 to GPIO 4 with 10K pull-up resistor")
    info("  - Run your dht22.py to verify (expect some retries!)")

    create_marker("hardware_checked", "Hardware check completed")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print(f"\n{Colors.BOLD}Formatif F2 - Local Hardware Validation{Colors.END}")
    print(f"{'='*60}\n")

    results = {}

    # Run all checks
    results["LED Scripts"] = check_led_scripts()
    results["DHT22 Script"] = check_dht22_script()
    results["Git Setup"] = check_git_setup()
    results["Hardware"] = check_hardware()

    # Summary
    header("FINAL RESULTS")

    # LED and DHT22 are required, Git and Hardware are helpful
    required_passed = results["LED Scripts"] and results["DHT22 Script"]

    for test, passed in results.items():
        if passed:
            success(f"{test}: OK")
        else:
            fail(f"{test}: FAILED")

    print()

    if required_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}")
        print("=" * 60)
        print(" ALL REQUIRED TESTS PASSED!")
        print("=" * 60)
        print(f"{Colors.END}")

        create_marker("all_tests_passed", "All validations completed")

        print("\nNext steps:")
        print("  git add .test_markers/")
        print("  git commit -m \"validation locale completee\"")
        print("  git push")
        print("\nRemember: You can push as many times as needed!")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}")
        print("=" * 60)
        print(" SOME TESTS FAILED - Fix issues and run again")
        print("=" * 60)
        print(f"{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
