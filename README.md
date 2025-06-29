# DaVinci Resolve Video Converter for Linux

A comprehensive GUI application to convert videos to formats compatible with DaVinci Resolve on Linux systems. This project provides both a development environment and a production-ready single executable.

## 📁 Project Structure

```
linuxdavinciconverter/
├── 📄 README.md                           # This comprehensive documentation
├── 📄 Makefile                            # Build system with multiple targets
├── 📄 requirements.txt                    # Python dependencies (Pillow, pyperclip)
├── 📄 .gitignore                          # Git ignore patterns
├── 🐍 video_converter.py                  # Main GUI application (42KB, 980 lines)
├── 🐍 test_converter.py                   # Application tests (5.7KB, 173 lines)
├── 🐍 test_progress.py                    # Progress tracking tests (702B, 25 lines)
└── 🐍 run_converter.sh                    # Shell script to run the application
```

**Note**: Large executable files are not included in this repository due to GitHub's file size limits. See the [Releases](https://github.com/vamzii/linuxdavinciconverter/releases) section for downloadable executables.

## 🚀 Quick Start

### Option 1: Download from GitHub Releases (Recommended)
1. Go to [Releases](https://github.com/vamzii/linuxdavinciconverter/releases)
2. Download `DaVinciResolveConverter-v1.0.0.tar.gz`
3. Extract and install:
   ```bash
   tar -xzf DaVinciResolveConverter-v1.0.0.tar.gz
   cd dist
   ./install.sh
   ```

### Option 2: Development Environment
```bash
# Clone the repository
git clone https://github.com/vamzii/linuxdavinciconverter.git
cd linuxdavinciconverter

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 video_converter.py

# Or use the shell script
./run_converter.sh
```

### Option 3: Build Your Own Executable
```bash
# Clone the repository
git clone https://github.com/vamzii/linuxdavinciconverter.git
cd linuxdavinciconverter

# Install dependencies and PyInstaller
pip install -r requirements.txt
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name=DaVinciResolveConverter video_converter.py

# Run the built executable
./dist/DaVinciResolveConverter
```

## ✨ Features

### 🎬 Video Conversion
- **Multiple Formats**: DNxHD, ProRes, H.264, H.265/HEVC, MJPEG, custom FFmpeg parameters
- **Batch Processing**: Convert multiple videos simultaneously
- **Progress Tracking**: Real-time progress updates with detailed FFmpeg logging
- **Stop Conversion**: Cancel ongoing conversions at any time
- **Individual Selection**: Checkbox selection for specific videos
- **Conflict Resolution**: Smart filename conflict detection with options (overwrite, skip, suffix, timestamp)

### 🖥️ User Interface
- **Modern GUI**: Clean, intuitive tkinter interface
- **Context Menus**: Right-click for copy/paste directory operations
- **Undo/Redo**: Support for directory field operations
- **Clipboard Integration**: Copy/paste directory paths
- **File Browser**: Native file dialogs for directory selection
- **Real-time Updates**: Live progress bars and status updates

### 🔧 Technical Features
- **Self-Contained**: Single executable with embedded Python and FFmpeg
- **Cross-Platform**: Works on any Linux distribution
- **No Dependencies**: Everything included in the executable
- **Desktop Integration**: Appears in applications menu
- **Error Handling**: Comprehensive error handling and user feedback

## 🎯 Executable Versions

### Distribution Package (Available in Releases)
- **File**: `DaVinciResolveConverter-v1.0.0.tar.gz`
- **Size**: 133MB (compressed)
- **Contents**: Standalone executable + installer + desktop entry
- **Usage**: Download from [GitHub Releases](https://github.com/vamzii/linuxdavinciconverter/releases)
- **Features**: Complete distribution package with installation tools

### Built Executable
- **File**: `DaVinciResolveConverter` (created when building)
- **Size**: ~134MB
- **Type**: ELF 64-bit LSB executable
- **Architecture**: x86-64
- **Usage**: Run directly or install via `install.sh`
- **Features**: Self-contained with embedded Python and FFmpeg

## 📦 Installation Options

### Option 1: Download from GitHub Releases (Recommended)
```bash
# Download from releases page
# Extract the archive
tar -xzf DaVinciResolveConverter-v1.0.0.tar.gz
cd dist

# Install (creates desktop entry and adds to PATH)
./install.sh

# Or run directly without installation
./DaVinciResolveConverter
```

### Option 2: Development Environment
```bash
# Clone the repository
git clone https://github.com/vamzii/linuxdavinciconverter.git
cd linuxdavinciconverter

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 video_converter.py
```

### Option 3: Build Your Own Executable
```bash
# Clone the repository
git clone https://github.com/vamzii/linuxdavinciconverter.git
cd linuxdavinciconverter

# Install dependencies and PyInstaller
pip install -r requirements.txt
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name=DaVinciResolveConverter video_converter.py

# Run the built executable
./dist/DaVinciResolveConverter
```

## 🎮 Usage Guide

### Basic Workflow
1. **Select Input Directory**: Choose the folder containing your videos
2. **Select Output Directory**: Choose where to save converted videos
3. **Choose Format**: Select your preferred output format
4. **Select Videos**: Check/uncheck videos you want to convert
5. **Start Conversion**: Click "Start Conversion" to begin
6. **Monitor Progress**: Watch real-time progress and logs
7. **Stop if Needed**: Use "Stop Conversion" to cancel

### Advanced Features
- **Custom FFmpeg Parameters**: Define your own conversion settings
- **Batch Selection**: Select/deselect all videos at once
- **Progress Details**: View detailed FFmpeg output in real-time
- **Conflict Resolution**: Handle filename conflicts with multiple options
- **Directory History**: Undo/redo directory path changes

## 🎬 Supported Formats

### Professional Formats
- **DNxHD**: Avid's professional editing format
- **ProRes**: Apple's professional format
- **DNxHR**: High-resolution DNx format

### Consumer Formats
- **H.264**: Widely compatible format
- **H.265/HEVC**: High efficiency format
- **MJPEG**: Motion JPEG format

### Custom Format
- **Custom FFmpeg**: Define your own parameters for maximum flexibility

## 🛠️ Building from Source

To create the executable file from the repository files, follow these steps:

#### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install PyInstaller
pip install pyinstaller
```

#### Step 1: Create the Executable
```bash
# Build single executable with PyInstaller
pyinstaller --onefile --windowed --name=DaVinciResolveConverter video_converter.py
```

This command creates a single executable file that includes:
- **Python Interpreter**: Embedded Python runtime
- **Application Code**: Your `video_converter.py` application  
- **Dependencies**: All required Python packages (Pillow, pyperclip, tkinter)
- **FFmpeg**: Embedded FFmpeg binaries for video conversion
- **System Libraries**: Required system libraries and dependencies

#### Step 2: Create Distribution Package
```bash
# Create dist directory structure
mkdir -p dist

# Copy the PyInstaller executable
cp dist/DaVinciResolveConverter dist/

# Create desktop entry file
cat > dist/davinci-resolve-converter.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=DaVinci Resolve Video Converter
Comment=Convert videos to DaVinci Resolve compatible formats
Exec=DaVinciResolveConverter
Icon=video-x-generic
Terminal=false
Categories=AudioVideo;Video;GTK;
EOF

# Create installer script
cat > dist/install.sh << 'EOF'
#!/bin/bash
# DaVinci Resolve Video Converter - Executable Installer

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}DaVinci Resolve Video Converter - Executable Installer${NC}"
echo "=========================================================="

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}Warning: Running as root. This is not recommended.${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Default installation directory
INSTALL_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Create installation directory
echo "Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy executable
echo "Installing executable..."
cp DaVinciResolveConverter "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/DaVinciResolveConverter"

# Create desktop entry
echo "Creating desktop entry..."
cp davinci-resolve-converter.desktop "$DESKTOP_DIR/"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR"
fi

echo -e "${GREEN}Installation completed successfully!${NC}"
echo ""
echo "You can now:"
echo "1. Launch the application from your applications menu"
echo "2. Run it from terminal: $INSTALL_DIR/DaVinciResolveConverter"
echo "3. Uninstall by deleting: $INSTALL_DIR/DaVinciResolveConverter"
echo ""
echo "This is a single executable file with everything included!"
echo "No Python, FFmpeg, or other dependencies needed!"
EOF

# Make installer executable
chmod +x dist/install.sh

# Create distribution archive
cd dist
tar -czf DaVinciResolveConverter-v1.0.0.tar.gz DaVinciResolveConverter davinci-resolve-converter.desktop install.sh
cd ..
```

#### Step 3: Verify the Build
```bash
# Test the executable
./dist/DaVinciResolveConverter

# Check file information
file dist/DaVinciResolveConverter

# Check dependencies (should show minimal dependencies)
ldd dist/DaVinciResolveConverter
```

#### Alternative: Using Makefile
```bash
# Build using the provided Makefile
make single
```

#### Build Output
After running the build process, you'll have:
```
dist/
├── DaVinciResolveConverter          # Single executable (134MB)
├── davinci-resolve-converter.desktop # Desktop entry file
├── install.sh                       # Installation script
└── DaVinciResolveConverter-v1.0.0.tar.gz # Distribution package (133MB)
```

#### Troubleshooting
- **Large file size (134MB)**: Normal due to embedded Python and FFmpeg
- **Permission issues**: Run `chmod +x dist/DaVinciResolveConverter`
- **Missing dependencies**: Install with `pip install -r requirements.txt`

## 🧪 Testing

### Test Files
- **`test_converter.py`**: Main application tests (5.7KB, 173 lines)
- **`test_progress.py`**: Progress tracking functionality tests (702B, 25 lines)

### Running Tests
```bash
# Run all tests
make test

# Run specific test
python3 test_converter.py
python3 test_progress.py
```

## 📋 System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+, etc.)
- **Architecture**: x86-64 (64-bit)
- **RAM**: 512MB minimum, 2GB recommended
- **Storage**: 150MB for application + space for video files
- **Display**: X11 or Wayland with GUI support

### Recommended Requirements
- **OS**: Ubuntu 22.04+, Debian 12+, or newer
- **RAM**: 4GB or more
- **Storage**: SSD with 1GB+ free space
- **CPU**: Multi-core processor for faster conversions

## 🐛 Troubleshooting

### Common Issues

**Permission Denied**
```bash
chmod +x DaVinciResolveConverter
```

**Desktop Entry Not Working**
```bash
update-desktop-database ~/.local/share/applications/
```

**Application Not Starting**
- Check if you have GUI support (X11/Wayland)
- Try running from terminal to see error messages
- Verify the executable is not corrupted

**FFmpeg Not Found**
- The single executable includes FFmpeg, so this shouldn't happen
- If using development version, install FFmpeg: `sudo apt install ffmpeg`

### Debug Mode
```bash
# Run with verbose output
./DaVinciResolveConverter --debug

# Check executable information
file DaVinciResolveConverter
ldd DaVinciResolveConverter
```

## 📁 File Details

### Source Files
- **`video_converter.py`**: Main application with GUI, video processing, and all features
- **`test_converter.py`**: Comprehensive test suite for application functionality
- **`test_progress.py`**: Progress tracking and conversion simulation tests
- **`run_converter.sh`**: Convenient shell script to launch the application

### Build Files
- **`Makefile`**: Complete build system with multiple targets
- **`requirements.txt`**: Python dependencies (Pillow, pyperclip)
- **`.gitignore`**: Git ignore patterns for build artifacts

### Distribution Files (Available in Releases)
- **`DaVinciResolveConverter-v1.0.0.tar.gz`**: Complete distribution package (133MB)
  - Contains standalone executable, installer, and desktop entry
  - Download from [GitHub Releases](https://github.com/vamzii/linuxdavinciconverter/releases)

## 🔄 Development Workflow

### Setting Up Development Environment
```bash
# Clone repository
git clone https://github.com/vamzii/linuxdavinciconverter.git
cd linuxdavinciconverter

# Set up development environment
make dev

# Run application
python3 video_converter.py
```

### Making Changes
1. Edit `video_converter.py` for main application changes
2. Update tests in `test_converter.py` and `test_progress.py`
3. Test your changes: `make test`
4. Build new executable: `make single`
5. Test the executable: `./dist/DaVinciResolveConverter`

### Building Distribution Package
```bash
# Build single executable
make single

# Create distribution package
tar -czf DaVinciResolveConverter-v1.0.0.tar.gz dist/
```

## 🤝 Contributing

### Development Guidelines
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `make test`
6. Test the executable: `make single && ./dist/DaVinciResolveConverter`
7. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Add docstrings for functions and classes
- Include type hints where appropriate
- Write comprehensive tests for new features

## 📄 License

This project is open source. See LICENSE file for details.

## 🆘 Support

### Getting Help
1. Check this README first
2. Review the troubleshooting section
3. Check existing issues on GitHub
4. Open a new issue with detailed information

### Issue Reporting
When reporting issues, please include:
- Operating system and version
- Application version (development or executable)
- Steps to reproduce the problem
- Error messages or logs
- System specifications

## 📊 Project Statistics

- **Total Lines of Code**: ~1,200+ lines
- **Main Application**: 980 lines (video_converter.py)
- **Test Coverage**: 173 lines (test_converter.py) + 25 lines (test_progress.py)
- **Build System**: 81 lines (Makefile)
- **Documentation**: 157 lines (README.md)
- **Repository Size**: ~50KB (source code only)
- **Distribution Size**: 133MB (available in releases)

## 🎯 Roadmap

### Planned Features
- [ ] Support for more video formats
- [ ] Audio-only conversion options
- [ ] Preset management system
- [ ] Batch job scheduling
- [ ] Cloud storage integration
- [ ] Multi-language support

### Performance Improvements
- [ ] GPU acceleration support
- [ ] Parallel processing optimization
- [ ] Memory usage optimization
- [ ] Startup time improvement

---

**🎬 Convert your videos to DaVinci Resolve compatible formats with ease!**

*This project provides a complete solution for video conversion, from development environment to production-ready single executable.* 