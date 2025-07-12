#!/bin/bash

# DaVinci Resolve Video Converter - Tools Downloader
# This script downloads all required tools for the video converter project

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}DaVinci Resolve Video Converter - Tools Downloader${NC}"
echo "=========================================================="
echo ""

# Function to check if a file exists
file_exists() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓ $1 already exists${NC}"
        return 0
    else
        return 1
    fi
}

# Function to download file with progress
download_file() {
    local url="$1"
    local filename="$2"
    local description="$3"
    
    echo -e "${YELLOW}📥 Downloading $description...${NC}"
    echo "URL: $url"
    
    if wget --progress=bar:force:noscroll -O "$filename" "$url"; then
        echo -e "${GREEN}✅ Downloaded $filename successfully${NC}"
        chmod +x "$filename"
        return 0
    else
        echo -e "${RED}❌ Failed to download $filename${NC}"
        return 1
    fi
}

# Function to check file size
check_file_size() {
    local filename="$1"
    local expected_size="$2"
    
    if [ -f "$filename" ]; then
        local actual_size=$(stat -c%s "$filename")
        if [ "$actual_size" -gt 0 ]; then
            echo -e "${GREEN}✓ $filename downloaded successfully (${actual_size} bytes)${NC}"
            return 0
        else
            echo -e "${RED}❌ $filename is empty or corrupted${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ $filename not found${NC}"
        return 1
    fi
}

# Create tools directory if it doesn't exist
mkdir -p tools

echo -e "${BLUE}🔍 Checking existing files...${NC}"
echo ""

# 1. Download appimagetool
echo -e "${BLUE}1. AppImage Tool${NC}"
if file_exists "appimagetool-x86_64.AppImage"; then
    echo "   File already exists, skipping download"
else
    APIMAGETOOL_URL="https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    if download_file "$APIMAGETOOL_URL" "appimagetool-x86_64.AppImage" "AppImage Tool"; then
        check_file_size "appimagetool-x86_64.AppImage" "8000000"
    fi
fi
echo ""

# 2. Download HandBrakeCLI
echo -e "${BLUE}2. HandBrake CLI${NC}"
if file_exists "HandBrakeCLI"; then
    echo "   File already exists, skipping download"
else
    # Try multiple sources for HandBrakeCLI
    HANDBRAKE_URLS=(
        "https://github.com/HandBrake/HandBrake/releases/download/1.7.3/HandBrakeCLI-1.7.3-x86_64"
        "https://github.com/HandBrake/HandBrake/releases/download/1.7.2/HandBrakeCLI-1.7.2-x86_64"
        "https://github.com/HandBrake/HandBrake/releases/download/1.7.1/HandBrakeCLI-1.7.1-x86_64"
        "https://github.com/HandBrake/HandBrake/releases/download/1.7.0/HandBrakeCLI-1.7.0-x86_64"
        "https://github.com/HandBrake/HandBrake/releases/download/1.6.1/HandBrakeCLI-1.6.1-x86_64"
        "https://github.com/HandBrake/HandBrake/releases/download/1.6.0/HandBrakeCLI-1.6.0-x86_64"
        "https://github.com/HandBrake/HandBrake/releases/download/1.5.1/HandBrakeCLI-1.5.1-x86_64"
        "https://github.com/HandBrake/HandBrake/releases/download/1.5.0/HandBrakeCLI-1.5.0-x86_64"
    )
    
    HANDBRAKE_DOWNLOADED=false
    for url in "${HANDBRAKE_URLS[@]}"; do
        echo "   Trying: $url"
        if download_file "$url" "HandBrakeCLI" "HandBrake CLI"; then
            if check_file_size "HandBrakeCLI" "1000000"; then
                HANDBRAKE_DOWNLOADED=true
                break
            else
                rm -f "HandBrakeCLI"
            fi
        fi
    done
    
    if [ "$HANDBRAKE_DOWNLOADED" = false ]; then
        echo -e "${YELLOW}⚠️  HandBrakeCLI download failed - providing manual instructions${NC}"
        echo ""
        echo -e "${BLUE}📋 Manual HandBrakeCLI Installation Options:${NC}"
        echo ""
        echo "Option 1: Install via package manager"
        echo "  Ubuntu/Debian: sudo apt install handbrake-cli"
        echo "  Fedora: sudo dnf install HandBrake-cli"
        echo "  Arch: sudo pacman -S handbrake-cli"
        echo ""
        echo "Option 2: Download from official website"
        echo "  Visit: https://handbrake.fr/downloads.php"
        echo "  Download the Linux CLI version"
        echo ""
        echo "Option 3: Use Flatpak (if available)"
        echo "  flatpak install fr.handbrake.HandBrake"
        echo ""
        echo -e "${YELLOW}Note: HandBrakeCLI is optional - the app will work with just Avidemux and FFmpeg${NC}"
        echo ""
    fi
