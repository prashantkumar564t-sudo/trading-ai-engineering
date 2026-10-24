"""Baseline verification test for project structure, syntax, and documentation."""

import subprocess
from pathlib import Path
import py_compile
import sys
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.verify import (
    CheckResult,
    DEFAULT_SUBPROCESS_TIMEOUT,
    assess_platform_compatibility,
    check_environment,
    check_git_whitespace,
    check_working_tree,
    evaluate_checks,
    run_command,
    run_pytest_suite,
    summarize_checks,
)


def get_repo_root() -> Path:
    """Return the absolute path to the repository root directory."""
    return Path(__file__).resolve().parent.parent


EXPECTED_DOCUMENTATION_FILES = [
    Path("README.md"),
    Path("docs") / "principles.md",
    Path("docs") / "verification.md",
    Path(".gitignore"),
    Path("AGENTS.md"),
    Path(".agents") / "rules" / "engineering-standards.md",
]

EXPECTED_DIRECTORIES = [
    Path(".agents") / "rules",
    Path("docs"),
    Path("scripts"),
    Path("tests"),
]


def get_project_python_files() -> list[Path]:
    """Discover all project-owned Python files while excluding caches and environments."""
    root = get_repo_root()
    excluded_parts = {
        ".git",
        ".pytest_cache",
        "__pycache__",
        ".venv",
        "venv",
        "env",
        ".tox",
        ".nox",
    }
    python_files = []
    for path in root.rglob("*.py"):
        rel_parts = path.relative_to(root).parts
        if any(part in excluded_parts for part in rel_parts):
            continue
        python_files.append(path)
    return sorted(python_files)


@pytest.mark.parametrize("rel_path", EXPECTED_DOCUMENTATION_FILES)
def test_baseline_files_exist_and_non_empty(rel_path: Path):
    """Verify that expected baseline documentation files exist and contain content."""
    root = get_repo_root()
    target_file = root / rel_path

    assert target_file.exists(), f"Expected file does not exist: {rel_path}"
    assert target_file.is_file(), f"Expected path to be a regular file: {rel_path}"
    assert target_file.stat().st_size > 0, f"Expected file to be non-empty: {rel_path}"


@pytest.mark.parametrize("rel_dir", EXPECTED_DIRECTORIES)
def test_baseline_directories_exist(rel_dir: Path):
    """Verify that expected directories exist in the project structure."""
    root = get_repo_root()
    target_dir = root / rel_dir

    assert target_dir.exists(), f"Expected directory does not exist: {rel_dir}"
    assert target_dir.is_dir(), f"Expected path to be a directory: {rel_dir}"


@pytest.mark.parametrize(
    "py_file",
    get_project_python_files(),
    ids=lambda p: str(p.relative_to(get_repo_root())),
)
def test_python_syntax_compilation(py_file: Path, tmp_path: Path):
    """Verify that project Python files compile cleanly without syntax errors."""
    target_pyc = tmp_path / f"{py_file.stem}_compiled.pyc"
    try:
        py_compile.compile(str(py_file), cfile=str(target_pyc), doraise=True)
    except py_compile.PyCompileError as exc:
        pytest.fail(f"Syntax compilation error in {py_file}: {exc}")


@pytest.mark.parametrize("rel_path", EXPECTED_DOCUMENTATION_FILES)
def test_documentation_files_are_valid_utf8(rel_path: Path):
    """Verify that all project documentation and instruction files decode cleanly as UTF-8."""
    root = get_repo_root()
    target_file = root / rel_path

    assert target_file.exists(), f"Target file does not exist: {rel_path}"
    try:
        content = target_file.read_text(encoding="utf-8", errors="strict")
        assert len(content) > 0, f"Expected non-empty content in: {rel_path}"
    except UnicodeDecodeError as exc:
        pytest.fail(f"UTF-8 decoding failure in {rel_path}: {exc}")


@pytest.mark.parametrize(
    "checks,expected_outcome,expected_exit",
    [
        (
            [
                CheckResult("req1", "PASSED", "ok", 0, is_required=True),
                CheckResult("req2", "PASSED", "ok", 0, is_required=True),
                CheckResult("opt1", "UNTESTED", "info", None, is_required=False),
            ],
            "PASSED",
            0,
        ),
        (
            [
                CheckResult("req1", "FAILED", "err", 1, is_required=True),
                CheckResult("req2", "PASSED", "ok", 0, is_required=True),
            ],
            "FAILED",
            1,
        ),
        (
            [
                CheckResult("req1", "PASSED", "ok", 0, is_required=True),
                CheckResult("opt1", "FAILED", "opt err", 1, is_required=False),
            ],
            "PASSED",
            0,
        ),
        (
            [
                CheckResult("req1", "SKIPPED", "skip", 0, is_required=True),
                CheckResult("req2", "PASSED", "ok", 0, is_required=True),
            ],
            "FAILED",
            1,
        ),
        (
            [
                CheckResult("req1", "UNTESTED", "untested", None, is_required=True),
                CheckResult("req2", "PASSED", "ok", 0, is_required=True),
            ],
            "FAILED",
            1,
        ),
        (
            [],
            "FAILED",
            1,
        ),
    ],
    ids=[
        "all_required_passed",
        "required_failed",
        "optional_failed_required_passed",
        "required_skipped_fails_overall",
        "required_untested_fails_overall",
        "empty_input_fails_conservatively",
    ],
)
def test_verification_aggregation_outcomes(checks, expected_outcome, expected_exit):
    """Verify that evaluate_checks enforces strict pass requirements for required checks."""
    outcome, exit_code = evaluate_checks(checks)
    assert outcome == expected_outcome
    assert exit_code == expected_exit


