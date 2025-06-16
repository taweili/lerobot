#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 <repo_id> --single_task=<task> --tags=<json_array> [--episode_time_s=10] [--reset_time_s=10] [--num_episodes=5]"
    echo "  repo_id : Repository ID (must be a non-empty string)"
    echo "Required Options:"
    echo "  --single_task    : Task description (e.g. 'pick up doll')"
    echo "  --tags           : comma seperated tags (e.g. sa100,doll)"
    echo "Optional Options:"
    echo "  --episode_time_s : Episode duration in seconds (default: 10)"
    echo "  --reset_time_s   : Reset duration in seconds (default: 10)"
    echo "  --num_episodes   : Number of episodes (default: 5)"
    exit 1
}

# Default values
EPISODE_TIME_S=10
RESET_TIME_S=10
NUM_EPISODES=5
SINGLE_TASK=""
TAGS=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --single_task=*)
            SINGLE_TASK="${1#*=}"
            shift
            ;;
        --tags=*)
            TAGS="${1#*=}"
            shift
            ;;
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
                REPO_ID="$1-$(hostname)"
                shift
            else
                echo "Error: Unknown argument $1"
                usage
            fi
            ;;
    esac
done

# Check if required arguments are provided
if [ -z "$REPO_ID" ]; then
    echo "Error: repo_id argument is required"
    usage
fi

if [ -z "$SINGLE_TASK" ]; then
    echo "Error: --single_task argument is required"
    usage
fi

if [ -z "$TAGS" ]; then
    echo "Error: --tags argument is required"
    usage
else
    TAGS_JSON=$(echo "$TAGS" | jq -Rc 'split(",")')
    TAGS="$TAGS_JSON"
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
  --control.single_task="$SINGLE_TASK" \
  --control.tags="$TAGS" \
  --control.warmup_time_s=5 \
  --control.episode_time_s=$EPISODE_TIME_S \
  --control.reset_time_s=$RESET_TIME_S \
  --control.num_episodes=$NUM_EPISODES \
  --control.push_to_hub=false \
  --control.root=my-notes/dataset/$REPO_ID \
  --control.repo_id="$REPO_ID" \
  --control.display_data=true 
