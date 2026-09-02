#!/bin/bash
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
ROOT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

if [ -d "$ROOT_DIR/venv" ]; then
    "$ROOT_DIR/venv/bin/python3" "$ROOT_DIR/tech_course_ai/deepdive_pipeline.py" "$@"
else
    python3 "$ROOT_DIR/tech_course_ai/deepdive_pipeline.py" "$@"
fi
