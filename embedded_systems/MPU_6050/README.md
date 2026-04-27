
# MPU-6050 Arduino I2C Reader

This project provides a lightweight, library-free implementation for reading data from the MPU-6050 Accelerometer and Gyroscope using the Arduino Wire (I2C) library.

## Demo
![Project Demo](end_effector.gif)

## Features
- I2C register access (no heavy libraries).
- Accelerometer data in G-force (range: +/- 2g).
- Gyroscope data in Degrees per Second (range: +/- 250 deg/s).

## Pinout Configuration
For standard Arduino boards (Uno, Nano, Mini), use the following wiring:

| MPU-6050 Pin | Arduino Pin | Description |
| :--- | :--- | :--- |
| **VCC** | 3.3V / 5V | Power (check your module regulator) |
| **GND** | GND | Ground |
| **SCL** | A5 | I2C Clock |
| **SDA** | A4 | I2C Data |
| **AD0** | GND | Sets I2C Address to 0x68 |

## Technical Specifications
- **I2C Address:** 0x68
- **Accel Sensitivity:** 16384 LSB/g
- **Gyro Sensitivity:** 131 LSB/deg/s

## Usage
1. Connect the MPU-6050 to your Arduino according to the pinout above.
2. Upload the provided `.ino` source code.
3. Open the Serial Monitor at **9600 Baud**.
4. Observe real-time motion data.

## Register Map Used
- `0x6B`: Power Management (Wake up sensor)
- `0x1B`: Gyroscope Configuration
- `0x1C`: Accelerometer Configuration
- `0x3B - 0x40`: Accelerometer Measurements
- `0x43 - 0x48`: Gyroscope Measurements
