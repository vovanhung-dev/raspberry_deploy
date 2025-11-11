#!/bin/bash

# Installation script for Hand Sign Detection Web App on Raspberry Pi

echo "======================================"
echo "Hand Sign Detection - Installation"
echo "======================================"
echo ""

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ]; then
    echo "Warning: This script is optimized for Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo "Step 1/5: Updating system packages..."
sudo apt update

# Install system dependencies
echo ""
echo "Step 2/5: Installing system dependencies..."
sudo apt install -y python3-pip python3-venv
sudo apt install -y libatlas-base-dev libhdf5-dev
sudo apt install -y python3-opencv

# Create virtual environment
echo ""
echo "Step 3/5: Creating Python virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo ""
echo "Step 4/5: Upgrading pip..."
pip install --upgrade pip

# Install Python packages
echo ""
echo "Step 5/5: Installing Python dependencies..."
echo "This may take 10-30 minutes depending on your internet speed..."
echo ""

# Ask user for installation type
echo "Choose installation type:"
echo "  1) Full (TensorFlow) - Recommended for Pi 5, ~800MB"
echo "  2) Lite (TFLite) - Faster install, ~100MB (requires model conversion)"
echo "  3) Minimal (OpenCV headless) - Lightest, ~500MB"
read -p "Enter choice (1/2/3): " choice

case $choice in
    1)
        echo "Installing full dependencies..."
        pip install Flask==3.0.0 Werkzeug==3.0.1
        pip install numpy==1.24.3
        pip install opencv-python==4.8.1.78
        pip install tensorflow==2.15.0
        ;;
    2)
        echo "Installing lite dependencies..."
        pip install Flask==3.0.0 Werkzeug==3.0.1
        pip install numpy==1.24.3
        pip install opencv-python-headless==4.8.1.78
        pip install tflite-runtime
        echo ""
        echo "Note: You need to convert the model to TFLite format!"
        ;;
    3)
        echo "Installing minimal dependencies..."
        pip install Flask==3.0.0 Werkzeug==3.0.1
        pip install numpy==1.24.3
        pip install opencv-python-headless==4.8.1.78
        pip install tensorflow==2.15.0
        ;;
    *)
        echo "Invalid choice. Installing full dependencies..."
        pip install -r requirements.txt
        ;;
esac

# Check installation
echo ""
echo "======================================"
echo "Verifying installation..."
python3 -c "import flask; import cv2; import numpy; print('Flask, OpenCV, NumPy: OK')"

if [ $choice -eq 2 ]; then
    python3 -c "import tflite_runtime; print('TFLite Runtime: OK')"
else
    python3 -c "import tensorflow; print('TensorFlow: OK')"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "Installation completed successfully!"
    echo "======================================"
    echo ""
    echo "To run the app:"
    echo "  ./run.sh"
    echo ""
    echo "Or manually:"
    echo "  source venv/bin/activate"
    echo "  python3 app.py"
    echo ""

    # Get IP address
    IP=$(hostname -I | awk '{print $1}')
    echo "After starting, access at:"
    echo "  http://$IP:5000"
    echo ""
else
    echo ""
    echo "======================================"
    echo "Installation completed with warnings!"
    echo "======================================"
    echo "Some packages may need manual installation."
    echo "Check the error messages above."
    echo ""
fi
