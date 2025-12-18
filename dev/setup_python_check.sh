#!/bin/bash
set -euo pipefail
# Check Python 3.14 availability for testing

echo "🔍 Checking Python 3.14 availability for testing..."
echo ""

PYTHON_310_FOUND=false
PYTHON_310_PATH=""

# First, check for system Python 3.14 (apt, etc.) - avoid mise-managed paths
# Check common system locations first
for POSSIBLE_PATH in /usr/bin/python3.14 /usr/local/bin/python3.14; do
  if [ -x "$POSSIBLE_PATH" ] && "$POSSIBLE_PATH" --version 2>&1 | grep -q "3.14"; then
    PYTHON_310_PATH="$POSSIBLE_PATH"
    echo "✅ Python 3.14 found via system: $PYTHON_310_PATH"
    PYTHON_310_FOUND=true
    break
  fi
done

# If not found in system locations, check PATH but exclude mise-managed paths
if [ "$PYTHON_310_FOUND" = false ]; then
  PYTHON_310_PATH=$(command -v python3.14 2>/dev/null)
  if [ -n "$PYTHON_310_PATH" ] && ! echo "$PYTHON_310_PATH" | grep -qE "(mise|\.mise)"; then
    if "$PYTHON_310_PATH" --version 2>&1 | grep -q "3.14"; then
      echo "✅ Python 3.14 found via system: $PYTHON_310_PATH"
      PYTHON_310_FOUND=true
    fi
  fi
fi

# If not found, check mise
if [ "$PYTHON_310_FOUND" = false ]; then
  if command -v mise >/dev/null 2>&1; then
    # Try to find Python 3.14 via mise
    MISE_PYTHON=$(mise which python3.14 2>/dev/null || true)
    if [ -n "$MISE_PYTHON" ] && [ -x "$MISE_PYTHON" ]; then
      PYTHON_310_PATH="$MISE_PYTHON"
      echo "✅ Python 3.14 found via mise: $PYTHON_310_PATH"
      PYTHON_310_FOUND=true
    else
      echo "❌ Python 3.14 not found via mise"
      echo ""
      echo "To install Python 3.14 via mise:"
      echo "  1. Run: mise install python@3.14"
      echo ""
      echo "Common installation issues:"
      echo "  - Network issues (check your internet connection)"
      echo "  - mise not in PATH (restart your shell or see docs/contributing.md)"
      exit 1
    fi
  else
    echo "❌ Python 3.14 not found and mise is not installed"
    echo ""
    echo "Options:"
    echo "  1. Install via system package manager (Ubuntu/Debian):"
    echo "     sudo apt install python3.14 python3.14-venv python3.14-dev"
    echo ""
    echo "  2. Install via mise (see docs/contributing.md for full setup):"
    echo "     First install mise, then: mise install python@3.14"
    exit 1
  fi
fi

echo ""
echo "✅ Python 3.14 is available! You can use:"
echo "   poetry run poe env:py310    # Switch to Python 3.14"
echo "   poetry run poe test:py310   # Test on Python 3.14"

