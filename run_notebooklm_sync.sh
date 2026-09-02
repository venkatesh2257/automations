#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ -d "$DIR/venv" ]; then
    "$DIR/venv/bin/python3" "$DIR/tech_course_ai/notebooklm_video_sync.py" "$@"
else
    python3 "$DIR/tech_course_ai/notebooklm_video_sync.py" "$@"
fi
