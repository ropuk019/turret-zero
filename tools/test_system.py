import sys
import os
import yaml
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_hardware():
    print("--- TURRET ZERO HARDWARE TEST ---")
    
    with open('config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Test Camera
    print("\n[1/5] Testing Camera...")
    from camera.camera_handler import CameraHandler
    cam = CameraHandler(config)
    if cam.initialize():
        ret, frame = cam.get_frame()
        if ret:
            print("SUCCESS: Camera is working and capturing frames.")
        else:
            print("FAILED: Camera initialized but failed to capture.")
        cam.release()
    else:
        print("FAILED: Could not initialize camera.")

    # Test Motor
    print("\n[2/5] Testing Motor...")
    from control.rotation_motor import RotationMotor
    motor = RotationMotor(config)
    if motor.initialize():
        print("Motor initialized. Starting 5-second rotation test...")
        motor.start()
        start_angle = motor.get_angle()
        time.sleep(5)
        end_angle = motor.get_angle()
        motor.stop()
        if end_angle != start_angle or config['system']['simulation_mode']:
            print(f"SUCCESS: Motor rotation tracked. Angle moved from {start_angle:.1f} to {end_angle:.1f}")
        else:
            print("FAILED: Motor angle did not change.")
    else:
        print("FAILED: Could not initialize motor.")

    # Test GPS
    print("\n[3/5] Testing GPS...")
    from control.gps_handler import GPSHandler
    gps = GPSHandler(config)
    if gps.initialize():
        loc = gps.get_location()
        print(f"SUCCESS: GPS read location: {loc['lat']}, {loc['lon']}")
    else:
        print("FAILED: Could not initialize GPS.")

    # Test Gyro
    print("\n[4/5] Testing Gyroscope...")
    from control.gyro_handler import GyroHandler
    gyro = GyroHandler(config)
    if gyro.initialize():
        tilt = gyro.get_tilt()
        print(f"SUCCESS: Gyroscope read tilt: {tilt} degrees")
    else:
        print("FAILED: Could not initialize gyroscope.")

    # Test Telegram
    print("\n[5/5] Testing Telegram...")
    from communication.telegram_alert import TelegramAlert
    tg = TelegramAlert(config)
    if tg.enabled:
        print("Telegram is enabled. Sending test message...")
tg.send_alert("Turret Zero Hardware Test: System Online")
        print("Test message sent. Check your Telegram app.")
    else:
        print("SKIP: Telegram is disabled in config.")

    print("\n--- TEST COMPLETE ---")

if __name__ == "__main__":
    test_hardware()
