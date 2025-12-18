# Data Directory

This directory contains default data files used by the CLI.

## Structure

Place your data files here. They will be bundled with the package and available at runtime.

## User Overrides

Users can override any file in this directory by placing a file with the same name (and relative path) in their user data directory:

- **Linux**: `~/.local/share/satflow/`
- **macOS**: `~/Library/Application Support/satflow/`
- **Windows**: `%APPDATA%/satflow/`

The CLI will check for user overrides first, then fall back to the default files in this directory.

## Usage in Code

```python
from satflow.data import get_data_file, find_data_file

# Get a data file (raises FileNotFoundError if not found)
data_path = get_data_file("recipes.json")

# Find a data file (returns None if not found)
data_path = find_data_file("recipes.json")

# Disable user override checking
data_path = get_data_file("recipes.json", allow_user_override=False)
```