def test_run_command_decodes_valid_utf8():
    """Verify that run_command preserves valid UTF-8 output including non-ASCII characters."""
    repo_root = get_repo_root()
    test_str = "UTF-8 verified: 成功 ✔ — Greek: αβγ — Accents: café"
    code = f"import sys; sys.stdout.buffer.write({test_str.encode('utf-8')!r})"
    proc = run_command([sys.executable, "-c", code], cwd=repo_root)
    assert proc.returncode == 0
    assert proc.stdout == test_str


def test_run_command_replaces_malformed_utf8_bytes():
    """Verify that run_command safely replaces malformed UTF-8 bytes with replacement character."""
    repo_root = get_repo_root()
    code = "import sys; sys.stdout.buffer.write(b'prefix ' + bytes([0xff, 0xfe]) + b' suffix')"
    proc = run_command([sys.executable, "-c", code], cwd=repo_root)
    assert proc.returncode == 0
    assert proc.stdout == "prefix \ufffd\ufffd suffix"


@pytest.mark.parametrize(
    "checks,expected_summary",
    [
        (
            [
                CheckResult("req1", "PASSED", "ok", 0, is_required=True),
                CheckResult("req2", "PASSED", "ok", 0, is_required=True),
                CheckResult("opt1", "UNTESTED", "info", None, is_required=False),
            ],
            {
                "passed_required": 2,
                "failed_required": 0,
                "incomplete_required": 0,
                "failed_optional": 0,
                "skipped_total": 0,
                "untested_total": 1,
            },
        ),
        (
            [
                CheckResult("req1", "PASSED", "ok", 0, is_required=True),
                CheckResult("req2", "SKIPPED", "skip", 0, is_required=True),
                CheckResult("opt1", "FAILED", "opt err", 1, is_required=False),
            ],
            {
                "passed_required": 1,
                "failed_required": 0,
                "incomplete_required": 1,
                "failed_optional": 1,
                "skipped_total": 1,
                "untested_total": 0,
            },
        ),
        (
            [
                CheckResult("req1", "FAILED", "err", 1, is_required=True),
                CheckResult("req2", "UNTESTED", "untested req", None, is_required=True),
                CheckResult("opt1", "UNTESTED", "untested opt", None, is_required=False),
            ],
            {
                "passed_required": 0,
                "failed_required": 1,
                "incomplete_required": 1,
                "failed_optional": 0,
                "skipped_total": 0,
                "untested_total": 2,
            },
        ),
        (
            [],
            {
                "passed_required": 0,
                "failed_required": 0,
                "incomplete_required": 0,
                "failed_optional": 0,
                "skipped_total": 0,
                "untested_total": 0,
            },
        ),
    ],
    ids=[
        "all_required_passed_with_optional_untested",
        "required_skipped_and_optional_failed",
        "required_failed_and_untested",
        "empty_input",
    ],
)
def test_summarize_checks_categorization(checks, expected_summary):
    """Verify that summarize_checks accurately categorizes required and optional checks."""
    summary = summarize_checks(checks)
    assert summary == expected_summary


def test_check_git_whitespace_skips_when_not_git_repo(tmp_path: Path):
    """Verify check_git_whitespace returns SKIPPED when directory is not a Git repository."""
    result = check_git_whitespace(tmp_path)
    assert result.status == "SKIPPED"
    assert result.is_required is False
    assert result.exit_code == 0
    assert "not a Git repository" in result.details


def test_assess_platform_compatibility_non_termux_environment(
    monkeypatch: pytest.MonkeyPatch,
):
    """Verify assess_platform_compatibility marks Termux as UNTESTED when not in Termux environment."""
    monkeypatch.setattr(sys, "prefix", "/standard/python/prefix")
    monkeypatch.delenv("TERMUX_VERSION", raising=False)
    monkeypatch.setenv("PATH", "/usr/bin:/bin")

    results = assess_platform_compatibility()
    host_check = next(c for c in results if "Host Environment" in c.name)
    assert host_check.status == "PASSED"
    assert host_check.is_required is True

    termux_check = next(c for c in results if "Android Termux" in c.name)
    assert termux_check.name == "Android Termux Target"
    assert termux_check.status == "UNTESTED"
    assert termux_check.is_required is False
    assert termux_check.exit_code is None
    assert "Host platform is not Android Termux" in termux_check.details


