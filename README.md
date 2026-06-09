# Turret Zero

A simple air defence spotting system anyone can build for under $150.

## Overview
Turret Zero uses a Raspberry Pi 4, a rotating mount, and computer vision (YOLOv8) to scan the sky for aircraft. When an aircraft is detected, the system calculates its GPS coordinates, predicts its flight path, and sends an alert with a photo to your Telegram bot.

## Parts List
- Raspberry Pi 4 Model B (2GB+) 
- Raspberry Pi Camera Module v2 or HQ 
- Continuous rotation servo motor (FS90R) 
- GPS module (NEO-6M) 
- MPU6050 gyroscope sensor 
- Lazy Susan bearing (6 inch) 
- PVC pipe & T-joint 
- Wooden board (12x12") 
- Jumper wires & power supplies 
- MicroSD card (32GB) 
- External 5V/2A power supply for servo 

## Wiring Diagram (Raspberry Pi 4 Model B)

### Camera Module (CSI Port)
Connect the ribbon cable to the **CSI port** on the Pi 4:
- **Location:** Between the Ethernet port and HDMI ports
- **Orientation:** Metal contacts face AWAY from the Ethernet port (toward HDMI ports)
- **Lock tabs:** Gently lift the black tabs, insert cable, press down to lock

*Alternative: USB Webcam* - Plug into any USB port.

### Servo Motor (FS90R)
⚠️ **Requires external power - DO NOT use Pi 5V pin!**
```

FS90R            Raspberry Pi 4     External 5V Supply

---

Red    -----------(no)-----------   +5V (2A minimum)
Brown  ----------- GND (pin 6) ---  GND (common ground)
Orange ----------- GPIO 18 (pin 12)

```

### GPS Module (NEO-6M)
```

NEO-6M           Raspberry Pi 4

---

VCC    ----------- 3.3V (pin 1)
GND    ----------- GND (pin 9)
TX     ----------- RX (GPIO 15 / pin 10)
RX     ----------- TX (GPIO 14 / pin 8)

```

### MPU6050 Gyroscope (I2C)
```

MPU6050          Raspberry Pi 4

---

VCC    ----------- 3.3V (pin 1)
GND    ----------- GND (pin 9)
SDA    ----------- SDA (GPIO 2 / pin 3)
SCL    ----------- SCL (GPIO 3 / pin 5)

```

### Quick Pin Reference (RPi 4 Model B)
| GPIO | Pin # | Function | Connected To |
|------|-------|----------|--------------|
| 3.3V | 1     | Power    | GPS VCC, MPU VCC |
| 5V   | 2,4   | Power    | (Not for servo!) |
| GND  | 6,9   | Ground   | Servo, GPS, MPU |
| GPIO2| 3     | SDA      | MPU6050 SDA |
| GPIO3| 5     | SCL      | MPU6050 SCL |
| GPIO14| 8    | TX       | GPS RX |
| GPIO15| 10   | RX       | GPS TX |
| GPIO18| 12   | PWM      | Servo Orange |

## Installation
1. Enable camera & I2C interfaces:
   ```bash
   sudo raspi-config
   # Interface Options → Camera → Enable
   # Interface Options → I2C → Enable
   # Reboot
```

2. Clone the repository:
   ```bash
https://github.com/ropuk019/turret-zero.git
   cd turret-zero
   ```
3. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

Configuration

1. Create a Telegram bot using @BotFather.
2. Get your chat ID using @userinfobot.
3. Edit config/settings.yaml:
   ```yaml
   hardware:
     simulation_mode: false
     servo_pin: 18
     camera_type: "pi"  # or "usb"
   
   telegram:
     bot_token: "YOUR_BOT_TOKEN"
     chat_id: "YOUR_CHAT_ID"
     enabled: true
   
   gps:
     serial_port: "/dev/ttyAMA0"
     baud_rate: 9600
   ```

Running the System

1. Test your hardware:
   ```bash
   python3 tools/test_system.py
   ```
   · Test camera: --camera
   · Test servo: --servo
   · Test GPS: --gps
   · Test gyro: --gyro
2. Start the scanner:
   ```bash
   python3 src/main.py
   ```

Important Notes for RPi 4 Model B

· Servo Power: The Pi 4's 5V pins cannot drive a servo. Use external 5V/2A+ supply.
· Ground Connection: Connect servo ground to BOTH external supply AND Pi ground.
· UART for GPS: Disable Bluetooth if using UART (dtoverlay=disable-bt in /boot/config.txt)
· Camera: The CSI port is dedicated - USB webcams work too but use more CPU.
· Cooling: Pi 4 runs hot under load. Add a heatsink/fan if enclosed.

Troubleshooting

Issue Solution
Camera not detected vcgencmd get_camera → should show detected=1
I2C device missing i2cdetect -y 1 → should show 0x68 (MPU6050)
GPS no fix Wait 5-10 minutes outdoors, check LED blinking
Servo jittering Common ground missing or insufficient power

License

MIT

```
