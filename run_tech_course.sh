#!/bin/bash
# Master runner for Pro-Teacher Technical Course Video Generator

TARGET_SOURCE="${BASH_SOURCE[0]}"
while [ -h "$TARGET_SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$TARGET_SOURCE" )" >/dev/null 2>&1 && pwd )"
  TARGET_SOURCE="$(readlink "$TARGET_SOURCE")"
  [[ $TARGET_SOURCE != /* ]] && TARGET_SOURCE="$DIR/$TARGET_SOURCE"
done
SCRIPT_DIR="$( cd -P "$( dirname "$TARGET_SOURCE" )" >/dev/null 2>&1 && pwd )"

if [ ! -d "$SCRIPT_DIR/tech_course_ai" ]; then
    SCRIPT_DIR="/home/user/Desktop/automation"
fi

VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"
PROJECT_DIR="$SCRIPT_DIR/tech_course_ai"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "[!] Virtual environment not found at: $VENV_PYTHON"
    exit 1
fi

export PYTHONPATH="$PROJECT_DIR:$PYTHONPATH"
"$VENV_PYTHON" "$PROJECT_DIR/main.py" "$@"
