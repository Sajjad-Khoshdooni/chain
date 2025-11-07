#!/bin/bash

# Build script for Chain
# This script builds the project in different modes

set -e

echo "╔════════════════════════════════════════════════╗"
echo "║            Chain Build Script                  ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    print_error "Cargo is not installed. Please install Rust from https://rustup.rs/"
    exit 1
fi

print_info "Rust version: $(rustc --version)"
print_info "Cargo version: $(cargo --version)"
echo ""

# Parse arguments
BUILD_MODE=${1:-release}

case $BUILD_MODE in
    debug|dev)
        print_info "Building in DEBUG mode..."
        cargo build
        print_info "✓ Debug build completed!"
        print_info "Binary location: target/debug/chain"
        ;;
    release|prod)
        print_info "Building in RELEASE mode (optimized)..."
        cargo build --release
        print_info "✓ Release build completed!"
        print_info "Binary location: target/release/chain"
        ;;
    clean)
        print_info "Cleaning build artifacts..."
        cargo clean
        print_info "✓ Clean completed!"
        exit 0
        ;;
    test)
        print_info "Running tests..."
        cargo test
        print_info "✓ Tests completed!"
        exit 0
        ;;
    docker)
        print_info "Building Docker image..."
        docker build -t chain:latest .
        print_info "✓ Docker image built successfully!"
        print_info "Image: chain:latest"
        exit 0
        ;;
    *)
        print_error "Unknown build mode: $BUILD_MODE"
        echo "Usage: ./build.sh [debug|release|clean|test|docker]"
        echo "  debug   - Build in debug mode (faster compilation)"
        echo "  release - Build in release mode (optimized, default)"
        echo "  clean   - Clean build artifacts"
        echo "  test    - Run tests"
        echo "  docker  - Build Docker image"
        exit 1
        ;;
esac

echo ""
print_info "Build process completed successfully! 🎉"

