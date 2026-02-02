#!/usr/bin/env python3
"""
Milestone 3: Git Workflow (40 points)
=====================================

This milestone verifies that the student has:
1. Used basic Git commands (clone, add, commit, push)
2. Written meaningful commit messages
3. Completed all local tests

Note: Per CONTEXT.md, week 2 focuses on basic Git (clone/add/commit/push).
No branches or commit conventions required yet.
"""

import os
import ast
import subprocess
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
# Test 3.1: Multiple Commits (10 points)
# ---------------------------------------------------------------------------
def test_multiple_commits():
    """
    Verify that the student has made multiple commits.

    Expected: At least 2 commits beyond the initial template

    Suggestion: Make separate commits for different changes:
        git add led_simple.py
        git commit -m "add LED control script"
        git add dht22.py
        git commit -m "add DHT22 sensor script"
    """
    try:
        result = subprocess.run(
            ["git", "log", "--oneline"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(REPO_ROOT)
        )

        if result.returncode != 0:
            pytest.skip("Not a git repository or git not available")

        commits = [line for line in result.stdout.strip().split("\n") if line]
        commit_count = len(commits)

        if commit_count < 2:
            pytest.fail(
                f"\n\n"
                f"Expected: At least 2 commits\n"
                f"Actual: {commit_count} commit(s) found\n\n"
                f"Suggestion: Make commits for your work:\n"
                f"  git add led_simple.py\n"
                f"  git commit -m \"add LED control script\"\n"
                f"  git add dht22.py\n"
                f"  git commit -m \"add DHT22 sensor script\"\n"
            )

    except subprocess.TimeoutExpired:
        pytest.skip("Git command timed out")
    except FileNotFoundError:
        pytest.skip("Git not available")


# ---------------------------------------------------------------------------
# Test 3.2: Descriptive Commit Messages (10 points)
# ---------------------------------------------------------------------------
def test_descriptive_commit_messages():
    """
    Verify that commit messages are descriptive (not empty or generic).

    Expected: Commit messages with meaningful content

    Suggestion: Write descriptive messages:
        Good: "add LED control with GPIO setup"
        Bad:  "update" or "fix" alone
    """
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-10"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(REPO_ROOT)
        )

        if result.returncode != 0:
            pytest.skip("Git not available")

        commits = result.stdout.strip().split("\n")

        # Filter out very short/generic messages
        generic_messages = ["update", "fix", "test", "wip", ".", "...", "asdf"]
        problematic_commits = []

        for commit in commits:
            if not commit.strip():
                continue
            # Get message part (after hash)
            parts = commit.split(" ", 1)
            if len(parts) < 2:
                continue
            message = parts[1].lower().strip()

            # Check if message is too short or generic
            if len(message) < 3 or message in generic_messages:
                problematic_commits.append(commit)

        if problematic_commits and len(problematic_commits) > len(commits) / 2:
            pytest.fail(
                f"\n\n"
                f"Expected: Descriptive commit messages\n"
                f"Actual: Some messages are too short or generic:\n"
                f"  {problematic_commits[:3]}\n\n"
                f"Suggestion: Write meaningful commit messages:\n"
                f"  Good: \"add LED control with GPIO setup\"\n"
                f"  Good: \"implement DHT22 reading with retry\"\n"
                f"  Bad:  \"update\" or \"fix\" alone\n"
            )

    except subprocess.TimeoutExpired:
        pytest.skip("Git command timed out")
    except FileNotFoundError:
        pytest.skip("Git not available")


# ---------------------------------------------------------------------------
# Test 3.3: All Required Files Present (10 points)
# ---------------------------------------------------------------------------
def test_all_required_files():
    """
    Verify that all required files are in the repository.

    Expected: led_simple.py, dht22.py, .test_markers/

    Suggestion: Make sure you have created and committed all files.
    """
    missing = []

    if not (REPO_ROOT / "led_simple.py").exists():
        missing.append("led_simple.py")

    if not (REPO_ROOT / "dht22.py").exists():
        missing.append("dht22.py")

    if not (REPO_ROOT / ".test_markers").exists():
        missing.append(".test_markers/")

    if missing:
        pytest.fail(
            f"\n\n"
            f"Expected: All required files present\n"
            f"Actual: Missing: {', '.join(missing)}\n\n"
            f"Suggestion: Create missing files and run validate_pi.py:\n"
            f"  - led_simple.py: LED control script\n"
            f"  - dht22.py: DHT22 sensor reading script\n"
            f"  - .test_markers/: Created by validate_pi.py\n"
        )


# ---------------------------------------------------------------------------
# Test 3.4: All Local Tests Passed (10 points)
# ---------------------------------------------------------------------------
def test_all_local_tests_passed():
    """
    Verify that all local tests passed on Raspberry Pi.

    Expected: all_tests_passed.txt marker file

    Suggestion: Ensure validate_pi.py completes successfully.
    """
    markers_dir = REPO_ROOT / ".test_markers"

    if not markers_dir.exists():
        pytest.fail(
            f"\n\n"
            f"Expected: .test_markers/ directory\n"
            f"Actual: Directory not found\n\n"
            f"Suggestion: Run validate_pi.py on your Raspberry Pi.\n"
        )

    passed_marker = markers_dir / "all_tests_passed.txt"

    # Also accept if all individual markers exist
    led_marker = markers_dir / "led_scripts_verified.txt"
    dht_marker = markers_dir / "dht22_script_verified.txt"

    if passed_marker.exists():
        return  # Perfect!

    if led_marker.exists() and dht_marker.exists():
        return  # Also acceptable

    existing = [f.name for f in markers_dir.glob("*.txt")]
    pytest.fail(
        f"\n\n"
        f"Expected: all_tests_passed.txt (or led + dht markers)\n"
        f"Actual: Found markers: {existing}\n\n"
        f"Suggestion: Fix any failing tests and run validate_pi.py again:\n"
        f"  python3 validate_pi.py\n"
        f"\n"
        f"Then commit and push:\n"
        f"  git add .test_markers/\n"
        f"  git commit -m \"validation locale completee\"\n"
        f"  git push\n"
    )


# ---------------------------------------------------------------------------
# Test 3.5: LED RGB Script (Optional Bonus - 0 points but checked)
# ---------------------------------------------------------------------------
def test_led_rgb_script():
    """
    Check for optional LED RGB chenillard script (bonus).

    Expected: led_rgb.py with valid syntax (optional)

    Suggestion: Create led_rgb.py for bonus points.
    """
    script_path = REPO_ROOT / "led_rgb.py"

    if not script_path.exists():
        pytest.skip("led_rgb.py not found - this is optional bonus content")

    content = script_path.read_text()

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(
            f"\n\n"
            f"Expected: Valid Python syntax in led_rgb.py\n"
            f"Actual: SyntaxError on line {e.lineno}\n\n"
            f"Suggestion: Fix the syntax error in led_rgb.py.\n"
        )

    # Verify GPIO usage
    if "GPIO" not in content:
        pytest.fail(
            f"\n\n"
            f"Expected: GPIO usage in led_rgb.py\n"
            f"Actual: No GPIO reference found\n\n"
            f"Suggestion: led_rgb.py should control multiple LEDs.\n"
        )
