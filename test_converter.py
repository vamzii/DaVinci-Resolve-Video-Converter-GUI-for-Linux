#!/usr/bin/env python3
"""
Test script for DaVinci Resolve Video Converter
This script tests the basic functionality without requiring actual video files
"""

import os
import subprocess
import sys
from pathlib import Path

def test_ffmpeg_installation():
    """Test if FFmpeg is properly installed"""
    print("Testing FFmpeg installation...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ FFmpeg is installed and working")
            return True
        else:
            print("✗ FFmpeg returned an error")
            return False
    except subprocess.TimeoutExpired:
        print("✗ FFmpeg command timed out")
        return False
    except FileNotFoundError:
        print("✗ FFmpeg not found. Please install FFmpeg first.")
        return False
    except Exception as e:
        print(f"✗ Error testing FFmpeg: {e}")
        return False

def test_python_dependencies():
    """Test if required Python modules are available"""
    print("\nTesting Python dependencies...")
    
    required_modules = ['tkinter', 'PIL', 'pathlib', 'subprocess', 'threading', 'json', 'datetime', 'queue']
    missing_modules = []
    
    for module in required_modules:
        try:
            if module == 'PIL':
                import PIL
            elif module == 'tkinter':
                import tkinter
            else:
                __import__(module)
            print(f"✓ {module} is available")
        except ImportError:
            print(f"✗ {module} is missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\nMissing modules: {', '.join(missing_modules)}")
        print("Please install missing dependencies: pip install -r requirements.txt")
        return False
    else:
        print("✓ All Python dependencies are available")
        return True

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    required_files = ['video_converter.py', 'requirements.txt', 'README.md', 'install.sh']
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} is missing")
            missing_files.append(file)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    else:
        print("✓ All required files are present")
        return True

def test_gui_import():
    """Test if the GUI can be imported without errors"""
    print("\nTesting GUI import...")
    try:
        # Import the main application
        sys.path.insert(0, os.getcwd())
        from video_converter import VideoConverter
        print("✓ VideoConverter class can be imported")
        return True
    except ImportError as e:
        print(f"✗ Error importing VideoConverter: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_format_configurations():
    """Test the format configurations"""
    print("\nTesting format configurations...")
    
    try:
        from video_converter import VideoConverter
        import tkinter as tk
        
        # Create a temporary root window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = VideoConverter(root)
        
        # Test format configurations - now includes MJPEG and H.264
        expected_formats = ['MJPEG', 'H.264']
        for format_name in expected_formats:
            if format_name in app.supported_formats:
                format_info = app.supported_formats[format_name]
                required_keys = ['extension', 'codec', 'profile', 'description']
                missing_keys = [key for key in required_keys if key not in format_info]
                
                if missing_keys:
                    print(f"✗ {format_name} missing keys: {missing_keys}")
                else:
                    print(f"✓ {format_name} configuration is complete")
            else:
                print(f"✗ {format_name} format not found")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Error testing format configurations: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("=== DaVinci Resolve Video Converter Test Suite ===\n")
    
    tests = [
        ("FFmpeg Installation", test_ffmpeg_installation),
        ("Python Dependencies", test_python_dependencies),
        ("File Structure", test_file_structure),
        ("GUI Import", test_gui_import),
        ("Format Configurations", test_format_configurations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! The application should work correctly.")
        print("\nYou can now run the application with:")
        print("python3 video_converter.py")
    else:
        print("✗ Some tests failed. Please fix the issues before running the application.")
        print("\nCommon solutions:")
        print("1. Install FFmpeg: sudo apt install ffmpeg (Ubuntu/Debian)")
        print("2. Install Python dependencies: pip install -r requirements.txt")
        print("3. Make sure all files are in the same directory")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 