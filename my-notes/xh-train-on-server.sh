#!/bin/bash

if [ -z "$1" ]; then
    echo "用法: $0 <仓库ID>"
    exit 1
fi

REPO_ID="$1-$(hostname)"
DATASET_PATH="my-notes/dataset/$REPO_ID"
SERVER_PATH="dpbot/lerobot/$DATASET_PATH"
DPBOT_SERVER="dpbot@dpbot-server.local"

if [ ! -d "$DATASET_PATH" ]; then
    echo "错误: 数据集目录 $DATASET_PATH 不存在"
    exit 1
fi

ssh dpbot@dpbot-server.local "mkdir -p $SERVER_PATH"
scp -r $DATASET_PATH/* $DPBOT_SERVER:$SERVER_PATH

echo "\n\n正在登录服务器，您可以使用 my-notes/sa100-train.sh 进行训练，REPO_ID 为 $REPO_ID\n\n"
ssh $DPBOT_SERVER
