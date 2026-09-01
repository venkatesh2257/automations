#!/bin/bash
# Runner for Workhive Engine
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_BIN="$PARENT_DIR/venv/bin/python"

"$PYTHON_BIN" "$SCRIPT_DIR/workhive_engine.py" "$@"
