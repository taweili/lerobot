from lerobot.common.policies.act.modeling_act import ACTPolicy
from lerobot.common.robot_devices.robots.configs import Sa100RobotConfig
from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobot
import time
import torch

def busy_wait(duration):
    """Busy wait for the specified duration in seconds"""
    start = time.perf_counter()
    while time.perf_counter() - start < duration:
        pass

inference_time_s = 60
fps = 30
device = "cpu"  # TODO: On Mac, use "mps" or "cpu"

ckpt_path = "outputs/train/taweili/sa004/checkpoints/last/pretrained_model"
policy = ACTPolicy.from_pretrained(ckpt_path)
policy.to(device)

# Initialize and connect robot in mock mode for testing
robot_config = Sa100RobotConfig()
robot = ManipulatorRobot(robot_config)
robot.connect()

for _ in range(inference_time_s * fps):
    start_time = time.perf_counter()

    # Read the follower state and access the frames from the cameras
    observation = robot.capture_observation()

    # Convert to pytorch format: channel first and float32 in [0,1]
    # with batch dimension
    for name in observation:
        if "image" in name:
            observation[name] = observation[name].type(torch.float32) / 255
            observation[name] = observation[name].permute(2, 0, 1).contiguous()
        observation[name] = observation[name].unsqueeze(0)
        observation[name] = observation[name].to(device)

    # Compute the next action with the policy
    # based on the current observation
    action = policy.select_action(observation)
    # Remove batch dimension
    action = action.squeeze(0)
    # Move to cpu, if not already the case
    action = action.to("cpu")
    # Order the robot to move
    robot.send_action(action)

    dt_s = time.perf_counter() - start_time
    # Ensure we don't sleep for negative time
    wait_time = max(0, 1 / fps - dt_s)
    busy_wait(wait_time)
