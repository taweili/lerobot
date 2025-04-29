#!/bin/bash

python lerobot/scripts/control_robot.py \
    --robot.type=sa100 \
    --control.display_data=true \
    --control.type=teleoperate 
