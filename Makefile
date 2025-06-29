# Makefile for DaVinci Resolve Video Converter

.PHONY: all build clean install test help single

# Default target
all: build

# Build the standalone application
build:
	@echo "🚀 Building DaVinci Resolve Video Converter..."
	python3 build_standalone.py

# Build single executable
single:
	@echo "🚀 Building single executable DaVinci Resolve Video Converter..."
	python3 build_single_executable.py

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ build_single/ dist_single/
	rm -f *.tar.gz *.spec
	@echo "✅ Clean completed"

# Install dependencies
deps:
	@echo "📦 Installing Python dependencies..."
	pip3 install -r requirements.txt
	@echo "✅ Dependencies installed"

# Test the application
test:
	@echo "🧪 Running tests..."
	python3 test_converter.py
	@echo "✅ Tests completed"

# Install the built application
install: build
	@echo "📥 Installing application..."
	cd dist/DaVinciResolveConverter && ./install.sh

# Install the single executable
install-single: single
	@echo "📥 Installing single executable..."
	cd dist_single && ./install.sh

# Create development environment
dev: deps
	@echo "🔧 Setting up development environment..."
	@echo "✅ Development environment ready"
	@echo "Run 'python3 video_converter.py' to start the application"

# Show help
help:
	@echo "DaVinci Resolve Video Converter - Build System"
	@echo "=============================================="
	@echo ""
	@echo "Available targets:"
	@echo "  build         - Build standalone application with embedded FFmpeg"
	@echo "  single        - Build single executable with PyInstaller"
	@echo "  clean         - Remove build artifacts"
	@echo "  deps          - Install Python dependencies"
	@echo "  test          - Run application tests"
	@echo "  install       - Build and install the application"
	@echo "  install-single- Build and install single executable"
	@echo "  dev           - Set up development environment"
	@echo "  help          - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make build    # Build the application"
	@echo "  make single   # Build single executable"
	@echo "  make clean    # Clean build files"
	@echo "  make install  # Build and install"
	@echo "  make dev      # Set up for development"

# Show version information
version:
	@echo "DaVinci Resolve Video Converter"
	@echo "Version: 1.0.0"
	@echo "Python: $(shell python3 --version)"
	@echo "Platform: $(shell uname -s) $(shell uname -m)" 