#!/bin/bash

# Run script for Chain
# This script runs the blockchain in different modes

set -e

echo "╔════════════════════════════════════════════════╗"
echo "║             Chain Run Script                   ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Parse arguments
RUN_MODE=${1:-native}

case $RUN_MODE in
    native|local)
        print_step "Running in NATIVE mode..."
        
        # Check if binary exists
        if [ -f "target/release/chain" ]; then
            print_info "Using release binary..."
            ./target/release/chain
        elif [ -f "target/debug/chain" ]; then
            print_info "Using debug binary..."
            ./target/debug/chain
        else
            print_warning "Binary not found. Building first..."
            cargo build --release
            ./target/release/chain
        fi
        ;;
    
    cargo|dev)
        print_step "Running with CARGO (development mode)..."
        cargo run --release
        ;;
    
    docker)
        print_step "Running in DOCKER container..."
        
        # Check if image exists
        if ! docker image inspect chain:latest &> /dev/null; then
            print_warning "Docker image not found. Building..."
            docker build -t chain:latest .
        fi
        
        print_info "Starting Docker container..."
        docker run --rm --name chain-instance chain:latest
        ;;
    
    docker-compose|compose)
        print_step "Running with DOCKER COMPOSE..."
        
        if ! command -v docker-compose &> /dev/null; then
            print_error "docker-compose is not installed."
            exit 1
        fi
        
        print_info "Building and starting services..."
        docker-compose up --build
        ;;
    
    docker-compose-bg|compose-bg)
        print_step "Running with DOCKER COMPOSE (background)..."
        
        if ! command -v docker-compose &> /dev/null; then
            print_error "docker-compose is not installed."
            exit 1
        fi
        
        print_info "Building and starting services in background..."
        docker-compose up --build -d
        print_info "✓ Services started!"
        print_info "View logs: docker-compose logs -f"
        print_info "Stop services: docker-compose down"
        ;;
    
    stop)
        print_step "Stopping Docker services..."
        docker-compose down
        print_info "✓ Services stopped!"
        ;;
    
    clean)
        print_step "Cleaning Docker resources..."
        docker-compose down --volumes --remove-orphans
        docker rmi chain:latest 2>/dev/null || true
        print_info "✓ Docker resources cleaned!"
        ;;
    
    *)
        print_error "Unknown run mode: $RUN_MODE"
        echo ""
        echo "Usage: ./run.sh [mode]"
        echo ""
        echo "Available modes:"
        echo "  native          - Run native binary (default)"
        echo "  cargo           - Run with cargo (development)"
        echo "  docker          - Run in Docker container"
        echo "  docker-compose  - Run with docker-compose"
        echo "  compose-bg      - Run docker-compose in background"
        echo "  stop            - Stop docker-compose services"
        echo "  clean           - Clean Docker resources"
        echo ""
        exit 1
        ;;
esac

echo ""
print_info "Execution completed! ✅"

