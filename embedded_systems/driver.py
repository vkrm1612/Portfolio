from serial import Serial
from time import sleep
import struct

class RPLidarSC:
    """Deals with RPLIDAR S & C Series based on Slamtec Protocol v2.8"""
    
    def __init__(self, port, baudrate=115200, timeout=1):
        """Initialize the connection parameters."""
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._is_scanning = False
        self._is_connected = False
        self._s = None

    def Connect(self):
        """Begin serial connection with RPLIDAR and check health."""
        try:
            if not self._is_connected:
                self._s = Serial(self._port, self._baudrate, timeout=self._timeout)
                self._is_connected = True
                
                # Protocol requires a short wait after power-up/connection
                sleep(0.5)
                self._s.reset_input_buffer()
                
                if self.GetHealthStatus():
                    return True
                else:
                    raise Exception('LIDAR in Protection Stop state. Try Reset().')
            else:
                raise Exception("Already connected")
        except Exception as e:
            print(f"Connection Error: {e}")
            return False

    def _Send_Request(self, command, payload=b''):
        """Formats and sends a request packet (Start Flag 0xA5 + Command)."""
        packet = b'\xA5' + command
        if payload:
            # If request carries payload, add Size, Data, and Checksum
            size = bytes([len(payload)])
            checksum = 0xA5 ^ ord(command) ^ len(payload)
            for b in payload:
                checksum ^= b
            packet += size + payload + bytes([checksum])
        self._s.write(packet)

    def GetHealthStatus(self):
        """Returns True if RPLIDAR health status is 'Good'."""
        if not self._is_connected: 
            return False
        
        # Send GET_HEALTH request (0x52)
        self._Send_Request(b'\x52')
        
        # Read 7-byte Response Descriptor
        descriptor = self._s.read(7)
        if len(descriptor) == 7 and descriptor[0:2] == b'\xA5\x5A':
            # Read 3-byte Data Response
            data = self._s.read(3)
            status = data[0] # 0: Good, 1: Warning, 2: Error
            return status == 0
        return False

    def GetDeviceInfo(self):
        """Returns dictionary of device information."""
        if not self._is_connected: 
            return None
        
        # Send GET_INFO request (0x50)
        self._Send_Request(b'\x50')
        descriptor = self._s.read(7)
        
        if len(descriptor) == 7 and descriptor[0:2] == b'\xA5\x5A':
            data = self._s.read(20)
            return {
                "model": data[0],
                "firmware": f"{data[2]}.{data[1]}",
                "hardware": data[3],
                "serial": data[4:].hex().upper()
            }
        return None

    def StartScanning(self):
        """Generator yielding 360-degree scan dictionaries {angle: distance_mm}."""
        if not self._is_connected: 
            raise Exception("Device is not connected")
        
        if self._is_scanning:
            raise Exception("Device is already scanning")

        self._is_scanning = True
        self._s.reset_input_buffer()
        
        # Send SCAN request (0x20)
        self._Send_Request(b'\x20')
        
        # Verify Response Descriptor (5-byte responses expected)
        descriptor = self._s.read(7)
        if not (len(descriptor) == 7 and descriptor[0:2] == b'\xA5\x5A'):
            self._is_scanning = False
            raise Exception("Failed to start scan: Invalid response descriptor")

        scan_data = {}
        while self._is_scanning:
            raw = self._s.read(5) # Standard SCAN response is 5 bytes
            if len(raw) < 5: 
                continue
            
            # Check Start Flag (S bit) for a new 360-degree rotation
            s_bit = raw[0] & 0x01
            
            # If a new scan starts and we have data, yield the previous full scan
            if s_bit and scan_data:
                yield scan_data
                scan_data = {}

            # Angle Calculation: Stored in q6 fixed point (divide by 64.0)
            # angle_q6 is bits [1:15] of bytes 1 and 2
            angle_raw = struct.unpack('<H', raw[1:3])[0] >> 1
            angle = angle_raw / 64.0
            
            # Distance Calculation: Stored in q2 fixed point (divide by 4.0)
            dist_raw = struct.unpack('<H', raw[3:5])[0]
            distance = dist_raw / 4.0 # result in mm
            
            if distance > 0:
                scan_data[round(angle, 2)] = distance

    def StopScanning(self):
        """Stops scanning and laser operation."""
        if self._is_connected:
            # Send STOP request (0x25)
            self._Send_Request(b'\x25')
            self._is_scanning = False
            sleep(0.02) # Required 10ms-20ms wait before next request

    def Reset(self):
        """Resets/Reboots the RPLIDAR core."""
        if self._is_connected:
            # Send RESET request (0x40)
            self._Send_Request(b'\x40')
            self._is_scanning = False
            sleep(0.6) # Required >500ms wait for reboot
            self._s.reset_input_buffer()

    def Disconnect(self):
        """Stops scanning and closes serial port."""
        if self._is_connected:
            if self._is_scanning:
                self.StopScanning()
            self._s.close()
            self._is_connected = False
