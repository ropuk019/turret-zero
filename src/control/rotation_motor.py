import time
import logging
import threading

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

class RotationMotor:
    def __init__(self, config):
        self.config = config['motor']
        self.simulation = config['system'].get('simulation_mode', False)
        self.pin = self.config['gpio_pin']
        self.speed_dps = self.config['speed_dps']
        self.current_angle = 0.0
        self.running = False
        self.pwm = None
        self.thread = None

    def initialize(self):
        if self.simulation or GPIO is None:
            logging.info("Motor: Simulation mode active.")
            return True
        
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.pin, 50) # 50Hz
            self.pwm.start(0)
            return True
        except Exception as e:
            logging.error(f"Motor: Error initializing: {e}")
            return False

    def _run_loop(self):
        last_time = time.time()
        # For a continuous rotation servo, duty cycle controls speed.
        # FS90R: 1.5ms (7.5%) is stop, 2.0ms (10%) is full speed one way, 1.0ms (5%) other way.
        # We'll set it to a slow rotation.
        
        if not self.simulation and self.pwm:
            # Adjust duty cycle for desired speed. 
            # This is very hardware dependent. Let's assume 8% duty cycle for slow CW rotation.
            self.pwm.ChangeDutyCycle(7.7) 

        while self.running:
            now = time.time()
            dt = now - last_time
            last_time = now
            
            # Update internal angle estimate
            self.current_angle = (self.current_angle + self.speed_dps * dt) % 360
            time.sleep(0.1)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logging.info("Motor: Scanning started.")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        if self.pwm:
            self.pwm.ChangeDutyCycle(0)
            self.pwm.stop()
        if GPIO:
            # GPIO.cleanup() # Usually handled in main
            pass
        logging.info("Motor: Scanning stopped.")

    def get_angle(self):
        return self.current_angle
