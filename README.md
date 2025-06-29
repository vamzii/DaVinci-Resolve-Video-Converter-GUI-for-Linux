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
├── 🐍 run_converter.sh                    # Shell script to run the application
├── 📦 DaVinciResolveConverter-Executable.tar.gz  # Distribution package (133MB)
├── 📦 DaVinciResolveConverter.py         # PyInstaller single-file executable (203MB, 1,031 lines)
└── 📁 dist/                               # Distribution directory
    ├── 🚀 DaVinciResolveConverter        # Single executable (134MB)
    ├── 📄 davinci-resolve-converter.desktop # Desktop entry file
    └── 📄 install.sh                      # Installation script
```

## 🚀 Quick Start

### Option 1: PyInstaller Single-File Executable (Direct)
```bash
# Run the PyInstaller-generated single-file executable directly
./DaVinciResolveConverter.py

# Or with Python (if needed)
python3 DaVinciResolveConverter.py
```

### Option 2: Single Executable (Recommended for End Users)
```bash
# Download and extract
tar -xzf DaVinciResolveConverter-Executable.tar.gz
cd dist

# Install (creates desktop entry and adds to PATH)
./install.sh

# Or run directly without installation
./DaVinciResolveConverter
```

### Option 3: Development Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python3 video_converter.py

# Or use the shell script
./run_converter.sh
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

### PyInstaller Single-File Executable (`DaVinciResolveConverter.py`)
- **File**: `DaVinciResolveConverter.py`
- **Size**: 203MB
- **Type**: Python script with embedded PyInstaller executable
- **Lines**: 1,031 lines (mostly embedded binary data)
- **Usage**: Run directly with `./DaVinciResolveConverter.py`
- **Features**: Complete self-contained application with embedded FFmpeg

### Standalone Single Executable (`dist/DaVinciResolveConverter`)
- **File**: `dist/DaVinciResolveConverter`
- **Size**: 134MB
- **Type**: ELF 64-bit LSB executable
- **Architecture**: x86-64
- **Usage**: Run directly or install via `install.sh`
- **Features**: Same functionality, smaller size, better integration

### Distribution Package (`DaVinciResolveConverter-Executable.tar.gz`)
- **File**: `DaVinciResolveConverter-Executable.tar.gz`
- **Size**: 133MB (compressed)
- **Contents**: Standalone executable + installer + desktop entry
- **Usage**: Extract and install for end users
- **Features**: Complete distribution package with installation tools

## 📦 Installation Options

### Option 1: PyInstaller Executable (Direct)
```bash
# Make executable
chmod +x DaVinciResolveConverter.py

# Run directly
./DaVinciResolveConverter.py
```

### Option 2: Using Installer (Recommended)
```bash
# Extract the archive
tar -xzf DaVinciResolveConverter-Executable.tar.gz
cd dist

# Run installer
./install.sh
```

The installer will:
- Install to `~/.local/bin/DaVinciResolveConverter`
- Create desktop entry for easy launching
- Set up proper permissions
- Update desktop database

### Option 3: Direct Execution
```bash
# Extract and run directly
tar -xzf DaVinciResolveConverter-Executable.tar.gz
cd dist
chmod +x DaVinciResolveConverter
./DaVinciResolveConverter
```

### Option 4: Development Setup
```bash
# Clone or download source
git clone <repository-url>
cd linuxdavinciconverter

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python3 video_converter.py
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

## 🛠️ Build System

### Available Make Targets
```bash
make build          # Build standalone application with embedded FFmpeg
make single         # Build single executable with PyInstaller
make clean          # Remove build artifacts
make deps           # Install Python dependencies
make test           # Run application tests
make install        # Build and install the application
make install-single # Build and install single executable
make dev            # Set up development environment
make help           # Show help message
make version        # Show version information
```

### Building from Source
```bash
# Install PyInstaller
pip install pyinstaller

# Build single executable
pyinstaller --onefile --windowed --name=DaVinciResolveConverter DaVinciResolveConverter.py
```

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

### Executable Files
- **`DaVinciResolveConverter.py`**: PyInstaller-generated single-file executable (203MB, 1,031 lines)
  - Contains embedded Python interpreter, FFmpeg binaries, and all dependencies
  - Can be run directly: `./DaVinciResolveConverter.py`
  - Self-contained with no external dependencies
  - Larger size due to embedded Python interpreter

### Distribution Files
- **`DaVinciResolveConverter-Executable.tar.gz`**: Complete distribution package (133MB)
- **`dist/DaVinciResolveConverter`**: Standalone executable (134MB)
- **`dist/install.sh`**: Installation script with desktop integration
- **`dist/davinci-resolve-converter.desktop`**: Desktop entry file

## 🔄 Development Workflow

### Setting Up Development Environment
```bash
# Clone repository
git clone <repository-url>
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
tar -czf DaVinciResolveConverter-Executable.tar.gz dist/
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
- **PyInstaller Executable**: 1,031 lines (DaVinciResolveConverter.py)
- **Test Coverage**: 173 lines (test_converter.py) + 25 lines (test_progress.py)
- **Build System**: 81 lines (Makefile)
- **Documentation**: 157 lines (README.md)
- **Distribution Size**: 133MB (compressed), 134MB (standalone executable), 203MB (PyInstaller executable)

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