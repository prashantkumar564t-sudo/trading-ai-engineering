"""Baseline verification test for project structure and documentation."""

from pathlib import Path
import pytest


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
