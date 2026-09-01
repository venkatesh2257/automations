#!/bin/bash
# Master Automation Controller Script (Workhive Work Log Only)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "=================================================="
echo "         WORKHIVE AUTOMATION CONTROLLER           "
echo "=================================================="
echo "[+] Workhive Log Update & Excel Sync"
echo "=================================================="

ACTION="${1:-workhive}"

if [ "$ACTION" = "poweroff" ]; then
    echo "[+] Prompting Workhive Log Update & Shutting down..."
    "$SCRIPT_DIR/workhive/run_worklog.sh" --poweroff
else
    echo "[+] Running Workhive Daily Log & Excel Update..."
    "$SCRIPT_DIR/workhive/run_worklog.sh"
fi
