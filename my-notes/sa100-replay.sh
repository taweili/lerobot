#!/bin/bash

# Check if repo_id parameter is provided
if [ -z "$1" ]; then
    echo "Error: repo_id parameter is required"
    echo "Usage: $0 <user/repo> [episode]"
    exit 1
fi

REPO_ID=$1 

# Set episode index (default to 0 if not provided)
EPISODE=${2:-0}

mamba run -n dpbot python lerobot/scripts/control_robot.py \
    --robot.type=sa100 \
    --control.type=replay \
    --control.fps 30 \
    --control.root "my-notes/dataset/$REPO_ID" \
    --control.repo_id "$1" \
    --control.episode "$EPISODE"