fi
echo ""

# 3. Download Avidemux AppImage
echo -e "${BLUE}3. Avidemux AppImage${NC}"
if file_exists "avidemux_2.8.1.appImage"; then
    echo "   File already exists, skipping download"
else
    # Try multiple sources for Avidemux
    AVIDEMUX_URLS=(
        "https://github.com/mean00/avidemux2/releases/download/2.8.1/avidemux_2.8.1.appImage"
        "https://github.com/mean00/avidemux2/releases/download/2.8.0/avidemux_2.8.0.appImage"
        "https://github.com/mean00/avidemux2/releases/download/2.7.20/avidemux_2.7.20.appImage"
    )
    
    AVIDEMUX_DOWNLOADED=false
    for url in "${AVIDEMUX_URLS[@]}"; do
        echo "   Trying: $url"
        if download_file "$url" "avidemux_2.8.1.appImage" "Avidemux AppImage"; then
            if check_file_size "avidemux_2.8.1.appImage" "40000000"; then
                AVIDEMUX_DOWNLOADED=true
                break
            else
                rm -f "avidemux_2.8.1.appImage"
            fi
        fi
    done
    
    if [ "$AVIDEMUX_DOWNLOADED" = false ]; then
        echo -e "${RED}❌ Failed to download Avidemux from all sources${NC}"
        echo "   You may need to download it manually from:"
        echo "   https://github.com/mean00/avidemux2/releases"
    fi
fi
echo ""

# Summary
echo -e "${BLUE}📊 Download Summary${NC}"
echo "=========================="

if [ -f "appimagetool-x86_64.AppImage" ]; then
    echo -e "${GREEN}✓ AppImage Tool: $(stat -c%s appimagetool-x86_64.AppImage) bytes${NC}"
else
    echo -e "${RED}✗ AppImage Tool: Missing${NC}"
fi

if [ -f "HandBrakeCLI" ]; then
    echo -e "${GREEN}✓ HandBrakeCLI: $(stat -c%s HandBrakeCLI) bytes${NC}"
elif command -v HandBrakeCLI >/dev/null 2>&1; then
    echo -e "${GREEN}✓ HandBrakeCLI: System installed (available via package manager)${NC}"
else
    echo -e "${YELLOW}⚠ HandBrakeCLI: Optional - install manually if needed${NC}"
fi

if [ -f "avidemux_2.8.1.appImage" ]; then
    echo -e "${GREEN}✓ Avidemux AppImage: $(stat -c%s avidemux_2.8.1.appImage) bytes${NC}"
else
    echo -e "${RED}✗ Avidemux AppImage: Missing${NC}"
fi

echo ""
echo -e "${BLUE}🎯 Next Steps${NC}"
echo "================"
echo "1. Install Python dependencies: pip install -r requirements.txt"
echo "2. Run the application: python3 video_converter.py"
echo "3. Build AppImage: python3 create_appimage.py"
echo ""
echo -e "${GREEN}✅ Tools download completed!${NC}" 