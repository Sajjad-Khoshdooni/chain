use sha2::{Digest, Sha256};
use serde::{Serialize, Deserialize};
use crate::transaction::Transaction;
use crate::utils::current_timestamp;

/// Represents a block in a side chain
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SideChainBlock {
    pub index: u64,
    pub side_chain_id: usize,
    pub timestamp: u64,
    pub transactions: Vec<Transaction>,
    pub previous_hash: String,
    pub parent_master_block_hash: String,
    pub hash: String,
    pub nonce: u64,
}

impl SideChainBlock {
    pub fn new(
        index: u64,
        side_chain_id: usize,
        transactions: Vec<Transaction>,
        previous_hash: String,
        parent_master_block_hash: String,
    ) -> Self {
        let timestamp = current_timestamp();
        let hash = Self::calculate_hash(
            index,
            side_chain_id,
            timestamp,
            &transactions,
            &previous_hash,
            &parent_master_block_hash,
            0,
        );
        
        SideChainBlock {
            index,
            side_chain_id,
            timestamp,
            transactions,
            previous_hash,
            parent_master_block_hash,
            hash,
            nonce: 0,
        }
    }
    
    pub fn calculate_hash(
        index: u64,
        side_chain_id: usize,
        timestamp: u64,
        transactions: &[Transaction],
        previous_hash: &str,
        parent_master_block_hash: &str,
        nonce: u64,
    ) -> String {
        let mut hasher = Sha256::new();
        let tx_data: Vec<String> = transactions.iter().map(|tx| tx.id.clone()).collect();
        let data = format!(
            "{}{}{}{}{}{}{}",
            index,
            side_chain_id,
            timestamp,
            tx_data.join(","),
            previous_hash,
            parent_master_block_hash,
            nonce
        );
        hasher.update(data.as_bytes());
        hex::encode(hasher.finalize())
    }
    
    /// Mine the block with specified difficulty
    /// Side chains typically use lower difficulty than master chain
    pub fn mine(&mut self, difficulty: usize) {
        let target = "0".repeat(difficulty);
        
        loop {
            self.hash = Self::calculate_hash(
                self.index,
                self.side_chain_id,
                self.timestamp,
                &self.transactions,
                &self.previous_hash,
                &self.parent_master_block_hash,
                self.nonce,
            );
            
            if self.hash.starts_with(&target) {
                break;
            }
            
            self.nonce += 1;
        }
    }
}

/// Represents a side chain with its own blockchain and mempool
#[derive(Debug, Clone)]
pub struct SideChain {
    pub id: usize,
    pub blocks: Vec<SideChainBlock>,
    pub mempool: Vec<Transaction>,
}

impl SideChain {
    /// Create a new side chain with genesis block
    pub fn new(id: usize, parent_master_hash: String) -> Self {
        let genesis = SideChainBlock::new(
            0,
            id,
            vec![],
            "0".to_string(),
            parent_master_hash,
        );
        
        SideChain {
            id,
            blocks: vec![genesis],
            mempool: vec![],
        }
    }
    
    /// Add a transaction to the mempool
    pub fn add_transaction(&mut self, tx: Transaction) {
        self.mempool.push(tx);
    }
    
    /// Get the latest block in the chain
    pub fn get_latest_block(&self) -> &SideChainBlock {
        self.blocks.last().unwrap()
    }
    
    /// Generate a new side chain block
    /// In production, this happens every 1 minute
    pub fn generate_block(&mut self, parent_master_hash: String, difficulty: usize) -> SideChainBlock {
        let latest_index = self.get_latest_block().index;
        let latest_hash = self.get_latest_block().hash.clone();
        let transactions = self.mempool.drain(..).collect();
        
        let mut new_block = SideChainBlock::new(
            latest_index + 1,
            self.id,
            transactions,
            latest_hash,
            parent_master_hash,
        );
        
        new_block.mine(difficulty);
        self.blocks.push(new_block.clone());
        
        new_block
    }
    
    /// Get total number of transactions processed
    pub fn total_transactions(&self) -> usize {
        self.blocks.iter().map(|b| b.transactions.len()).sum()
    }
}

