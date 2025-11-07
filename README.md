# Chain

> A Scalable Blockchain Implementation with Master and Side Chains in Rust

[![Rust](https://img.shields.io/badge/rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)

## 📖 Overview

**Chain** is an innovative blockchain architecture designed to significantly enhance Bitcoin's scalability by implementing a master chain and multiple side chains. This bifurcated structure facilitates parallel transaction processing, thereby increasing overall transaction throughput without compromising security and decentralization.

### Key Features

- 🔗 **Master Chain**: PoW consensus, 10-minute block time, stores side chain references
- ⛓️ **Side Chains**: Multiple parallel chains with 1-minute block time
- 🎯 **UTXO-based Transaction Assignment**: Deterministic routing using `utxo_hash % side_chain_count`
- ⚡ **High Scalability**: Dynamic side chain scaling based on network demand
- 🔒 **Security**: Bitcoin-compatible PoW for master chain
- 📊 **Theoretical TPS**: `TPS = M/600 + (N*S)/60`

### Scalability Comparison

| Side Chains | TPS (M=1000, S=100) | vs Bitcoin (7 TPS) |
|-------------|---------------------|--------------------|
| 1           | 3.33                | 0.5x               |
| 5           | 10.00               | 1.4x               |
| 10          | 18.33               | 2.6x               |
| 20          | 35.00               | 5.0x               |

---

## 🏗️ Architecture

```
Master Chain (a1) → (a2) → (a3)
                ↓      ↓      ↓
Side Chain 1:  b11→b12→b13→b14
Side Chain 2:  c11→c12→c13→c14
Side Chain 3:  d11→d12→d13→d14
```

### Core Components

- **Master Chain**: Maintains network state with PoW consensus (SHA-256), generates blocks every 10 minutes
- **Side Chains**: Process transactions in parallel with lower PoW difficulty, 1-minute block generation
- **Transaction Assignment**: UTXO-based routing (`utxo_hash % num_side_chains`)
- **Miner Assignment**: Each miner participates in at least 2 side chains to prevent centralization

### Key Algorithms

1. **Transaction Assignment**: `side_chain_id = utxo_hash % num_side_chains`
2. **Miner Assignment**: `side_chain_1 = miner_id % N`, `side_chain_2 = (miner_id / N) % N`
3. **TPS Calculation**: `TPS = M/600 + (N*S)/60`

---

## 🚀 Quick Start

### Prerequisites

- Rust 1.75+ and Cargo
- Docker (optional)

### One-Line Start

```bash
./start.sh
```

### Build Options

```bash
./build.sh release      # Build optimized binary
./build.sh debug        # Build debug version
./build.sh test         # Run all tests
./build.sh docker       # Build Docker image
./build.sh clean        # Clean artifacts
```

### Run Options

```bash
./run.sh native         # Run natively (fastest)
./run.sh cargo          # Run with cargo
./run.sh docker         # Run in Docker
./run.sh docker-compose # Run with compose
./run.sh compose-bg     # Background mode
./run.sh stop           # Stop services
```

---

## 📂 Project Structure

```
Chain/
├── src/
│   ├── lib.rs              # Library entry point & public API
│   ├── main.rs             # Demo application
│   ├── utils.rs            # Utility functions
│   ├── utxo.rs             # UTXO implementation
│   ├── transaction.rs      # Transaction structures
│   ├── side_chain.rs       # Side chain logic & blocks
│   ├── master_chain.rs     # Master chain with PoW
│   ├── miner.rs            # Miner assignment algorithm
│   └── blockchain.rs       # Main blockchain system
│
├── Cargo.toml              # Rust package configuration
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Service orchestration
│
├── build.sh                # Build automation script
├── run.sh                  # Run automation script
├── start.sh                # Quick start script
│
├── ashkchain.txt           # Technical architecture (full paper)
└── proposal.txt            # Research proposal (Persian)
```

---

## 💻 Usage & Examples

### Basic Usage in Rust

```rust
use chain::{Chain, Transaction, UTXO};

fn main() {
    // Create blockchain with 5 side chains, difficulty 3
    let mut blockchain = Chain::new(5, 3);
    
    // Create a transaction
    let utxo = UTXO {
        tx_hash: "prev_tx_1".to_string(),
        output_index: 0,
        amount: 1000,
        owner: "alice".to_string(),
    };
    
    let output = UTXO {
        tx_hash: "new_tx_1".to_string(),
        output_index: 0,
        amount: 1000,
        owner: "bob".to_string(),
    };
    
    let tx = Transaction::new(vec![utxo], vec![output]);
    
    // Assign transaction to appropriate side chain
    blockchain.assign_transaction(tx);
    
    // Generate side chain blocks (1-minute intervals)
    let refs = blockchain.generate_side_chain_blocks(2);
    
    // Generate master block (10-minute interval)
    blockchain.generate_master_block(refs);
    
    // Display statistics
    blockchain.display_stats();
}
```

### Miner Assignment Example

```rust
use chain::assign_miner_to_sidechains;

let (sc1, sc2) = assign_miner_to_sidechains(15, 10);
println!("Miner 15 → Side Chains ({}, {})", sc1, sc2);
// Output: Miner 15 → Side Chains (5, 1)
```

---

## 🐳 Docker Deployment

### Build & Run

```bash
# Build image
docker build -t chain:latest .

# Run container
docker run --rm chain:latest
```

### Using Docker Compose

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🧪 Testing & Development

### Run Tests

```bash
./build.sh test
# or
cargo test
```

### Development Workflow

```bash
# 1. Make changes to src/
# 2. Test
cargo test

# 3. Format and lint
cargo fmt
cargo clippy

# 4. Run
cargo run --release

# 5. Commit
git add .
git commit -m "Your message"
```

### Common Cargo Commands

```bash
cargo build --release   # Optimized build
cargo build             # Debug build
cargo test              # Run tests
cargo check             # Quick check
cargo fmt               # Format code
cargo clippy            # Lint code
cargo doc --open        # Generate & open docs
```

---

## 🔧 Configuration

### Blockchain Parameters

Edit `src/main.rs`:

```rust
let num_side_chains = 3;       // Number of parallel side chains
let master_difficulty = 3;     // Master chain PoW difficulty
let side_difficulty = 2;       // Side chain PoW difficulty
```

### Environment Variables

```bash
export RUST_LOG=info           # Logging level
export RUST_BACKTRACE=1        # Enable backtraces
```

---

## 📊 Performance Characteristics

### Block Generation
- **Master Chain**: ~10 minutes (adjustable difficulty)
- **Side Chains**: ~1 minute (lower difficulty)

### Transaction Assignment
- **Algorithm**: `utxo_hash % num_side_chains`
- **Complexity**: O(1)
- **Deterministic**: Yes (prevents double-spending)

### Scalability Formula
```
TPS_total = M/600 + (N*S)/60

Where:
  M = Master chain transactions per block
  N = Number of side chains
  S = Side chain transactions per block
```

---

## 🔒 Security Features

1. **PoW Consensus**: Bitcoin-compatible SHA-256 mining
2. **Deterministic Assignment**: Prevents transaction conflicts
3. **Chain Integrity**: Cryptographic hashing throughout
4. **Miner Distribution**: Multi-chain participation prevents centralization
5. **Block References**: Side chains anchored to master chain

---

## 🎓 Academic Context

**Research Project**: Master's Thesis  
**Institution**: University of Tehran  
**Faculty**: Engineering Science  
**Student**: Sajad Khoshdooni Farahani  
**Supervisor**: Dr. Ali Komandi  
**Year**: 2025

### Research Objectives

1. ✅ Enhance blockchain scalability
2. ✅ Maintain security and decentralization
3. ✅ Reduce transaction latency
4. ✅ Optimize energy efficiency
5. ✅ Enable dynamic scaling

---

## 🛠️ Technical Details

### Dependencies

```toml
sha2 = "0.10"          # SHA-256 hashing
hex = "0.4"            # Hexadecimal encoding
serde = "1.0"          # Serialization framework
serde_json = "1.0"     # JSON support
chrono = "0.4"         # Date/time utilities
```

### Modular Architecture

- **7 Core Modules**: Separated concerns for maintainability
- **Type-Safe**: Full Rust type system
- **Tested**: Unit tests for critical algorithms
- **Documented**: Inline documentation throughout

---

## 🚧 Troubleshooting

### Build Issues

```bash
./build.sh clean
./build.sh release
```

### Docker Issues

```bash
docker-compose down --volumes
docker-compose build --no-cache
docker-compose up
```

### Permission Issues

```bash
chmod +x build.sh run.sh start.sh
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test: `cargo test`
4. Format code: `cargo fmt && cargo clippy`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open Pull Request

---

## 📄 License & Citation

This is a research implementation as part of a Master's thesis at the University of Tehran.

### Citation

If you use this work in your research:

```bibtex
@mastersthesis{farahani2025ashkanchain,
  title={Design and Optimization of a Scalable Consensus Algorithm for Blockchain Systems},
  author={Farahani, Sajad Khoshdooni},
  year={2025},
  school={University of Tehran}
}
```

---

## 📞 Contact

**Sajad Khoshdooni Farahani**  
📧 sajjad.farahani@ut.ac.ir  
🏛️ University of Tehran - Faculty of Engineering Science

---

## 🙏 Acknowledgments

- Bitcoin Core for foundational concepts
- Rust community for excellent tooling
- University of Tehran for research support
- Dr. Ali Komandi for academic guidance

---

## 🔗 Related Work

- **Bitcoin**: Original blockchain implementation
- **Lightning Network**: Layer-2 scaling solution
- **Ethereum 2.0**: Sharding implementation
- **Polkadot**: Multi-chain architecture

---

**⚠️ Note**: This is a research implementation. Not recommended for production use without further security audits and testing.

**Version**: 0.1.0  
**Last Updated**: November 7, 2025

Made with ❤️ in Tehran, Iran 🇮🇷
