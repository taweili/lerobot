import argparse
from lerobot.common.robot_devices.motors.configs import FeetechMotorsBusConfig
from lerobot.common.robot_devices.motors.feetech import FeetechMotorsBus

def scan_all_servos(port, model="sts3215", servo_id=None):
    # Create a config with a dummy motor
    config = FeetechMotorsBusConfig(
        port=port,
        motors={"dummy": (1, model)}
    )
    
    # Initialize the motor bus
    motor_bus = FeetechMotorsBus(config=config)
    
    try:
        # Connect to the motor bus
        motor_bus.connect()
        print(f"Connected to motor bus on port {port}")
        
        # Scan for either all possible IDs (1-253) or specific ID
        print("Scanning for servos...")
        if servo_id is not None:
            present_ids = motor_bus.find_motor_indices([servo_id])
        else:
            present_ids = motor_bus.find_motor_indices(list(range(1, 254)))
        
        if present_ids:
            print(f"Found {len(present_ids)} servos with IDs: {present_ids}")
            
            # Read additional information for each servo
            for servo_id in present_ids:
                try:
                    data_names = [
                        "Model", 
                        "ID", 
                        "Mode", 
                        "Present_Position", 
                        "Goal_Position",
                        "Offset",
                        "Status"
                    ]
                    print(f"\nServo ID: {servo_id}")
                    for data_name in data_names:
                        value = motor_bus.read_with_motor_ids(
                            motor_bus.motor_models, servo_id, data_name
                        )
                        print(f"  {data_name}: {value}")
                except Exception as e:
                    print(f"Error reading info for servo ID {servo_id}: {e}")
        else:
            print("No servos found. Check connections and power.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Disconnect from the motor bus
        motor_bus.disconnect()
        print("Disconnected from motor bus")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan for all connected servos")
    parser.add_argument("--port", type=str, required=True, help="Motor bus port (e.g., /dev/ttyACM0)")
    parser.add_argument("--model", type=str, default="sts3215", help="Motor model (default: sts3215)")
    parser.add_argument("--id", type=int, help="Specific servo ID to scan (default: scan all)")
    
    args = parser.parse_args()
    scan_all_servos(args.port, args.model, args.id)