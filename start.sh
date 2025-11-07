#!/bin/bash

# Quick start script for Chain
# This script builds and runs the project with one command

set -e

echo "╔════════════════════════════════════════════════╗"
echo "║          Chain Quick Start Script              ║"
echo "╚════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Step 1: Build
print_step "Building Chain..."
./build.sh release

echo ""

# Step 2: Run
print_step "Running Chain..."
./run.sh native

print_info "All done! 🎉"

