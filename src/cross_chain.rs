// Cross-Chain Communication Module - Simplified for Academic Architecture Demonstration
// Implements cross-sidechain transaction protocol

use crate::transaction::Transaction;
use crate::utxo::UTXO;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;

/// Cross-chain transfer request
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CrossChainTransfer {
    pub transfer_id: String,
    pub source_chain_id: usize,
    pub target_chain_id: usize,
    pub amount: u64,
    pub sender: String,
    pub recipient: String,
    pub status: TransferStatus,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum TransferStatus {
    Initiated,       // Transfer initiated on source chain
    Locked,          // Funds locked on source chain
    Verified,        // Transfer verified by master chain
    Completed,       // Transfer completed on target chain
    Failed,          // Transfer failed
}

/// Cross-chain bridge for managing transfers between sidechains
pub struct CrossChainBridge {
    /// Pending transfers
    pending_transfers: HashMap<String, CrossChainTransfer>,
    /// Completed transfers
    completed_transfers: HashMap<String, CrossChainTransfer>,
}

impl CrossChainBridge {
    pub fn new() -> Self {
        Self {
            pending_transfers: HashMap::new(),
            completed_transfers: HashMap::new(),
        }
    }
    
    /// Initiate a cross-chain transfer
    pub fn initiate_transfer(
        &mut self,
        source_chain_id: usize,
        target_chain_id: usize,
        amount: u64,
        sender: String,
        recipient: String,
    ) -> Result<String, CrossChainError> {
        // Validate source and target are different
        if source_chain_id == target_chain_id {
            return Err(CrossChainError::SameChain);
        }
        
        // Generate transfer ID
        let transfer_id = format!(
            "xfer_{}_{}_{}",
            source_chain_id,
            target_chain_id,
            chrono::Utc::now().timestamp_millis()
        );
        
        let transfer = CrossChainTransfer {
            transfer_id: transfer_id.clone(),
            source_chain_id,
            target_chain_id,
            amount,
            sender,
            recipient,
            status: TransferStatus::Initiated,
        };
        
        self.pending_transfers.insert(transfer_id.clone(), transfer);
        
        println!(
            "🌉 Cross-chain transfer initiated: {} → {} (amount: {})",
            source_chain_id, target_chain_id, amount
        );
        
        Ok(transfer_id)
    }
    
    /// Lock funds on source chain
    pub fn lock_funds(&mut self, transfer_id: &str) -> Result<(), CrossChainError> {
        let transfer = self.pending_transfers
            .get_mut(transfer_id)
            .ok_or(CrossChainError::TransferNotFound)?;
        
        if transfer.status != TransferStatus::Initiated {
            return Err(CrossChainError::InvalidState);
        }
        
        transfer.status = TransferStatus::Locked;
        
        println!(
            "🔒 Funds locked on chain {} (transfer: {})",
            transfer.source_chain_id, transfer_id
        );
        
        Ok(())
    }
    
    /// Verify transfer through master chain
    pub fn verify_transfer(
        &mut self,
        transfer_id: &str,
        master_block_hash: &str,
    ) -> Result<(), CrossChainError> {
        let transfer = self.pending_transfers
            .get_mut(transfer_id)
            .ok_or(CrossChainError::TransferNotFound)?;
        
        if transfer.status != TransferStatus::Locked {
            return Err(CrossChainError::InvalidState);
        }
        
        transfer.status = TransferStatus::Verified;
        
        println!(
            "✓ Transfer verified by master chain (block: {})",
            &master_block_hash[..8]
        );
        
        Ok(())
    }
    
    /// Complete transfer on target chain
    pub fn complete_transfer(&mut self, transfer_id: &str) -> Result<CrossChainTransfer, CrossChainError> {
        let mut transfer = self.pending_transfers
            .remove(transfer_id)
            .ok_or(CrossChainError::TransferNotFound)?;
        
        if transfer.status != TransferStatus::Verified {
            return Err(CrossChainError::InvalidState);
        }
        
        transfer.status = TransferStatus::Completed;
        
        println!(
            "✅ Transfer completed on chain {} (recipient: {})",
            transfer.target_chain_id, transfer.recipient
        );
        
        self.completed_transfers.insert(transfer_id.to_string(), transfer.clone());
        
        Ok(transfer)
    }
    
    /// Get transfer status
    pub fn get_transfer_status(&self, transfer_id: &str) -> Option<TransferStatus> {
        self.pending_transfers
            .get(transfer_id)
            .map(|t| t.status.clone())
            .or_else(|| {
                self.completed_transfers
                    .get(transfer_id)
                    .map(|t| t.status.clone())
            })
    }
    
    /// Get all pending transfers
    pub fn get_pending_transfers(&self) -> Vec<&CrossChainTransfer> {
        self.pending_transfers.values().collect()
    }
}

/// Cross-chain protocol for atomic swaps
pub struct AtomicSwapProtocol {
    pub hash_lock: String,      // Hash lock for atomic swap
    pub time_lock: u64,          // Time lock (expiration timestamp)
    pub secret: Option<String>,  // Secret for unlocking
}

impl AtomicSwapProtocol {
    /// Create new atomic swap
    pub fn new(secret: &str, time_lock: u64) -> Self {
        use sha2::{Digest, Sha256};
        
        let mut hasher = Sha256::new();
        hasher.update(secret.as_bytes());
        let hash_lock = hex::encode(hasher.finalize());
        
        Self {
            hash_lock,
            time_lock,
            secret: None,
        }
    }
    
    /// Verify secret matches hash lock
    pub fn verify_secret(&self, secret: &str) -> bool {
        use sha2::{Digest, Sha256};
        
        let mut hasher = Sha256::new();
        hasher.update(secret.as_bytes());
        let hash = hex::encode(hasher.finalize());
        
        hash == self.hash_lock
    }
    
    /// Check if time lock has expired
    pub fn is_expired(&self, current_time: u64) -> bool {
        current_time > self.time_lock
    }
}

/// Cross-chain errors
#[derive(Debug)]
pub enum CrossChainError {
    TransferNotFound,
    SameChain,
    InvalidState,
    InsufficientBalance,
    TimeoutExpired,
    InvalidSecret,
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_cross_chain_transfer() {
        let mut bridge = CrossChainBridge::new();
        
        // Initiate transfer
        let transfer_id = bridge
            .initiate_transfer(0, 1, 100, "alice".to_string(), "bob".to_string())
            .unwrap();
        
        assert_eq!(
            bridge.get_transfer_status(&transfer_id),
            Some(TransferStatus::Initiated)
        );
        
        // Lock funds
        bridge.lock_funds(&transfer_id).unwrap();
        assert_eq!(
            bridge.get_transfer_status(&transfer_id),
            Some(TransferStatus::Locked)
        );
        
        // Verify transfer
        bridge.verify_transfer(&transfer_id, "master_block_hash").unwrap();
        assert_eq!(
            bridge.get_transfer_status(&transfer_id),
            Some(TransferStatus::Verified)
        );
        
        // Complete transfer
        let transfer = bridge.complete_transfer(&transfer_id).unwrap();
        assert_eq!(transfer.status, TransferStatus::Completed);
    }
    
    #[test]
    fn test_atomic_swap() {
        let secret = "my_secret_123";
        let time_lock = 1000000000;
        
        let swap = AtomicSwapProtocol::new(secret, time_lock);
        
        // Verify correct secret
        assert!(swap.verify_secret(secret));
        
        // Verify wrong secret
        assert!(!swap.verify_secret("wrong_secret"));
        
        // Check time lock
        assert!(!swap.is_expired(999999999));
        assert!(swap.is_expired(1000000001));
    }
}

