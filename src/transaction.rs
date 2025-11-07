use sha2::{Digest, Sha256};
use serde::{Serialize, Deserialize};
use crate::utxo::UTXO;
use crate::utils::current_timestamp;

/// Represents a transaction in the blockchain
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Transaction {
    pub id: String,
    pub inputs: Vec<UTXO>,
    pub outputs: Vec<UTXO>,
    pub timestamp: u64,
}

impl Transaction {
    /// Create a new transaction
    pub fn new(inputs: Vec<UTXO>, outputs: Vec<UTXO>) -> Self {
        let timestamp = current_timestamp();
        let id = Self::calculate_hash(&inputs, &outputs, timestamp);
        
        Transaction {
            id,
            inputs,
            outputs,
            timestamp,
        }
    }
    
    /// Calculate the transaction hash
    fn calculate_hash(inputs: &[UTXO], outputs: &[UTXO], timestamp: u64) -> String {
        let mut hasher = Sha256::new();
        let data = format!("{:?}{:?}{}", inputs, outputs, timestamp);
        hasher.update(data.as_bytes());
        hex::encode(hasher.finalize())
    }
    
    /// Get the primary UTXO for side chain assignment
    /// The first input UTXO is used to determine which side chain processes this transaction
    pub fn get_primary_utxo(&self) -> Option<&UTXO> {
        self.inputs.first()
    }
}

