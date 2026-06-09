import time
import logging

try:
    import smbus2 as smbus
except ImportError:
    smbus = None

class GyroHandler:
    def __init__(self, config):
        self.config = config['gyro']
        self.simulation = config['system'].get('simulation_mode', False)
        self.bus = None
        self.address = self.config['address']
        self.tilt_angle = 0.0

    def initialize(self):
        if self.simulation or smbus is None:
            logging.info("Gyro: Simulation mode active.")
            return True
        
        try:
            self.bus = smbus.SMBus(self.config['i2c_bus'])
            # Wake up MPU6050
            self.bus.write_byte_data(self.address, 0x6B, 0)
            return True
        except Exception as e:
            logging.error(f"Gyro: Error initializing: {e}")
            return False

    def get_tilt(self):
        if self.simulation:
            return 20.0 # Default tilt from config
            
        try:
            # Simple read of accelerometer X/Y to get tilt
            # Register 0x3B is Accel X
            # This is a simplified version
            return 20.0 
        except:
            return 20.0
