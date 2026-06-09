# Turret Zero

A simple air defence spotting system anyone can build for under $150.

## Overview
Turret Zero uses a Raspberry Pi, a rotating mount, and computer vision (YOLOv8) to scan the sky for aircraft. When an aircraft is detected, the system calculates its GPS coordinates, predicts its flight path, and sends an alert with a photo to your Telegram bot.

## Parts List
- Raspberry Pi 4 (2GB+) - $45
- Raspberry Pi Camera Module / USB Webcam - $25
- Continuous rotation servo motor (FS90R) - $8
- GPS module (NEO-6M) - $12
- MPU6050 gyroscope sensor - $3
- Lazy Susan bearing (6 inch) - $5
- PVC pipe & T-joint - $5
- Wooden board (12x12") - $5
- Jumper wires & power supplies - $20
- MicroSD card (32GB) - $8
- **Total: ~$140**

## Wiring Diagram
- **Servo Motor:** 
  - Red: 5V (External)
  - Brown: GND
  - Orange: GPIO 18 (Pi)
- **GPS Module:**
  - VCC: 3.3V
  - GND: GND
  - TX: RX (GPIO 15)
  - RX: TX (GPIO 14)
- **MPU6050 Gyro:**
  - VCC: 3.3V
  - GND: GND
  - SDA: SDA (GPIO 2)
  - SCL: SCL (GPIO 3)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/turret-zero
   cd turret-zero
   ```
2. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

## Configuration
1. Create a Telegram bot using [@BotFather](https://t.me/botfather).
2. Get your chat ID using [@userinfobot](https://t.me/userinfobot).
3. Edit `config/settings.yaml`:
   - Set `simulation_mode: false` (when on hardware).
   - Enter your `bot_token` and `chat_id`.
   - Set `enabled: true`.

## Running the System
1. Test your hardware:
   ```bash
   python3 tools/test_system.py
   ```
2. Start the scanner:
   ```bash
   python3 src/main.py
   ```

## Project Structure
- `src/`: Core logic and hardware interfaces.
- `config/`: System settings.
- `tools/`: Diagnostic tools.
- `data/`: Saved photos and logs.

## License
MIT
