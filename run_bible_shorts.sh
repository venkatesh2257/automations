#!/bin/bash
# One-click runner for Biblical Stories AI YouTube Shorts Generator

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"
PROJECT_DIR="$SCRIPT_DIR/bible_shorts_ai"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "[!] Virtual environment not found. Please check ./venv"
    exit 1
fi

export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
"$VENV_PYTHON" "$PROJECT_DIR/main.py" "$@"
