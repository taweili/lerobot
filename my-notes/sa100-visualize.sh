#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <repo-id>"
    exit 1
fi

REPO_ID=$1
ROOT_PATH="my-notes/dataset/$REPO_ID"

python lerobot/scripts/visualize_dataset_html.py \
    --root $ROOT_PATH \
    --repo-id $REPO_ID \
    --port 9013
