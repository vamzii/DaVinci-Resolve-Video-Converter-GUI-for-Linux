# DaVinci Resolve Video Converter for Linux

A comprehensive GUI application to convert videos to formats compatible with DaVinci Resolve on Linux systems. This project provides both a development environment and a production-ready AppImage with embedded video processing tools.

## 🚀 Quick Start

### Option 1: Run from Source (Development)
```bash
# Download required tools
./download_tools.sh

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python3 video_converter.py
```

### Option 2: Use AppImage (Production)
```bash
# Build AppImage
python3 create_appimage.py

# Run the AppImage
./dist_appimage/DaVinciResolveConverter-x86_64.AppImage
```

## 📁 Project Structure

```
linuxdavinciconverter/
├── 📄 README.md                           # This documentation
├── 📄 requirements.txt                    # Python dependencies
├── 🐍 video_converter.py                  # Main GUI application
├── 🐍 create_appimage.py                  # AppImage builder
├── 🛠️ download_tools.sh                  # Tools downloader
├── 🛠️ avidemux_2.8.1.appImage            # Video conversion tool (43MB)
├── 🛠️ appimagetool-x86_64.AppImage       # AppImage creation tool (8.5MB)
└── 📦 dist_appimage/                      # AppImage output directory
    └── DaVinciResolveConverter-x86_64.AppImage
```

## ✨ Features

### 🎬 Video Conversion
- **Multiple Formats**: MJPEG (DaVinci Resolve compatible), H.264, custom FFmpeg parameters
- **Batch Processing**: Convert multiple videos simultaneously with individual selection
- **Progress Tracking**: Real-time progress updates with detailed logging
- **Stop Conversion**: Cancel ongoing conversions at any time
- **Conflict Resolution**: Smart filename conflict detection with multiple resolution options

### 🖥️ User Interface
- **Modern GUI**: Clean, intuitive tkinter interface with dark/light themes
- **Context Menus**: Right-click for copy/paste directory operations
- **Undo/Redo**: Support for directory field operations
- **Clipboard Integration**: Copy/paste directory paths
- **File Browser**: Native file dialogs for directory selection
- **Real-time Updates**: Live progress bars and status updates

### 🔧 Technical Features
- **Self-Contained**: AppImage with embedded tools (no system dependencies)
- **Cross-Platform**: Works on any Linux distribution
- **Multiple Engines**: FFmpeg, Avidemux, and HandBrakeCLI support
- **Desktop Integration**: Appears in applications menu with proper icon
- **Error Handling**: Comprehensive error handling and user feedback

## 🎯 Supported Formats & Tools

### Output Formats
- **MJPEG**: DaVinci Resolve compatible format (recommended for editing)
- **H.264**: Universal playback format (good for distribution)
- **Custom**: User-defined FFmpeg parameters for advanced users

### Conversion Engines
- **FFmpeg**: Primary conversion engine (system or embedded)
- **Avidemux**: Alternative conversion tool (embedded AppImage)
- **HandBrakeCLI**: High-quality conversion tool (system installation)

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.6+** (for development)
- **FFmpeg** (system installation or embedded in AppImage)
- **Required Python packages** (see requirements.txt)

### Automated Setup

The `download_tools.sh` script automatically downloads most required tools:

```bash
./download_tools.sh
```

This script will download:
- ✅ **AppImage Tool** (for building AppImages)
- ✅ **Avidemux AppImage** (video converter)
- ⚠️ **HandBrakeCLI** (provides manual installation instructions)

### HandBrakeCLI Installation

Due to changes in HandBrake's distribution model, the CLI tool is no longer available as a standalone download. The script provides manual installation options:

#### Option 1: Package Manager (Recommended)
```bash
# Ubuntu/Debian
sudo apt install handbrake-cli

# Fedora
sudo dnf install HandBrake-cli

# Arch Linux
sudo pacman -S handbrake-cli
```

#### Option 2: Official Website
Visit https://handbrake.fr/downloads.php and download the Linux CLI version

#### Option 3: Flatpak
```bash
flatpak install fr.handbrake.HandBrake
```

