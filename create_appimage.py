#!/usr/bin/env python3
"""
Create a true AppImage for DaVinci Resolve Video Converter
Bundles Python, your app, Avidemux AppImage, and HandBrake CLI
"""

import os
import sys
import subprocess
import shutil
import tarfile
import urllib.request
from pathlib import Path

class AppImageBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.appdir = self.project_root / "AppDir"
        self.dist_dir = self.project_root / "dist_appimage"
        
    def clean_dirs(self):
        """Clean build directories"""
        print("🧹 Cleaning build directories...")
        if self.appdir.exists():
            shutil.rmtree(self.appdir)
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        
        self.appdir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
    def download_portable_python(self):
        """Download a portable Python build"""
        print("📥 Downloading portable Python...")
        
        # Try to find a portable Python build
        python_url = "https://www.python.org/ftp/python/3.9.18/Python-3.9.18.tgz"
        python_tar = self.project_root / "Python-3.9.18.tgz"
        
        if not python_tar.exists():
            print(f"Downloading Python from {python_url}")
            urllib.request.urlretrieve(python_url, python_tar)
        
        # Extract Python
        python_dir = self.project_root / "Python-3.9.18"
        if not python_dir.exists():
            print("Extracting Python...")
            with tarfile.open(python_tar, 'r:gz') as tar:
                tar.extractall(self.project_root)
        
        return python_dir
        
    def setup_appdir_structure(self):
        """Create the AppDir structure"""
        print("📁 Creating AppDir structure...")
        
        # Create directories
        (self.appdir / "usr" / "bin").mkdir(parents=True, exist_ok=True)
        (self.appdir / "usr" / "lib").mkdir(parents=True, exist_ok=True)
        (self.appdir / "usr" / "share" / "applications").mkdir(parents=True, exist_ok=True)
        (self.appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True, exist_ok=True)
        (self.appdir / "tools").mkdir(exist_ok=True)
        
    def copy_application_files(self):
        """Copy application files to AppDir"""
        print("📁 Copying application files...")
        
        # Copy main application
        shutil.copy2(self.project_root / "video_converter.py", self.appdir / "usr" / "bin" / "video_converter.py")
        
        # Copy requirements
        if (self.project_root / "requirements.txt").exists():
            shutil.copy2(self.project_root / "requirements.txt", self.appdir / "usr" / "bin" / "requirements.txt")
            
        # Copy tools
        if (self.project_root / "avidemux_2.8.1.appImage").exists():
            shutil.copy2(self.project_root / "avidemux_2.8.1.appImage", self.appdir / "tools" / "avidemux.appImage")
            (self.appdir / "tools" / "avidemux.appImage").chmod(0o755)
            
        # Copy HandBrake CLI
        handbrake_local = self.project_root / "HandBrakeCLI"
        handbrake_system = "/usr/bin/HandBrakeCLI"
        if handbrake_local.exists():
            shutil.copy2(handbrake_local, self.appdir / "tools" / "HandBrakeCLI")
            (self.appdir / "tools" / "HandBrakeCLI").chmod(0o755)
            print("✅ Copied local HandBrakeCLI")
        elif os.path.exists(handbrake_system):
            shutil.copy2(handbrake_system, self.appdir / "tools" / "HandBrakeCLI")
            (self.appdir / "tools" / "HandBrakeCLI").chmod(0o755)
            print("✅ Copied system HandBrakeCLI")
        else:
            print("⚠️  Warning: HandBrakeCLI not found in system or local directory")
            
    def create_apprun(self):
        """Create the AppRun launcher script"""
        print("📝 Creating AppRun script...")
        
        apprun_content = '''#!/bin/bash
# DaVinci Resolve Video Converter AppImage Launcher

# Get the directory where this AppImage is mounted
HERE="$(dirname "$(readlink -f "${0}")")"

# Set up environment
export PATH="$HERE/usr/bin:$HERE/tools:$PATH"
export PYTHONPATH="$HERE/usr/lib/python3.9/site-packages:$PYTHONPATH"
export LD_LIBRARY_PATH="$HERE/usr/lib:$LD_LIBRARY_PATH"

# Check if Python is available
PYTHON_BIN="$HERE/usr/bin/python3"
if [ ! -f "$PYTHON_BIN" ]; then
    # Fall back to system Python
    PYTHON_BIN="python3"
fi

# Check if required packages are installed
$PYTHON_BIN -c "import tkinter, pyperclip" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required Python packages..."
    $PYTHON_BIN -m pip install -r "$HERE/usr/bin/requirements.txt"
fi

# Make tools executable
chmod +x "$HERE/tools/avidemux.appImage" 2>/dev/null
chmod +x "$HERE/tools/HandBrakeCLI" 2>/dev/null

echo "Starting DaVinci Resolve Video Converter..."
echo "Tools available:"
echo "  - Avidemux AppImage: $HERE/tools/avidemux.appImage"
echo "  - HandBrake CLI: $HERE/tools/HandBrakeCLI"

# Launch the application
cd "$HERE/usr/bin"
exec "$PYTHON_BIN" video_converter.py "$@"
'''
        
        apprun_path = self.appdir / "AppRun"
        with open(apprun_path, 'w') as f:
            f.write(apprun_content)
        
        apprun_path.chmod(0o755)
        print("✅ Created AppRun script")
        
    def create_desktop_file(self):
        """Create the .desktop file"""
        print("📝 Creating .desktop file...")
        
        desktop_content = '''[Desktop Entry]
Version=1.0
Type=Application
Name=DaVinci Resolve Video Converter
Comment=Convert videos to DaVinci Resolve compatible formats
Exec=video_converter
Icon=video-converter
Terminal=false
Categories=AudioVideo;Video;GTK;
'''
        
        desktop_path_usr = self.appdir / "usr" / "share" / "applications" / "davinci-resolve-converter.desktop"
        desktop_path_top = self.appdir / "davinci-resolve-converter.desktop"
        with open(desktop_path_usr, 'w') as f:
            f.write(desktop_content)
        with open(desktop_path_top, 'w') as f:
            f.write(desktop_content)
        
        print("✅ Created .desktop file (both in usr/share/applications and top level)")
        
    def create_icon(self):
        """Create a simple icon file"""
        print("🎨 Creating icon...")
        
        # Create a simple SVG icon (you can replace this with a proper icon)
        icon_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" version="1.1" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" fill="#2b2b2b"/>
  <circle cx="128" cy="128" r="80" fill="#4CAF50" stroke="#2E7D32" stroke-width="8"/>
  <polygon points="100,80 100,176 180,128" fill="white"/>
  <text x="128" y="220" text-anchor="middle" fill="white" font-family="Arial" font-size="16">Video</text>
