# Servo Control Parameters

Valid `data_name` values for `read_with_motor_ids` operations:

## Motor Configuration
- `Model` - Motor model number (2 bytes)
- `ID` - Motor ID (1 byte)
- `Baud_Rate` - Communication speed (1 byte)
- `Return_Delay` - Response delay time (1 byte)
- `Response_Status_Level` - Error response level (1 byte)
- `Phase` - Motor phase (1 byte)
- `Mode` - Operating mode (1 byte)

## Limit Settings
- `Min_Angle_Limit` - Minimum position limit (2 bytes)
- `Max_Angle_Limit` - Maximum position limit (2 bytes)
- `Max_Temperature_Limit` - Temperature cutoff (1 byte)
- `Max_Voltage_Limit` - Maximum voltage (1 byte)
- `Min_Voltage_Limit` - Minimum voltage (1 byte)
- `Max_Torque_Limit` - Maximum torque (2 bytes)
- `Protection_Current` - Current protection threshold (2 bytes)

## Control Parameters
- `P_Coefficient` - Proportional gain (1 byte)
- `D_Coefficient` - Derivative gain (1 byte)
- `I_Coefficient` - Integral gain (1 byte)
- `Minimum_Startup_Force` - Minimum startup torque (2 bytes)
- `CW_Dead_Zone` - Clockwise dead zone (1 byte)
- `CCW_Dead_Zone` - Counter-clockwise dead zone (1 byte)
- `Offset` - Position offset (2 bytes)
- `Angular_Resolution` - Position resolution (1 byte)

## Status Monitoring
- `Present_Position` - Current position (2 bytes)
- `Present_Speed` - Current speed (2 bytes)
- `Present_Load` - Current load (2 bytes)
- `Present_Voltage` - Current voltage (1 byte)
- `Present_Temperature` - Current temperature (1 byte)
- `Present_Current` - Current draw (2 bytes)
- `Status` - Error status (1 byte)
- `Moving` - Movement status (1 byte)

## Torque Control
- `Torque_Enable` - Torque on/off (1 byte)
- `Torque_Limit` - Torque limit (2 bytes)
- `Protective_Torque` - Protection torque (1 byte)
- `Overload_Torque` - Overload torque (1 byte)

## Motion Control
- `Goal_Position` - Target position (2 bytes)
- `Goal_Time` - Movement time (2 bytes)
- `Goal_Speed` - Target speed (2 bytes)
- `Acceleration` - Acceleration rate (1 byte)

## Protection Settings
- `Lock` - EEPROM lock (1 byte)
- `Protection_Time` - Overload protection time (1 byte)
- `Over_Current_Protection_Time` - Current protection time (1 byte)

## Calibration Usage

During servo calibration:
- `Present_Position` is used to read current positions
- `Goal_Position` is used to set:
  - `start_pos`: Initial calibration position
  - `end_pos`: Target calibration position
  - `zero_pos`: Zero/reference position

These positions are stored in calibration JSON files with their corresponding motor names.