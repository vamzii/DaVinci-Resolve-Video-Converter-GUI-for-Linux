#!/bin/bash

# DaVinci Resolve Video Converter Launcher
# This script launches the video converter application

echo "Starting DaVinci Resolve Video Converter..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if the main script exists
if [ ! -f "video_converter.py" ]; then
    echo "Error: video_converter.py not found in current directory"
    echo "Please run this script from the application directory"
    exit 1
fi

# Run the application
python3 video_converter.py 