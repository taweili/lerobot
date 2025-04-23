# https://www.genspark.ai/agents?id=992db78d-0889-4f1e-9c39-a0c8fa13ffd4

import os
import argparse

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from scservo_sdk import *                    # Uses SCServo SDK library

# Control table addresses for the servo
ADDR_STS_PRESENT_POSITION = 56   # Address for Present Position
ADDR_STS_TORQUE_ENABLE = 64      # Address for Torque Enable status
PRESENT_POSITION_SIZE = 4        # Data size is 4 bytes (position + speed)
TORQUE_ENABLE_SIZE = 1           # Data size is 1 byte for torque status

# Set up command line arguments
parser = argparse.ArgumentParser(description='SCServo group sync read utility')
parser.add_argument('--port', type=str, default='/dev/ttyACM0',
                   help='Port name (e.g. /dev/ttyACM0 or COM1)')
parser.add_argument('--n', type=int, default=7,
                   help='Number of servos to check (1-n)')
parser.add_argument('--ids', type=str,
                   help='Comma-separated list of servo IDs to check (overrides --n)')
args = parser.parse_args()

# Process servo IDs
if args.ids:
    try:
        servo_ids = [int(id.strip()) for id in args.ids.split(',')]
        if not servo_ids:
            raise ValueError("No valid servo IDs provided")
    except ValueError as e:
        print(f"Invalid servo IDs: {e}")
        quit()
else:
    servo_ids = list(range(1, args.n + 1))

# Protocol settings
BAUDRATE = 1000000              # Default Baudrate of SCServo
PROTOCOL_END = 0                # SCServo bit end(STS/SMS=0, SCS=1)

# Set the port path
portHandler = PortHandler(args.port)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_END)

# Initialize GroupSyncRead instances
groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_STS_PRESENT_POSITION, PRESENT_POSITION_SIZE)
groupSyncReadTorque = GroupSyncRead(portHandler, packetHandler, ADDR_STS_TORQUE_ENABLE, TORQUE_ENABLE_SIZE)

# Open port
if portHandler.openPort():
    print(f"Succeeded to open the port {args.port}")
else:
    print(f"Failed to open the port {args.port}")
    print("Press any key to terminate...")
    getch()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Add parameter storage for servo IDs
for servoId in servo_ids:
    servo_addparam_result = groupSyncRead.addParam(servoId)
    torque_addparam_result = groupSyncReadTorque.addParam(servoId)
    if servo_addparam_result != True or torque_addparam_result != True:
        print(f"[ID:{servoId:03d}] groupSyncRead addparam failed")
        quit()

while True:
    print("Press any key to read position! (or press ESC to quit)")
    if getch() == chr(0x1b):
        break

    # Syncread present position and torque status
    servo_comm_result = groupSyncRead.txRxPacket()
    torque_comm_result = groupSyncReadTorque.txRxPacket()
    if servo_comm_result != COMM_SUCCESS or torque_comm_result != COMM_SUCCESS:
        print(f"Failed to sync read: {packetHandler.getTxRxResult(servo_comm_result)}")
        continue
        
    # Display position for each servo
    print("\nServo Positions:")
    print("-----------------")
    
    for servoId in servo_ids:
        # Check if data from the servo is available
        if groupSyncRead.isAvailable(servoId, ADDR_STS_PRESENT_POSITION, PRESENT_POSITION_SIZE):
            # Get the position value (4 bytes data: Position + Speed)
            position_speed_data = groupSyncRead.getData(servoId, ADDR_STS_PRESENT_POSITION, PRESENT_POSITION_SIZE)
            
            # Extract actual position (lower 2 bytes)
            position = SCS_LOWORD(position_speed_data)
            
            # Extract speed (higher 2 bytes)
            speed = SCS_HIWORD(position_speed_data)
            
            # Get torque status
            torque_status = groupSyncReadTorque.getData(servoId, ADDR_STS_TORQUE_ENABLE, TORQUE_ENABLE_SIZE)
            torque_enabled = "ON" if torque_status else "OFF"
            print(f"Servo ID: {servoId} | Position: {position} | Speed: {SCS_TOHOST(speed, 15)} | Torque: {torque_enabled}")
        else:
            print(f"Servo ID: {servoId} | Failed to get data")
    
    print("-----------------\n")

# Clear parameter storage before exit
groupSyncRead.clearParam()

# Close port
portHandler.closePort()
