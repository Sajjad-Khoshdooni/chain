use sha2::{Digest, Sha256};
use serde::{Serialize, Deserialize};
use crate::utils::current_timestamp;

/// Reference to side chain blocks included in a master block
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SideChainBlockReference {
    pub side_chain_id: usize,
    pub block_hash: String,
    pub block_index: u64,
    pub transaction_count: usize,
}

impl SideChainBlockReference {
    pub fn new(side_chain_id: usize, block_hash: String, block_index: u64, transaction_count: usize) -> Self {
        SideChainBlockReference {
            side_chain_id,
            block_hash,
            block_index,
            transaction_count,
        }
    }
}

/// Represents a block in the master chain
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MasterBlock {
    pub index: u64,
    pub timestamp: u64,
    pub side_chain_references: Vec<SideChainBlockReference>,
    pub previous_hash: String,
    pub hash: String,
    pub nonce: u64,
    pub difficulty: usize,
}

impl MasterBlock {
    pub fn new(
        index: u64,
        side_chain_references: Vec<SideChainBlockReference>,
        previous_hash: String,
        difficulty: usize,
    ) -> Self {
        let timestamp = current_timestamp();
        let hash = Self::calculate_hash(
            index,
            timestamp,
            &side_chain_references,
            &previous_hash,
            0,
        );
        
        MasterBlock {
            index,
            timestamp,
            side_chain_references,
            previous_hash,
            hash,
            nonce: 0,
            difficulty,
        }
    }
    
    pub fn calculate_hash(
        index: u64,
        timestamp: u64,
        side_chain_references: &[SideChainBlockReference],
        previous_hash: &str,
        nonce: u64,
    ) -> String {
        let mut hasher = Sha256::new();
        let refs_data: Vec<String> = side_chain_references
            .iter()
            .map(|r| format!("{}:{}", r.side_chain_id, r.block_hash))
            .collect();
        let data = format!(
            "{}{}{}{}{}",
            index,
            timestamp,
            refs_data.join(","),
            previous_hash,
            nonce
        );
        hasher.update(data.as_bytes());
        hex::encode(hasher.finalize())
    }
    
    /// Mine the master block with Proof of Work consensus
    /// Uses Bitcoin-like PoW mechanism (10 minute average in production)
    pub fn mine(&mut self) {
        let target = "0".repeat(self.difficulty);
        
        println!("Mining master block {} with difficulty {}...", self.index, self.difficulty);
        
        loop {
            self.hash = Self::calculate_hash(
                self.index,
                self.timestamp,
                &self.side_chain_references,
                &self.previous_hash,
                self.nonce,
            );
            
            if self.hash.starts_with(&target) {
                println!("✓ Master block mined! Hash: {}, Nonce: {}", self.hash, self.nonce);
                break;
            }
            
            self.nonce += 1;
            
            if self.nonce % 100000 == 0 {
                println!("  Mining progress... nonce: {}", self.nonce);
            }
        }
    }
}

/// The master blockchain
#[derive(Debug, Clone)]
pub struct MasterChain {
    pub blocks: Vec<MasterBlock>,
    pub difficulty: usize,
}

impl MasterChain {
    /// Create a new master chain with genesis block
    pub fn new(difficulty: usize) -> Self {
        let mut genesis = MasterBlock::new(0, vec![], "0".to_string(), difficulty);
        genesis.mine();
        
        MasterChain {
            blocks: vec![genesis],
            difficulty,
        }
    }
    
    /// Get the latest block in the master chain
    pub fn get_latest_block(&self) -> &MasterBlock {
        self.blocks.last().unwrap()
    }
    
    /// Add a new block to the master chain
    /// This happens every 10 minutes in production
    pub fn add_block(&mut self, side_chain_references: Vec<SideChainBlockReference>) -> &MasterBlock {
        let latest_block = self.get_latest_block();
        
        let mut new_block = MasterBlock::new(
            latest_block.index + 1,
            side_chain_references,
            latest_block.hash.clone(),
            self.difficulty,
        );
        
        new_block.mine();
        self.blocks.push(new_block);
        
        self.blocks.last().unwrap()
    }
}

