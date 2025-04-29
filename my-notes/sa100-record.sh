#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 <repo_id>"
    echo "  repo_id : Repository ID (must be a non-empty string)"
    exit 1
}

# Check if repo_id argument is provided
if [ $# -eq 0 ]; then
    echo "Error: repo_id argument is required"
    usage
fi

# Get the repo_id from first argument
REPO_ID="$1"

# Validate repo_id is not empty
if [ -z "$REPO_ID" ]; then
    echo "Error: repo_id must be a non-empty string"
    usage
fi

python lerobot/scripts/control_robot.py \
  --robot.type=sa100 \
  --control.type=record \
  --control.fps=30 \
  --control.single_task="pick up doll" \
  --control.tags='["sa100","tutorial"]' \
  --control.warmup_time_s=5 \
  --control.episode_time_s=30 \
  --control.reset_time_s=30 \
  --control.num_episodes=2 \
  --control.push_to_hub=false \
  --control.root=/home/david/Works/lerobot/my-notes/dataset/$REPO_ID \
  --control.repo_id="$REPO_ID" \
  --control.display_data=true 
