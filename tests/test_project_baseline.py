"""Baseline verification test for project structure, syntax, and documentation."""

from pathlib import Path
import py_compile
import sys
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.verify import CheckResult, evaluate_checks


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
    Path(".agents") / "skills",
    Path("docs"),
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
