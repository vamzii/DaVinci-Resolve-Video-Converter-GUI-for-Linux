#!/usr/bin/env python3
"""
Test script to demonstrate progress tracking functionality
"""

import subprocess
import time
import threading

def test_progress_tracking():
    """Test the progress tracking functionality"""
    print("Testing progress tracking functionality...")
    print("This will simulate a video conversion with progress updates.")
    
    # Simulate a 10-second conversion with progress updates
    duration = 10
    for i in range(duration):
        progress = (i / duration) * 100
        print(f"Converting test_video.mp4: {progress:.1f}%")
        time.sleep(1)
    
    print("✓ Conversion completed: test_video.mp4")

if __name__ == "__main__":
    test_progress_tracking() 