// Chain - A Scalable Blockchain Implementation in Rust
//
// Architecture:
// - Master Chain: PoW consensus, 10-minute blocks, stores side chain references
// - Side Chains: Multiple parallel chains, 1-minute blocks, process transactions
// - Transaction Assignment: UTXO-based (utxo_hash % side_chain_count)
// - Dynamic Scaling: Side chains scale with network demand

pub mod utils;
pub mod utxo;
pub mod transaction;
pub mod side_chain;
pub mod master_chain;
pub mod miner;
pub mod blockchain;
pub mod chain_system;

// New modules for enhanced architecture
pub mod crypto;
pub mod consensus;
pub mod validation;
pub mod cross_chain;

// Re-export main types for easier usage
pub use utxo::UTXO;
pub use transaction::Transaction;
pub use side_chain::{SideChain, SideChainBlock};
pub use master_chain::{MasterChain, MasterBlock, SideChainBlockReference};
pub use miner::assign_miner_to_sidechains;
pub use blockchain::Chain;
pub use chain_system::ChainSystem;
pub use utils::current_timestamp;

// Re-export new types
pub use crypto::{Wallet, Signature};
pub use consensus::{ConsensusRules, ForkResolver, ByzantineFaultTolerance};
pub use validation::{UtxoSet, TransactionValidator, ValidationError};
pub use cross_chain::{CrossChainBridge, CrossChainTransfer, TransferStatus, AtomicSwapProtocol};

