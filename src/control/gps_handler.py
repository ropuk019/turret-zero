import time
import logging
import threading

class GPSHandler:
    def __init__(self, config):
        self.config = config['gps']
        self.simulation = config['system'].get('simulation_mode', False)
        self.current_pos = {
            'lat': self.config['default_lat'],
            'lon': self.config['default_lon'],
            'alt': self.config['default_alt']
        }
        self.running = False
        self.thread = None

    def initialize(self):
        if self.simulation:
            logging.info("GPS: Simulation mode active.")
            return True
        
        # In reality, would use serial library to read NMEA
        # For this template, we'll simulate the interface
        logging.info(f"GPS: Attempting to connect on {self.config['port']}")
        return True

    def _update_loop(self):
        while self.running:
            if not self.simulation:
                # Actual NMEA parsing would go here
                pass
            time.sleep(5)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def get_location(self):
        return self.current_pos
