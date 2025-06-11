from lerobot.common.robot_devices.robots.configs import Sa100RobotConfig

# Create SA100 config using its specific class
config = Sa100RobotConfig()

print("SA100 Leader arms:", list(config.leader_arms.keys()))
print("SA100 Follower arms:", list(config.follower_arms.keys()))

# Print detailed motor info for each arm
for arm_type in ["leader", "follower"]:
    arms = getattr(config, f"{arm_type}_arms")
    print(f"\n{arm_type.capitalize()} Arms Details:")
    for arm_name, arm_config in arms.items():
        print(f"  {arm_name}:")
        print(f"    Port: {arm_config.port}")
        print("    Motors:")
        for motor_name, motor_info in arm_config.motors.items():
            print(f"      {motor_name}: ID {motor_info[0]}, Model {motor_info[1]}")