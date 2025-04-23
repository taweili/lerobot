# https://www.genspark.ai/agents?id=17a42d26-f329-4264-933e-539dfa73f8cb

from lerobot.common.datasets.lerobot_dataset import LeRobotDataset

# Load a dataset from Hugging Face Hub
dataset = LeRobotDataset("lerobot/pusht")

# Visualize a dataset episode
import os
os.system("python lerobot/scripts/visualize_dataset.py --repo-id lerobot/pusht --episode-index 0")
