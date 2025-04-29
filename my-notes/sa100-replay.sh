#!/bin/bash

# Check if repo_id parameter is provided
if [ -z "$1" ]; then
    echo "Error: repo_id parameter is required"
    echo "Usage: $0 <user/repo> [episode_index]"
    exit 1
fi

# Extract user and repo name from repo_id
IFS='/' read -ra PARTS <<< "$1"
if [ ${#PARTS[@]} -ne 2 ]; then
    echo "Error: Invalid repo_id format. Expected 'user/repo'"
    exit 1
fi
USER=${PARTS[0]}
REPO=${PARTS[1]}

# Set episode index (default to 0 if not provided)
EPISODE=${2:-0}

python lerobot/scripts/control_robot.py \
    --robot.type=sa100 \
    --control.type=replay \
    --control.fps 30 \
    --control.root "my-notes/dataset/$USER/$REPO" \
    --control.repo_id "$1" \
    --control.episode "$EPISODE"
