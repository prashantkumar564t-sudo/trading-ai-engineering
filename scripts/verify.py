#!/usr/bin/env python3
"""Minimal, reusable verification orchestrator for project baselines.

Executes environment inspection, Git whitespace checks, working-tree status,
and the automated pytest suite, producing a standardized four-state evidence report.
"""

from dataclasses import dataclass
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Optional


def get_repo_root() -> Path:
    """Return the absolute path to the repository root directory."""
    return Path(__file__).resolve().parent.parent


@dataclass
class CheckResult:
    """Data container for an individual verification check."""

    name: str
    status: str  # "PASSED", "FAILED", "SKIPPED", "UNTESTED"
    details: str
    exit_code: Optional[int] = None
    is_required: bool = True


def run_command(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Execute a command safely without shell expansion."""
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        shell=False,
    )


def check_environment(repo_root: Path) -> dict[str, str]:
    """Collect environment information and Git version."""
    env_info = {
        "Python Version": f"{platform.python_version()} ({platform.architecture()[0]})",
        "Python Executable": sys.executable,
        "Platform": f"{platform.system()} {platform.release()} ({sys.platform})",
    }

    try:
        proc = run_command(["git", "--version"], cwd=repo_root)
        if proc.returncode == 0:
            env_info["Git Version"] = proc.stdout.strip()
        else:
            env_info["Git Version"] = f"Unavailable (git exited with code {proc.returncode})"
    except FileNotFoundError:
        env_info["Git Version"] = "Unavailable (git executable not found in PATH)"

    return env_info


def check_git_whitespace(repo_root: Path) -> CheckResult:
    """Run git diff --check on both unstaged and staged changes."""
    try:
        proc_unstaged = run_command(["git", "diff", "--check"], cwd=repo_root)
        proc_staged = run_command(["git", "diff", "--cached", "--check"], cwd=repo_root)

        has_unstaged_issues = proc_unstaged.returncode != 0
        has_staged_issues = proc_staged.returncode != 0

        if not has_unstaged_issues and not has_staged_issues:
            return CheckResult(
                name="Git Whitespace Check (unstaged & staged)",
                status="PASSED",
                details="No whitespace errors or conflict markers detected (unstaged and staged).",
                exit_code=0,
                is_required=True,
            )

        diagnostics = []
        exit_code = 0
        if has_unstaged_issues:
            err = proc_unstaged.stdout.strip() or proc_unstaged.stderr.strip()
            diagnostics.append(f"Unstaged changes (git diff --check):\n{err}")
            exit_code = proc_unstaged.returncode
        if has_staged_issues:
            err = proc_staged.stdout.strip() or proc_staged.stderr.strip()
            diagnostics.append(f"Staged changes (git diff --cached --check):\n{err}")
            if exit_code == 0:
                exit_code = proc_staged.returncode

        return CheckResult(
            name="Git Whitespace Check (unstaged & staged)",
            status="FAILED",
            details="\n\n".join(diagnostics),
            exit_code=exit_code,
            is_required=True,
        )
    except FileNotFoundError:
        return CheckResult(
            name="Git Whitespace Check (unstaged & staged)",
            status="FAILED",
            details="Git command unavailable in PATH.",
            exit_code=1,
            is_required=True,
        )


def check_working_tree(repo_root: Path) -> tuple[str, str]:
    """Inspect working tree status without marking it as a verification failure."""
    try:
        proc = run_command(["git", "status", "--porcelain"], cwd=repo_root)
        if proc.returncode == 0:
            output = proc.stdout.strip()
            if not output:
                return "Clean", "Working tree is completely clean (no uncommitted or untracked changes)."
            else:
                lines = output.splitlines()
                return "Modified / Untracked", f"Working tree contains {len(lines)} change(s):\n{output}"
        else:
            return "Unavailable", f"git status returned non-zero exit code: {proc.returncode}"
    except FileNotFoundError:
        return "Unavailable", "Git command unavailable in PATH."


def run_pytest_suite(repo_root: Path) -> CheckResult:
    """Run the pytest test suite using the current Python interpreter."""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    try:
        proc = run_command(cmd, cwd=repo_root)
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        combined_output = f"{stdout}\n{stderr}".strip() if stderr else stdout

        if proc.returncode == 0:
            summary_line = stdout.splitlines()[-1] if stdout else "Tests passed"
            return CheckResult(
                name="Automated Test Suite (pytest tests/ -v)",
                status="PASSED",
                details=f"{summary_line}\nCommand: {' '.join(cmd)}",
                exit_code=0,
                is_required=True,
            )
        else:
            return CheckResult(
                name="Automated Test Suite (pytest tests/ -v)",
                status="FAILED",
                details=f"pytest failed with exit code {proc.returncode}:\n{combined_output}",
                exit_code=proc.returncode,
                is_required=True,
            )
    except FileNotFoundError:
        return CheckResult(
            name="Automated Test Suite (pytest tests/ -v)",
            status="FAILED",
            details=f"Failed to invoke pytest using interpreter: {sys.executable}",
            exit_code=1,
            is_required=True,
        )


def assess_platform_compatibility() -> list[CheckResult]:
    """Assess and report platform verification states accurately."""
    results = []

    # Host platform check
    results.append(
        CheckResult(
            name=f"Host Environment ({sys.platform})",
            status="PASSED",
            details=f"Verified execution on {platform.system()} {platform.release()}",
            exit_code=0,
            is_required=True,
        )
    )

    # Android Termux check
    is_termux = (
        "com.termux" in sys.prefix
        or "TERMUX_VERSION" in os.environ
        or "/data/data/com.termux" in os.environ.get("PATH", "")
    )
    if is_termux:
        results.append(
            CheckResult(
                name="Android Termux Environment",
                status="PASSED",
                details="Termux environment identified on host. (Requires full test pass to confirm compatibility).",
                exit_code=0,
                is_required=False,
            )
        )
    else:
        results.append(
            CheckResult(
                name="Android Termux Target",
                status="UNTESTED",
                details="Host platform is not Android Termux. Compatibility must be verified on genuine hardware.",
                exit_code=None,
                is_required=False,
            )
        )

    return results


def main() -> int:
    """Main verification orchestrator routine."""
    repo_root = get_repo_root()
    print("=" * 70)
    print("           TRADING AI ENGINEERING - VERIFICATION AUDIT")
    print("=" * 70)
    print(f"Repository Root: {repo_root}\n")

    # A. Environment Information
    env_info = check_environment(repo_root)
    print("--- Environment Information ---")
    for key, value in env_info.items():
        print(f"  {key:<20}: {value}")
    print()

    # B. Working-Tree Information (Informational)
    tree_status, tree_details = check_working_tree(repo_root)
    print("--- Working-Tree Status (Informational) ---")
    print(f"  State: {tree_status}")
    for line in tree_details.splitlines():
        print(f"    {line}")
    print()

    # Checks collection
    checks: list[CheckResult] = []

    # C. Git Whitespace Check
    whitespace_result = check_git_whitespace(repo_root)
    checks.append(whitespace_result)

    # D. Automated Tests
    test_result = run_pytest_suite(repo_root)
    checks.append(test_result)

    # E. Platform Checks
    platform_results = assess_platform_compatibility()
    checks.extend(platform_results)

    # F. Report and Evaluation
    print("--- Verification Results ---")
    for chk in checks:
        print(f"  [{chk.status:<8}] {chk.name}")
        for dline in chk.details.splitlines():
            print(f"             {dline}")
    print()

    # Tally results
    passed_required = [c for c in checks if c.status == "PASSED" and c.is_required]
    failed_required = [c for c in checks if c.status == "FAILED" and c.is_required]
    skipped_checks = [c for c in checks if c.status == "SKIPPED"]
    untested_checks = [c for c in checks if c.status == "UNTESTED"]

    all_required_passed = len(failed_required) == 0

    print("=" * 70)
    print("                       VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"  Required Checks Passed : {len(passed_required)}")
    print(f"  Required Checks Failed : {len(failed_required)}")
    print(f"  Skipped Checks         : {len(skipped_checks)}")
    print(f"  Untested Capabilities  : {len(untested_checks)}")
    print("-" * 70)

    overall_outcome = "PASSED" if all_required_passed else "FAILED"
    print(f"  OVERALL OUTCOME        : {overall_outcome}")
    print("=" * 70)

    return 0 if all_required_passed else 1


if __name__ == "__main__":
    sys.exit(main())
