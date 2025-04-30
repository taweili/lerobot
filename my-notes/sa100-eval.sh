#! /bin/bash

python lerobot/scripts/eval.py \
  --policy.path=outputs/train/taweili/sa004/checkpoints/last/pretrained_model \
  --env.type=sa100 \
  --eval.batch_size=10 \
  --eval.n_episodes=50
