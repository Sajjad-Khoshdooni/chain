// Validation Module - Simplified for Academic Architecture Demonstration
// Implements transaction and block validation logic

use crate::transaction::Transaction;
use crate::utxo::UTXO;
use crate::crypto::{Wallet, Signature};
use std::collections::{HashMap, HashSet};

/// UTXO Set for tracking unspent transaction outputs
#[derive(Debug, Clone)]
pub struct UtxoSet {
    /// Map: (tx_hash, output_index) -> UTXO
    unspent: HashMap<(String, u32), UTXO>,
    /// Track spent UTXOs to detect double-spending
    spent: HashSet<(String, u32)>,
}

impl UtxoSet {
    pub fn new() -> Self {
        Self {
            unspent: HashMap::new(),
            spent: HashSet::new(),
        }
    }
    
    /// Add a new UTXO
    pub fn add_utxo(&mut self, utxo: UTXO) {
        let key = (utxo.tx_hash.clone(), utxo.output_index);
        self.unspent.insert(key, utxo);
    }
    
    /// Check if UTXO is unspent
    pub fn is_unspent(&self, tx_hash: &str, output_index: u32) -> bool {
        let key = (tx_hash.to_string(), output_index);
        self.unspent.contains_key(&key) && !self.spent.contains(&key)
    }
    
    /// Mark UTXO as spent
    pub fn spend_utxo(&mut self, tx_hash: &str, output_index: u32) -> Result<(), ValidationError> {
        let key = (tx_hash.to_string(), output_index);
        
        if self.spent.contains(&key) {
            return Err(ValidationError::DoubleSpend);
        }
        
        if !self.unspent.contains_key(&key) {
            return Err(ValidationError::UtxoNotFound);
        }
        
        self.spent.insert(key);
        Ok(())
    }
    
    /// Get balance for an address
    pub fn get_balance(&self, address: &str) -> u64 {
        self.unspent
            .values()
            .filter(|utxo| utxo.owner == address)
            .map(|utxo| utxo.amount)
            .sum()
    }
}

/// Transaction Validator
pub struct TransactionValidator {
    utxo_set: UtxoSet,
    min_fee: u64,
}

impl TransactionValidator {
    pub fn new() -> Self {
        Self {
            utxo_set: UtxoSet::new(),
            min_fee: 1000,  // Minimum transaction fee
        }
    }
    
    pub fn with_utxo_set(utxo_set: UtxoSet) -> Self {
        Self {
            utxo_set,
            min_fee: 1000,
        }
    }
    
    /// Validate a transaction
    pub fn validate_transaction(&self, tx: &Transaction) -> Result<(), ValidationError> {
        // 1. Check transaction has inputs and outputs
        if tx.inputs.is_empty() {
            return Err(ValidationError::NoInputs);
        }
        
        if tx.outputs.is_empty() {
            return Err(ValidationError::NoOutputs);
        }
        
        // 2. Check all inputs are unspent
        for input in &tx.inputs {
            if !self.utxo_set.is_unspent(&input.tx_hash, input.output_index) {
                return Err(ValidationError::InputNotUnspent);
            }
        }
        
        // 3. Check input amounts >= output amounts
        let input_sum: u64 = tx.inputs.iter().map(|i| i.amount).sum();
        let output_sum: u64 = tx.outputs.iter().map(|o| o.amount).sum();
        
        if input_sum < output_sum {
            return Err(ValidationError::InsufficientFunds {
                input: input_sum,
                output: output_sum,
            });
        }
        
        // 4. Check minimum fee
        let fee = input_sum - output_sum;
        if fee < self.min_fee {
            return Err(ValidationError::InsufficientFee {
                provided: fee,
                required: self.min_fee,
            });
        }
        
        // 5. Check for double-spending within transaction
        let mut seen = HashSet::new();
        for input in &tx.inputs {
            let key = (&input.tx_hash, input.output_index);
            if !seen.insert(key) {
                return Err(ValidationError::DoubleSpendInTransaction);
            }
        }
        
        Ok(())
    }
    
    /// Apply transaction to UTXO set
    pub fn apply_transaction(&mut self, tx: &Transaction) -> Result<(), ValidationError> {
        // First validate
        self.validate_transaction(tx)?;
        
        // Spend inputs
        for input in &tx.inputs {
            self.utxo_set.spend_utxo(&input.tx_hash, input.output_index)?;
        }
        
        // Add outputs as new UTXOs
        for (index, output) in tx.outputs.iter().enumerate() {
            let utxo = UTXO {
                tx_hash: tx.id.clone(),
                output_index: index as u32,
                amount: output.amount,
                owner: output.owner.clone(),
            };
            self.utxo_set.add_utxo(utxo);
        }
        
        Ok(())
    }
    
    pub fn get_utxo_set(&self) -> &UtxoSet {
        &self.utxo_set
    }
}

/// Validation errors
#[derive(Debug)]
pub enum ValidationError {
    NoInputs,
    NoOutputs,
    InputNotUnspent,
    InsufficientFunds { input: u64, output: u64 },
    InsufficientFee { provided: u64, required: u64 },
    DoubleSpend,
    DoubleSpendInTransaction,
    UtxoNotFound,
    InvalidSignature,
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_utxo_set() {
        let mut utxo_set = UtxoSet::new();
        
        let utxo = UTXO {
            tx_hash: "tx1".to_string(),
            output_index: 0,
            amount: 100,
            owner: "alice".to_string(),
        };
        
        utxo_set.add_utxo(utxo);
        
        assert!(utxo_set.is_unspent("tx1", 0));
        assert!(!utxo_set.is_unspent("tx1", 1));
        
        utxo_set.spend_utxo("tx1", 0).unwrap();
        assert!(!utxo_set.is_unspent("tx1", 0));
    }
    
    #[test]
    fn test_double_spend_detection() {
        let mut utxo_set = UtxoSet::new();
        
        let utxo = UTXO {
            tx_hash: "tx1".to_string(),
            output_index: 0,
            amount: 100,
            owner: "alice".to_string(),
        };
        
        utxo_set.add_utxo(utxo);
        utxo_set.spend_utxo("tx1", 0).unwrap();
        
        // Try to spend again - should fail
        let result = utxo_set.spend_utxo("tx1", 0);
        assert!(matches!(result, Err(ValidationError::DoubleSpend)));
    }
}

