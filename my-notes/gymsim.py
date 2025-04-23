import gymnasium as gym
import gym_pusht  # or gym_aloha, gym_xarm

# Create environment
env = gym.make("gym_pusht/PushT-v0", render_mode="human")
observation, info = env.reset()

# Interact with environment
for _ in range(1000):
    action = env.action_space.sample()  # Replace with your policy
    observation, reward, terminated, truncated, info = env.step(action)
    
    if terminated or truncated:
        observation, info = env.reset()
