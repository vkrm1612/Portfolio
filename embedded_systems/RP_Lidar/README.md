
# RPLIDAR S & C Series Python Driver

This project provides a Python-based interface for the **Slamtec RPLIDAR S & C series** laser scanners. It implements the binary protocol (v2.8) to handle device communication via a TTL UART serial interface.

## 1. Project Overview

The driver manages the communication lifecycle between a host system and the RPLIDAR core. It handles initialization, state transitions, and high-frequency data parsing for 360-degree environmental mapping.

### Major Working States
- **Idle**: Power-saving mode where the laser and motor are disabled.
- **Scanning**: Active measurement mode where data is streamed to the host.
- **Protection Stop**: Safety state triggered by hardware failure; requires a reset to recover.

---

## 2. Technical Specifications

### Measurement Data Format
In standard `SCAN` mode, each measurement sample is encapsulated in a 5-byte packet. The driver parses these using the following fixed-point mathematics:

* **Angle ($\theta$):** Stored in **q6** format. 
    * $Actual\ Angle = \frac{angle\_q6}{64.0}$ (degrees)
* **Distance ($d$):** Stored in **q2** format. 
    * $Actual\ Distance = \frac{distance\_q2}{4.0}$ (mm)



### Request Protocol
Every request packet follows a strict binary structure:
- **Start Flag**: `0xA5` (1 byte)
- **Command**: 8-bit command ID (1 byte)
- **Optional Payload**: Includes Payload Size, Data, and Checksum.

---

## 3. Driver Architecture

```mermaid
classDiagram
    class RPLidarSC {
        -port: String
        -baudrate: int
        -is_scanning: bool
        -serial_conn: Serial
        +Connect() bool
        +StartScanning() Generator
        +StopScanning() void
        +Reset() void
        +GetHealthStatus() dict
        +GetDeviceInfo() dict
        -_Send_Request(cmd, payload) void
    }
