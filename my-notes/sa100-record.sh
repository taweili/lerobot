#!/bin/bash

# https://www.genspark.ai/agents?id=32507939-e62d-4db2-a528-809582876711

# Default values
REPO_ID="taweili/sa100_002"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo_id=*)
      REPO_ID="${1#*=}"
      shift
      ;;
    *)
      echo "Unknown parameter: $1"
      exit 1
      ;;
  esac
done

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
  --control.repo_id="$REPO_ID"
