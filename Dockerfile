# Multi-stage Docker build for Chain
# Stage 1: Build the application
FROM rust:1.75-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a new empty project
WORKDIR /usr/src/chain

# Copy manifests
COPY Cargo.toml Cargo.lock ./

# Copy source code
COPY src ./src

# Build for release
RUN cargo build --release

# Stage 2: Runtime image
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 chain

WORKDIR /home/chain

# Copy the binary from builder
COPY --from=builder /usr/src/chain/target/release/chain /usr/local/bin/chain

# Change ownership
RUN chown -R chain:chain /home/chain

# Switch to non-root user
USER chain

# Set the entrypoint
ENTRYPOINT ["chain"]

# Metadata
LABEL maintainer="Sajad Khoshdooni Farahani <sajjad.farahani@ut.ac.ir>"
LABEL description="Chain - A scalable blockchain with master and side chains"
LABEL version="0.1.0"

