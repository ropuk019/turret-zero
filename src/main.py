import os
import sys
import time
import yaml
import logging
import cv2
import threading
from datetime import datetime

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from camera.camera_handler import CameraHandler
from detection.aircraft_detector import AircraftDetector
from tracking.coordinate_calculator import CoordinateCalculator
from tracking.flight_predictor import FlightPredictor
from control.rotation_motor import RotationMotor
from control.gps_handler import GPSHandler
from control.gyro_handler import GyroHandler
from communication.telegram_alert import TelegramAlert

class TurretZero:
    def __init__(self, config_path="config/settings.yaml"):
        self.load_config(config_path)
        self.setup_logging()
        
        self.camera = CameraHandler(self.config)
        self.detector = AircraftDetector(self.config)
        self.coord_calc = CoordinateCalculator(self.config)
        self.predictor = FlightPredictor()
        self.motor = RotationMotor(self.config)
        self.gps = GPSHandler(self.config)
        self.gyro = GyroHandler(self.config)
        self.telegram = TelegramAlert(self.config)
        
        self.last_alert_time = 0
        self.running = False

    def load_config(self, path):
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler("data/logs/system.log"),
                logging.StreamHandler()
            ]
        )

    def initialize(self):
        logging.info("Initializing Turret Zero...")
        success = True
        success &= self.camera.initialize()
        success &= self.detector.load_model()
        success &= self.motor.initialize()
        success &= self.gps.initialize()
        success &= self.gyro.initialize()
        
        if not success:
            logging.error("Initialization failed! Check logs.")
            return False
        
        logging.info("All systems initialized successfully.")
        return True

    def run(self):
        self.running = True
        self.motor.start()
        self.gps.start()
        
        try:
            while self.running:
                ret, frame = self.camera.get_frame()
                if not ret:
                    continue

                detections = self.detector.detect(frame)
                
                if detections:
                    # Take the highest confidence detection
                    best_det = max(detections, key=lambda x: x['confidence'])
                    
                    # Calculate position
                    azimuth = self.motor.get_angle()
                    elevation = self.gyro.get_tilt()
                    station_pos = self.gps.get_location()
                    
                    bbox = best_det['bbox']
                    pixel_width = bbox[2] - bbox[0]
                    
                    obj_gps = self.coord_calc.calculate_object_gps(
                        station_pos, azimuth, elevation, pixel_width, frame.shape[1]
                    )
                    
                    self.predictor.add_datapoint(obj_gps['lat'], obj_gps['lon'], obj_gps['alt'])
                    prediction = self.predictor.predict()
                    
                    best_det['gps'] = obj_gps
                    best_det['direction'] = self.coord_calc.get_cardinal_direction(azimuth)
                    best_det['prediction'] = prediction
                    
                    # Alert cooldown
                    now = time.time()
                    if now - self.last_alert_time > self.config['system']['alert_cooldown']:
                        self.handle_alert(frame, best_det)
                        self.last_alert_time = now

                # Display for local debugging if needed
                # cv2.imshow("Turret Zero", frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'): break
                
                # Handle Telegram commands
                self.telegram.handle_commands(self.get_status)

                time.sleep(0.01) # Low CPU usage

    def get_status(self):
        motor_status = "Scanning" if self.motor.running else "Stopped"
        return f"Turret Zero: Online\nMotor: {motor_status}\nLast Alert: {datetime.fromtimestamp(self.last_alert_time).strftime('%H:%M:%S') if self.last_alert_time > 0 else 'None'}"

        except KeyboardInterrupt:
            logging.info("Shutdown requested by user.")
        finally:
            self.stop()

    def handle_alert(self, frame, detection):
        logging.info(f"ALARM: {detection['label']} detected at {detection['gps']['lat']}, {detection['gps']['lon']}")
        
        # Save photo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/photos/detection_{timestamp}.jpg"
        
        # Draw on frame before saving
        annotated_frame = self.detector.draw_detections(frame.copy(), [detection])
        cv2.imwrite(filename, annotated_frame)
        
        # Send Telegram alert
        message = self.telegram.format_alert(detection)
        self.telegram.send_alert(message, filename)

    def stop(self):
        self.running = False
        self.motor.stop()
        self.gps.stop()
        self.camera.release()
        logging.info("System stopped safely.")

if __name__ == "__main__":
    turret = TurretZero()
    if turret.initialize():
        turret.run()
