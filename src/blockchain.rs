use crate::master_chain::{MasterChain, SideChainBlockReference};
use crate::side_chain::SideChain;
use crate::transaction::Transaction;

/// Chain - Main blockchain system
/// 
/// Architecture:
/// - Master Chain: PoW consensus, 10-minute block time, stores side chain references
/// - Side Chains: Multiple parallel chains, 1-minute block time, process transactions
/// - Transaction Assignment: UTXO-based (utxo % side_chain_id)
/// - Dynamic Scaling: Number of side chains adjusts to network load
pub struct Chain {
    pub master_chain: MasterChain,
    pub side_chains: Vec<SideChain>,
    pub num_side_chains: usize,
}

impl Chain {
    /// Create a new Chain with specified number of side chains
    pub fn new(num_side_chains: usize, master_difficulty: usize) -> Self {
        let master_chain = MasterChain::new(master_difficulty);
        let master_hash = master_chain.get_latest_block().hash.clone();
        
        let side_chains: Vec<SideChain> = (0..num_side_chains)
            .map(|id| SideChain::new(id, master_hash.clone()))
            .collect();
        
        println!("🚀 Chain initialized with {} side chains", num_side_chains);
        
        Chain {
            master_chain,
            side_chains,
            num_side_chains,
        }
    }
    
    /// Assign a transaction to the appropriate side chain based on UTXO
    /// Uses deterministic assignment: utxo_hash % num_side_chains
    pub fn assign_transaction(&mut self, tx: Transaction) {
        if let Some(utxo) = tx.get_primary_utxo() {
            let utxo_hash = utxo.numeric_hash();
            let side_chain_id = (utxo_hash % self.num_side_chains as u64) as usize;
            
            println!(
                "📝 Transaction {} → Side Chain {}",
                &tx.id[..8],
                side_chain_id
            );
            
            self.side_chains[side_chain_id].add_transaction(tx);
        }
    }
    
    /// Generate blocks on all side chains
    /// Simulates 1-minute block generation interval
    pub fn generate_side_chain_blocks(&mut self, side_chain_difficulty: usize) -> Vec<SideChainBlockReference> {
        let master_hash = self.master_chain.get_latest_block().hash.clone();
        let mut references = Vec::new();
        
        println!("\n⛓️  Generating side chain blocks...");
        
        for side_chain in &mut self.side_chains {
            if !side_chain.mempool.is_empty() || side_chain.blocks.len() == 1 {
                let block = side_chain.generate_block(master_hash.clone(), side_chain_difficulty);
                
                println!(
                    "   Side Chain {} → Block {} ({} tx)",
                    side_chain.id,
                    block.index,
                    block.transactions.len()
                );
                
                references.push(SideChainBlockReference::new(
                    side_chain.id,
                    block.hash.clone(),
                    block.index,
                    block.transactions.len(),
                ));
            }
        }
        
        references
    }
    
    /// Generate a master chain block
    /// Simulates 10-minute block generation interval
    pub fn generate_master_block(&mut self, side_chain_refs: Vec<SideChainBlockReference>) {
        println!("\n🔗 Generating Master Chain Block...");
        let block = self.master_chain.add_block(side_chain_refs);
        
        println!(
            "✓ Master Block {} created ({} side chain refs)",
            block.index,
            block.side_chain_references.len()
        );
    }
    
    /// Calculate total TPS based on the formula:
    /// TPS_total = M/600 + (N*S)/60
    /// where M = master chain tx/block, N = side chains, S = side chain tx/block
    pub fn calculate_tps(&self, master_tx_per_block: u64, side_tx_per_block: u64) -> f64 {
        let master_tps = master_tx_per_block as f64 / 600.0;
        let side_tps = (self.num_side_chains as f64 * side_tx_per_block as f64) / 60.0;
        master_tps + side_tps
    }
    
    /// Display comprehensive statistics
    pub fn display_stats(&self) {
        println!("\n╔════════════════════════════════════════════════╗");
        println!("║            Chain Statistics                    ║");
        println!("╚════════════════════════════════════════════════╝");
        println!("📊 Master Chain Blocks: {}", self.master_chain.blocks.len());
        println!("🔗 Number of Side Chains: {}", self.num_side_chains);
        
        let mut total_tx = 0;
        for sc in &self.side_chains {
            let sc_tx = sc.total_transactions();
            total_tx += sc_tx;
            println!(
                "   └─ Side Chain {}: {} blocks, {} transactions",
                sc.id, sc.blocks.len(), sc_tx
            );
        }
        
        println!("💰 Total Transactions: {}", total_tx);
        
        // Theoretical TPS calculation
        let theoretical_tps = self.calculate_tps(1000, 100);
        println!("⚡ Theoretical TPS (M=1000, S=100): {:.2}", theoretical_tps);
        println!("════════════════════════════════════════════════\n");
    }
    
    /// Get total number of transactions processed
    pub fn total_transactions(&self) -> usize {
        self.side_chains.iter().map(|sc| sc.total_transactions()).sum()
    }
    
    /// Scale the network by adding new side chains
    pub fn add_side_chains(&mut self, count: usize) {
        let master_hash = self.master_chain.get_latest_block().hash.clone();
        
        for i in 0..count {
            let new_id = self.num_side_chains + i;
            self.side_chains.push(SideChain::new(new_id, master_hash.clone()));
        }
        
        self.num_side_chains += count;
        println!("📈 Added {} side chains (total: {})", count, self.num_side_chains);
    }
}

