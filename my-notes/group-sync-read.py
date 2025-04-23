# https://www.genspark.ai/agents?id=992db78d-0889-4f1e-9c39-a0c8fa13ffd4

import os

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
PRESENT_POSITION_SIZE = 4        # Data size is 4 bytes (position + speed)

# Default settings
BAUDRATE = 1000000              # Default Baudrate of SCServo
DEVICENAME = '/dev/ttyACM0'     # Check which port is being used on your controller
                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"
PROTOCOL_END = 0                # SCServo bit end(STS/SMS=0, SCS=1)
GroupSyncRead
# Set the port path
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol type
packetHandler = PacketHandler(PROTOCOL_END)

# Initialize GroupSyncRead instance for Present Position
groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_STS_PRESENT_POSITION, PRESENT_POSITION_SIZE)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
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

# Add parameter storage for servo IDs 1-7
for servoId in range(1, 7):
    servo_addparam_result = groupSyncRead.addParam(servoId)
    if servo_addparam_result != True:
        print(f"[ID:{servoId:03d}] groupSyncRead addparam failed")
        quit()

while True:
    print("Press any key to read position! (or press ESC to quit)")
    if getch() == chr(0x1b):
        break

    # Syncread present position
    servo_comm_result = groupSyncRead.txRxPacket()
    if servo_comm_result != COMM_SUCCESS:
        print(f"Failed to sync read: {packetHandler.getTxRxResult(servo_comm_result)}")
        continue
        
    # Display position for each servo
    print("\nServo Positions:")
    print("-----------------")
    
    for servoId in range(1, 7):
        # Check if data from the servo is available
        if groupSyncRead.isAvailable(servoId, ADDR_STS_PRESENT_POSITION, PRESENT_POSITION_SIZE):
            # Get the position value (4 bytes data: Position + Speed)
            position_speed_data = groupSyncRead.getData(servoId, ADDR_STS_PRESENT_POSITION, PRESENT_POSITION_SIZE)
            
            # Extract actual position (lower 2 bytes)
            position = SCS_LOWORD(position_speed_data)
            
            # Extract speed (higher 2 bytes)
            speed = SCS_HIWORD(position_speed_data)
            
            print(f"Servo ID: {servoId} | Position: {position} | Speed: {SCS_TOHOST(speed, 15)}")
        else:
            print(f"Servo ID: {servoId} | Failed to get data")
    
    print("-----------------\n")

# Clear parameter storage before exit
groupSyncRead.clearParam()

# Close port
portHandler.closePort()
