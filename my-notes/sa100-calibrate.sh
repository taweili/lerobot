#!/bin/bash

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --arms)
            arms="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Default to both arms if not specified
arms=${arms:-"right left"}

python lerobot/scripts/control_robot.py \
    --robot.type=sa100 \
    --control.type=calibrate \
    --control.arms $arms  # Use specified arms or default to both