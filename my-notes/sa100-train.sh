

#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage: $0 repo_id"
    exit 1
fi

REPO_ID=$1

python lerobot/scripts/train.py \
  --policy.type=act \
  --policy.device=cpu \
  --output_dir=outputs/train/$REPO_ID \
  --dataset.root=my-notes/dataset/$REPO_ID \
  --dataset.repo_id=$REPO_ID \
  