**Note**: HandBrakeCLI is optional - the application works perfectly with just Avidemux and FFmpeg.

### Manual Setup
```bash
# Clone the repository
git clone <repository-url>
cd linuxdavinciconverter

# Download required tools
./download_tools.sh

# Install Python dependencies
pip install -r requirements.txt

# Run the application
python3 video_converter.py
```

## 🎮 Usage Guide

### Basic Workflow
1. **Select Input Directory**: Choose the folder containing your videos
2. **Select Output Directory**: Choose where to save converted videos
3. **Choose Format**: Select your preferred output format (MJPEG or H.264)
4. **Select Videos**: Check/uncheck videos you want to convert
5. **Start Conversion**: Click "Start Conversion" to begin
6. **Monitor Progress**: Watch real-time progress and logs
7. **Stop if Needed**: Use "Stop Conversion" to cancel

### Advanced Features
- **Custom FFmpeg Parameters**: Define your own conversion settings
- **Batch Selection**: Select/deselect all videos at once
- **Progress Details**: View detailed conversion output in real-time
- **Conflict Resolution**: Handle filename conflicts with multiple options
- **Directory History**: Undo/redo directory path changes

### Format Recommendations
- **For DaVinci Resolve**: Use MJPEG format for best compatibility
- **For Distribution**: Use H.264 format for smaller file sizes
- **For Custom Needs**: Use custom FFmpeg parameters

## 📦 Distribution Options

### AppImage (Recommended for End Users)
- **File**: `DaVinciResolveConverter-x86_64.AppImage`
- **Size**: ~43MB
- **Features**: Self-contained with all tools embedded
- **Usage**: Download and run directly (no installation required)
- **Build**: `python3 create_appimage.py`

### Source Distribution (Recommended for Developers)
- **Files**: All source files and tools
- **Size**: ~53MB
- **Features**: Full development environment
- **Usage**: Clone and run with Python
- **Benefits**: Easy to modify and extend

## 🐛 Troubleshooting

### Common Issues

#### FFmpeg Not Found
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch
sudo pacman -S ffmpeg
```
*Note: The AppImage includes embedded FFmpeg*

#### Python Dependencies Missing
```bash
pip install -r requirements.txt
```

#### AppImage Won't Run
```bash
# Make executable
chmod +x DaVinciResolveConverter-x86_64.AppImage

# Check AppImage support
./DaVinciResolveConverter-x86_64.AppImage --appimage-extract-and-run
```

#### Conversion Fails
- Ensure input videos are valid and not corrupted
- Check available disk space in output directory
- Verify output directory has write permissions
- Check system resources (CPU, memory) during conversion

#### HandBrakeCLI Issues
- Verify installation: `HandBrakeCLI --version`
- Reinstall via package manager if needed
- HandBrakeCLI is optional - app works with just Avidemux and FFmpeg

### Debug Mode
Run with verbose logging:
```bash
python3 video_converter.py --debug
```

## 🔧 Development

### Building AppImage
```bash
# Ensure all tools are downloaded
./download_tools.sh

# Build AppImage
python3 create_appimage.py

# The AppImage will be created in dist_appimage/
```

### Testing
```bash
# Run the application
python3 video_converter.py

# Test with sample videos
python3 test_converter.py
```

### Project Structure
- `video_converter.py`: Main GUI application
- `create_appimage.py`: AppImage builder
- `download_tools.sh`: Tools downloader
- `requirements.txt`: Python dependencies
- `avidemux_2.8.1.appImage`: Embedded video converter
- `appimagetool-x86_64.AppImage`: AppImage creation tool

## 📝 License

This project is open source. See the repository for license details.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Submit issues and feature requests
- Create pull requests with improvements
- Help with documentation
- Test on different Linux distributions

## 📞 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the application logs for error details
3. Search existing issues on the repository
4. Submit a new issue with detailed information

### Getting Help
- **Application Logs**: Check the detailed output in the GUI
- **System Requirements**: Ensure you have the required tools installed
- **Format Issues**: Try different output formats if conversion fails
- **Performance**: Close other applications during large batch conversions

---

**Made with ❤️ for the Linux video editing community** 