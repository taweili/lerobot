#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <repo_id> <policy_type_or_path>"
  echo "Policy type examples: tdmpc, diffusion, act"
  echo "Policy path examples: lerobot/pi0fast_base, path/to/policy"
  exit 1
fi

REPO_ID="$1-$(hostname)"
INPUT=$2

# Determine if input is a policy type or path
if [[ $INPUT == */* ]]; then
  # Contains slash, treat as path
  POLICY_PATH=$INPUT
  POLICY_TYPE=""
else
  # No slash, treat as type
  POLICY_TYPE=$INPUT
  POLICY_PATH=""
fi

python lerobot/scripts/train.py \
  ${POLICY_TYPE:+--policy.type=$POLICY_TYPE} \
  ${POLICY_PATH:+--policy.path=$POLICY_PATH} \
  --output_dir=outputs/train/$REPO_ID \
  --dataset.root=my-notes/dataset/$REPO_ID \
  --dataset.repo_id=$REPO_ID \
