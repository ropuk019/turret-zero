#!/bin/bash

echo "=== Turret Zero Installation Script ==="

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get install -y python3-pip python3-opencv libatlas-base-dev libopenblas-dev gfortran python3-smbus i2c-tools

# Install Python requirements
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Download YOLO model
echo "Downloading YOLOv8 model..."
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Create necessary directories
echo "Creating data directories..."
mkdir -p data/photos data/logs

# Set permissions
chmod +x src/main.py

echo ""
echo "Installation complete!"
echo "Please configure your Telegram bot in config/settings.yaml"
echo "To test your hardware, run: python3 tools/test_system.py"
echo "To start the system, run: python3 src/main.py"
