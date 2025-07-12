# DaVinci Resolve Video Converter for Linux

A simple, modern Python GUI app to batch-convert videos into DaVinci Resolve–friendly formats (MJPEG, H.264, and more) on Linux. Build and run as an AppImage or from source.

---

## Features

- **Batch video conversion** (MJPEG, H.264)
- **Modern, easy-to-use GUI** (Tkinter)
- **Drag-and-drop, file browser, and clipboard support**
- **Progress bars and logs**
- **Smart filename conflict handling**
- **Works with HandBrakeCLI and Avidemux**

---

## Quick Start

### 1. Download Tools

```bash
./download_tools.sh
```
*This script fetches Avidemux and AppImage build tools. See below for HandBrakeCLI info.*

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
python3 video_converter.py
```

### 4. (Optional) Build AppImage

```bash
python3 create_appimage.py
```
The AppImage will appear in `dist_appimage/`.

---

## HandBrakeCLI Notice

HandBrakeCLI is **not auto-downloaded** (no official static binary).  
To use it, install via your package manager:

```bash
# Ubuntu/Debian
sudo apt install handbrake-cli

# Fedora
sudo dnf install HandBrake-cli

# Arch
sudo pacman -S handbrake-cli
```
Or see [handbrake.fr/downloads.php](https://handbrake.fr/downloads.php).

---

## Troubleshooting

- **HandBrakeCLI not found?**  
  Install it using your distro’s package manager (see above).
- **AppImage won’t run?**  
  `chmod +x DaVinciResolveConverter-x86_64.AppImage`
- **Conversion fails?**  
  Check input files, disk space, and output permissions.

---

## Contributing

Pull requests and issues are welcome!  
Tested on Ubuntu, but should work on any modern Linux.

---

**Made with ❤️ for the Linux video editing community.** 