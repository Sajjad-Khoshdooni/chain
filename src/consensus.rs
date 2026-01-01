// Consensus Module - Simplified for Academic Architecture Demonstration
// Implements basic consensus concepts: fork resolution, chain validation

use crate::master_chain::{MasterChain, MasterBlock};
use crate::side_chain::SideChain;

/// Consensus rules for the blockchain
pub struct ConsensusRules {
    pub min_difficulty: usize,
    pub max_block_time_variance: u64,
    pub finality_depth: u64,  // Blocks after which finality is reached
}

impl ConsensusRules {
    pub fn new() -> Self {
        Self {
            min_difficulty: 2,
            max_block_time_variance: 7200,  // 2 hours
            finality_depth: 6,  // 6 blocks for finality (like Bitcoin)
        }
    }
}

/// Fork resolution strategy
pub struct ForkResolver {
    rules: ConsensusRules,
}

impl ForkResolver {
    pub fn new(rules: ConsensusRules) -> Self {
        Self { rules }
    }
    
    /// Resolve fork by selecting the longest valid chain
    pub fn resolve_fork(&self, chain_a: &MasterChain, chain_b: &MasterChain) -> ChainSelection {
        // Rule 1: Select chain with most accumulated work (longest chain)
        let length_a = chain_a.blocks.len();
        let length_b = chain_b.blocks.len();
        
        if length_a > length_b {
            ChainSelection::ChainA
        } else if length_b > length_a {
            ChainSelection::ChainB
        } else {
            // Rule 2: If equal length, select chain with earlier timestamp on last block
            let time_a = chain_a.get_latest_block().timestamp;
            let time_b = chain_b.get_latest_block().timestamp;
            
            if time_a < time_b {
                ChainSelection::ChainA
            } else {
                ChainSelection::ChainB
            }
        }
    }
    
    /// Check if a block has reached finality
    pub fn is_finalized(&self, block_index: u64, current_height: u64) -> bool {
        current_height >= block_index + self.rules.finality_depth
    }
    
    /// Validate chain consistency
    pub fn validate_chain(&self, chain: &MasterChain) -> Result<(), ConsensusError> {
        if chain.blocks.is_empty() {
            return Err(ConsensusError::EmptyChain);
        }
        
        // Validate each block links to previous
        for i in 1..chain.blocks.len() {
            let prev_block = &chain.blocks[i - 1];
            let curr_block = &chain.blocks[i];
            
            // Check previous hash linkage
            if curr_block.previous_hash != prev_block.hash {
                return Err(ConsensusError::BrokenChain {
                    block_index: curr_block.index,
                });
            }
            
            // Check timestamp ordering
            if curr_block.timestamp < prev_block.timestamp {
                return Err(ConsensusError::InvalidTimestamp {
                    block_index: curr_block.index,
                });
            }
            
            // Check difficulty
            if curr_block.difficulty < self.rules.min_difficulty {
                return Err(ConsensusError::InsufficientDifficulty {
                    block_index: curr_block.index,
                    difficulty: curr_block.difficulty,
                });
            }
        }
        
        Ok(())
    }
}

/// Chain selection result
#[derive(Debug, PartialEq)]
pub enum ChainSelection {
    ChainA,
    ChainB,
}

/// Consensus errors
#[derive(Debug)]
pub enum ConsensusError {
    EmptyChain,
    BrokenChain { block_index: u64 },
    InvalidTimestamp { block_index: u64 },
    InsufficientDifficulty { block_index: u64, difficulty: usize },
    ForkTooLong,
}

/// Byzantine Fault Tolerance helper (simplified)
pub struct ByzantineFaultTolerance {
    total_nodes: usize,
    honest_nodes_required: usize,
}

impl ByzantineFaultTolerance {
    /// Create BFT with 2/3 majority requirement
    pub fn new(total_nodes: usize) -> Self {
        let honest_nodes_required = (total_nodes * 2) / 3 + 1;
        Self {
            total_nodes,
            honest_nodes_required,
        }
    }
    
    /// Check if we have Byzantine Fault Tolerance
    pub fn has_consensus(&self, honest_votes: usize) -> bool {
        honest_votes >= self.honest_nodes_required
    }
    
    /// Calculate maximum tolerable Byzantine (faulty) nodes
    pub fn max_byzantine_nodes(&self) -> usize {
        (self.total_nodes - 1) / 3
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_fork_resolution() {
        let rules = ConsensusRules::new();
        let resolver = ForkResolver::new(rules);
        
        let chain_a = MasterChain::new(3);
        let mut chain_b = MasterChain::new(3);
        chain_b.add_block(vec![]);  // Chain B is longer
        
        let selection = resolver.resolve_fork(&chain_a, &chain_b);
        assert_eq!(selection, ChainSelection::ChainB);
    }
    
    #[test]
    fn test_finality() {
        let rules = ConsensusRules::new();
        let resolver = ForkResolver::new(rules);
        
        // Block at height 10, current height 17
        assert!(resolver.is_finalized(10, 17));
        
        // Block at height 15, current height 17 (not finalized yet)
        assert!(!resolver.is_finalized(15, 17));
    }
    
    #[test]
    fn test_bft() {
        let bft = ByzantineFaultTolerance::new(10);
        
        assert_eq!(bft.max_byzantine_nodes(), 3);  // Can tolerate 3 Byzantine nodes
        assert!(bft.has_consensus(7));  // 7 votes is enough
        assert!(!bft.has_consensus(6));  // 6 votes is not enough
    }
}

