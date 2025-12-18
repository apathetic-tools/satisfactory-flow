"""Data loading utilities with user override support.

This module provides functions to load data files from the package's default
data directory, with optional user overrides in a user data directory.
"""

import logging
from collections.abc import Iterator
from importlib import resources
from pathlib import Path

from platformdirs import user_data_dir


logger = logging.getLogger(__name__)


def get_data_dir() -> Path:
    """Get the package's default data directory.

    Returns:
        Path to the data directory bundled with the package.
    """
    # Use importlib.resources for accessing package data
    # This works both in development and when installed
    try:
        # Python 3.9+: files() returns a Traversable
        data_files = resources.files("satflow") / "data"
        if data_files.is_dir():
            return Path(str(data_files))
    except (ModuleNotFoundError, TypeError):
        # Fallback: construct path relative to package
        pass

    # Fallback: assume we're in development mode
    package_dir = Path(__file__).parent
    return package_dir / "data"


def get_user_data_dir() -> Path:
    """Get the user's data directory for overrides.

    Returns:
        Path to the user data directory (platform-specific).
    """
    return Path(user_data_dir("satflow", "Apathetic Tools"))


def find_data_file(filename: str, *, allow_user_override: bool = True) -> Path | None:
    """Find a data file, checking user override first if enabled.

    Search order:
    1. User data directory (if allow_user_override=True and file exists)
    2. Package data directory

    Args:
        filename: Name of the data file to find (relative path within data/).
        allow_user_override: If True, check user data directory first.

    Returns:
        Path to the data file, or None if not found.
    """
    # Normalize filename (remove leading slashes, handle subdirectories)
    filename = filename.lstrip("/")

    # Check user override first
    if allow_user_override:
        user_data_dir = get_user_data_dir()
        user_path = user_data_dir / filename
        if user_path.exists():
            logger.debug("Using user override: %s", user_path)
            return user_path

    # Fall back to package data
    package_data_dir = get_data_dir()
    package_path = package_data_dir / filename
    if package_path.exists():
        return package_path

    return None


def get_data_file(filename: str, *, allow_user_override: bool = True) -> Path:
    """Get a data file, raising an error if not found.

    Args:
        filename: Name of the data file to get (relative path within data/).
        allow_user_override: If True, check user data directory first.

    Returns:
        Path to the data file.

    Raises:
        FileNotFoundError: If the data file is not found in either location.
    """
    path = find_data_file(filename, allow_user_override=allow_user_override)
    if path is None:
        msg = f"Data file not found: {filename}"
        raise FileNotFoundError(msg)
    return path


def list_data_files(pattern: str = "*") -> Iterator[Path]:
    """List all data files in the package data directory.

    Args:
        pattern: Glob pattern to match files (default: "*" for all files).

    Yields:
        Paths to data files in the package data directory.
    """
    data_dir = get_data_dir()
    if data_dir.exists():
        yield from data_dir.rglob(pattern)
