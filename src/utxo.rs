use sha2::{Digest, Sha256};
use serde::{Serialize, Deserialize};

/// Represents an Unspent Transaction Output (UTXO)
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub struct UTXO {
    pub tx_hash: String,
    pub output_index: u32,
    pub amount: u64,
    pub owner: String,
}

impl UTXO {
    /// Create a new UTXO
    pub fn new(tx_hash: String, output_index: u32, amount: u64, owner: String) -> Self {
        UTXO {
            tx_hash,
            output_index,
            amount,
            owner,
        }
    }
    
    /// Calculate a numeric hash for side chain assignment
    /// Uses modulo operation: utxo_hash % side_chain_count
    pub fn numeric_hash(&self) -> u64 {
        let hash_str = format!("{}{}", self.tx_hash, self.output_index);
        let mut hasher = Sha256::new();
        hasher.update(hash_str.as_bytes());
        let result = hasher.finalize();
        
        // Convert first 8 bytes to u64
        let mut bytes = [0u8; 8];
        bytes.copy_from_slice(&result[0..8]);
        u64::from_be_bytes(bytes)
    }
}

