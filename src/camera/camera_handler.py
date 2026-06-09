import cv2
import time
import logging

class CameraHandler:
    def __init__(self, config):
        self.config = config['camera']
        self.simulation = config['system'].get('simulation_mode', False)
        self.cap = None
        
    def initialize(self):
        if self.simulation:
            logging.info("Camera: Simulation mode active.")
            return True
        
        try:
            self.cap = cv2.VideoCapture(self.config['device_index'])
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['resolution'][0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['resolution'][1])
            
            if not self.cap.isOpened():
                logging.error("Camera: Could not open video device.")
                return False
            
            return True
        except Exception as e:
            logging.error(f"Camera: Error initializing: {e}")
            return False

    def get_frame(self):
        if self.simulation:
            # Return a blank frame or a placeholder if simulation
            import numpy as np
            frame = np.zeros((self.config['resolution'][1], self.config['resolution'][0], 3), dtype=np.uint8)
            cv2.putText(frame, "SIMULATION MODE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return True, frame

        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            return ret, frame
        return False, None

    def release(self):
        if self.cap:
            self.cap.release()
