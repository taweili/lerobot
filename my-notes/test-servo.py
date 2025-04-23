from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus
from lerobot.common.robot_devices.motors.configs import FeetechMotorsBusConfig
import time
import argparse

def test_servo_communication(port='/dev/ttyACM0', motor_id=1):
    motor_name = f"motor_{motor_id}"
    try:
        # Configure motor
        config = FeetechMotorsBusConfig(
            port=port,
            motors={motor_name: (motor_id, 'sts3215')},
            mock=False
        )
        
        # Initialize motor bus
        motor_bus = FeetechMotorsBus(config)
        motor_bus.connect()
        
        print(f"\n=== Testing Servo ID {motor_id} ===")
        
        # Enable torque
        motor_bus.write('Torque_Enable', 1, motor_name)
        print("Torque enabled")
        
        # Test reading position
        position = motor_bus.read('Present_Position', motor_name)
        print(f"Current position: {position}")
        
        # Test moving to position if goal specified
        if args.goal is not None:
            print(f"Moving to position {args.goal}...")
            motor_bus.write('Goal_Position', args.goal, motor_name)
            time.sleep(2)
            position = motor_bus.read('Present_Position', motor_name)
            print(f"New position: {position}")
        else:
            print("No goal position specified - skipping movement test")
        
        # Disable torque when done
        motor_bus.write('Torque_Enable', 0, motor_name)
        motor_bus.disconnect()
        print(f"Servo ID {motor_id} test completed successfully")
        
    except Exception as e:
        print(f"\nError testing Servo ID {motor_id}: {str(e)}")
        if 'motor_bus' in locals():
            motor_bus.disconnect()
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Feetech servo communication')
    parser.add_argument('--id', type=int, help='Servo ID to test (1-7)')
    parser.add_argument('--port', type=str, default='/dev/ttyACM0', help='Serial port')
    parser.add_argument('--goal', type=int, help='Optional goal position to move to')
    args = parser.parse_args()

    if args.id:
        # Test single specified servo
        test_servo_communication(port=args.port, motor_id=args.id)
    else:
        # Default behavior: test all servos 1-7
        for motor_id in range(1, 8):
            try:
                test_servo_communication(port=args.port, motor_id=motor_id)
            except Exception:
                print(f"Skipping Servo ID {motor_id} due to error")
                continue