@pytest.mark.parametrize(
    "setup_termux_env",
    [
        lambda mp: mp.setenv("TERMUX_VERSION", "0.118.0"),
        lambda mp: mp.setattr(sys, "prefix", "/data/data/com.termux/files/usr"),
        lambda mp: mp.setenv("PATH", "/data/data/com.termux/files/usr/bin:/bin"),
    ],
    ids=["termux_version_env", "termux_sys_prefix", "termux_path_env"],
)
def test_assess_platform_compatibility_termux_environment_detection(
    monkeypatch: pytest.MonkeyPatch, setup_termux_env
):
    """Verify assess_platform_compatibility reports environment detection when Termux is detected."""
    monkeypatch.setattr(sys, "prefix", "/standard/python/prefix")
    monkeypatch.delenv("TERMUX_VERSION", raising=False)
    monkeypatch.setenv("PATH", "/usr/bin:/bin")

    setup_termux_env(monkeypatch)

    results = assess_platform_compatibility()
    host_check = next(c for c in results if "Host Environment" in c.name)
    assert host_check.status == "PASSED"
    assert host_check.is_required is True

    termux_check = next(c for c in results if "Android Termux" in c.name)
    assert termux_check.name == "Android Termux Environment Detection"
    assert termux_check.status == "PASSED"
    assert termux_check.is_required is False
    assert termux_check.exit_code == 0
    assert "detection only" in termux_check.details.lower()


def test_run_command_raises_timeout_expired():
    """Verify that run_command raises subprocess.TimeoutExpired on a short timeout."""
    repo_root = get_repo_root()
    code = "import time; time.sleep(1.0)"
    with pytest.raises(subprocess.TimeoutExpired) as exc_info:
        run_command([sys.executable, "-c", code], cwd=repo_root, timeout=0.05)
    assert exc_info.value.timeout == 0.05


@pytest.mark.parametrize(
    "stdout_payload,stderr_payload,expected_out_snippet,expected_err_snippet",
    [
        ("test_item PASSED\ntest_item2 RUNNING", "warning emitted", "test_item PASSED", "warning emitted"),
        (b"bytes stdout \xff item", b"bytes stderr", "bytes stdout \ufffd item", "bytes stderr"),
        (None, None, "", ""),
    ],
    ids=["string_streams", "bytes_streams", "none_streams"],
)
def test_run_pytest_suite_handles_timeout(
    tmp_path: Path,
    stdout_payload,
    stderr_payload,
    expected_out_snippet,
    expected_err_snippet,
):
    """Verify run_pytest_suite converts TimeoutExpired into a failed required check with diagnostics."""
    from unittest.mock import patch

    timeout_exc = subprocess.TimeoutExpired(
        cmd=["pytest", "tests/"],
        timeout=30.0,
        output=stdout_payload,
        stderr=stderr_payload,
    )

    with patch("scripts.verify.run_command", side_effect=timeout_exc):
        result = run_pytest_suite(tmp_path)

    assert result.status == "FAILED"
    assert result.is_required is True
    assert result.exit_code == 1
    assert "timed out after 30.0 seconds" in result.details
    if expected_out_snippet:
        assert expected_out_snippet in result.details
    if expected_err_snippet:
        assert expected_err_snippet in result.details


def test_check_git_whitespace_handles_timeout(tmp_path: Path):
    """Verify check_git_whitespace converts TimeoutExpired into a failed required check."""
    from unittest.mock import patch

    (tmp_path / ".git").mkdir()

    timeout_exc = subprocess.TimeoutExpired(
        cmd=["git", "diff", "--check"],
        timeout=15.0,
    )

    with patch("scripts.verify.run_command", side_effect=timeout_exc):
        result = check_git_whitespace(tmp_path)

    assert result.status == "FAILED"
    assert result.is_required is True
    assert result.exit_code == 1
    assert "timed out after 15.0 seconds" in result.details


def test_check_environment_and_working_tree_handle_timeout(tmp_path: Path):
    """Verify informational helpers handle TimeoutExpired cleanly without crashing."""
    from unittest.mock import patch

    timeout_exc = subprocess.TimeoutExpired(cmd=["git"], timeout=10.0)

    with patch("scripts.verify.run_command", side_effect=timeout_exc):
        env_info = check_environment(tmp_path)
        assert "timed out after 10.0s" in env_info["Git Version"]

        state, details = check_working_tree(tmp_path)
        assert state == "Unavailable"
        assert "timed out after 10.0s" in details
