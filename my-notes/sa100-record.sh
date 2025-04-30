#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 <repo_id> [--episode_time_s=10] [--reset_time_s=10] [--num_episodes=5]"
    echo "  repo_id : Repository ID (must be a non-empty string)"
    echo "Options:"
    echo "  --episode_time_s : Episode duration in seconds (default: 10)"
    echo "  --reset_time_s   : Reset duration in seconds (default: 10)"
    echo "  --num_episodes   : Number of episodes (default: 5)"
    exit 1
}

# Default values
EPISODE_TIME_S=10
RESET_TIME_S=10
NUM_EPISODES=5

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --episode_time_s=*)
            EPISODE_TIME_S="${1#*=}"
            shift
            ;;
        --reset_time_s=*)
            RESET_TIME_S="${1#*=}"
            shift
            ;;
        --num_episodes=*)
            NUM_EPISODES="${1#*=}"
            shift
            ;;
        *)
            if [ -z "$REPO_ID" ]; then
                REPO_ID="$1"
                shift
            else
                echo "Error: Unknown argument $1"
                usage
            fi
            ;;
    esac
done

# Check if repo_id argument is provided
if [ -z "$REPO_ID" ]; then
    echo "Error: repo_id argument is required"
    usage
fi

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
  --control.episode_time_s=$EPISODE_TIME_S \
  --control.reset_time_s=$RESET_TIME_S \
  --control.num_episodes=$NUM_EPISODES \
  --control.push_to_hub=false \
  --control.root=/home/david/Works/lerobot/my-notes/dataset/$REPO_ID \
  --control.repo_id="$REPO_ID" \
  --control.display_data=true 