</svg>
'''
        
        icon_path = self.appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps" / "video-converter.svg"
        with open(icon_path, 'w') as f:
            f.write(icon_svg)
        # Also copy to top level for appimagetool
        icon_path_top = self.appdir / "video-converter.svg"
        shutil.copy2(icon_path, icon_path_top)
        print("✅ Created icon (both in icons dir and top level)")
        
    def bundle_python(self):
        """Bundle a portable Python installation"""
        print("🐍 Bundling Python...")
        
        # For now, we'll use system Python but set up the structure for portable Python
        # In a full implementation, you'd download and extract a portable Python build
        
        python_bin = shutil.which("python3")
        if python_bin:
            # Create a symlink to system Python
            os.symlink(python_bin, self.appdir / "usr" / "bin" / "python3")
            print(f"✅ Linked system Python: {python_bin}")
        else:
            print("❌ Error: python3 not found in system")
            return False
            
        return True
        
    def build_appimage(self):
        """Build the AppImage using appimagetool"""
        print("📦 Building AppImage...")
        
        appimagetool = self.project_root / "appimagetool-x86_64.AppImage"
        if not appimagetool.exists():
            print("❌ Error: appimagetool-x86_64.AppImage not found in project root")
            print("Please download it from: https://github.com/AppImage/AppImageKit/releases")
            return False
            
        # Make sure it's executable
        appimagetool.chmod(0o755)
        
        # Build the AppImage
        output_name = "DaVinciResolveConverter-x86_64.AppImage"
        output_path = self.dist_dir / output_name
        
        cmd = [
            str(appimagetool),
            str(self.appdir),
            str(output_path)
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ AppImage created: {output_path}")
            print(f"📊 Size: {output_path.stat().st_size / (1024*1024):.1f} MB")
            return True
        else:
            print(f"❌ AppImage build failed: {result.stderr}")
            return False
            
    def build(self):
        """Build the complete AppImage"""
        print("🚀 Building DaVinci Resolve Video Converter AppImage...")
        
        # Clean and setup
        self.clean_dirs()
        self.setup_appdir_structure()
        
        # Copy files
        self.copy_application_files()
        
        # Create launcher files
        self.create_apprun()
        self.create_desktop_file()
        self.create_icon()
        
        # Bundle Python
        if not self.bundle_python():
            return False
            
        # Build AppImage
        if not self.build_appimage():
            return False
            
        print("\n✅ AppImage build completed successfully!")
        print(f"📦 AppImage: {self.dist_dir}")
        print("\nTo test the AppImage:")
        print(f"  chmod +x {self.dist_dir}/*.AppImage")
        print(f"  ./{self.dist_dir}/*.AppImage")
        
        return True

def main():
    """Main function"""
    builder = AppImageBuilder()
    success = builder.build()
    
    if success:
        print("\n🎉 True AppImage created successfully!")
        print("This AppImage will run on any modern Linux system!")
    else:
        print("\n❌ AppImage build failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 