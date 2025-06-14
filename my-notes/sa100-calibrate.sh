#!/bin/bash

ARMS='["right_leader", "left_leader", "right_follower", "left_follower"]'
HAS_ARGS=0
# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --arms)
            ARMS="$2"
            HAS_ARGS=1
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

CMD="python lerobot/scripts/control_robot.py \
    --robot.type=sa100 \
    --control.type=calibrate"

if [ $HAS_ARGS -eq 1 ]; then
    CMD="$CMD --control.arms='[\"$ARMS\"]'"
fi

echo $CMD 
eval $CMD