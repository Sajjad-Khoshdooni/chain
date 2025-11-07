use chain::{Chain, Transaction, UTXO, assign_miner_to_sidechains};

fn main() {
    println!("╔════════════════════════════════════════════════╗");
    println!("║          Chain - Rust Implementation           ║");
    println!("║  Scalable Blockchain with Master + Side Chains║");
    println!("╚════════════════════════════════════════════════╝\n");
    
    // Configuration
    let num_side_chains = 3;
    let master_difficulty = 3; // Adjust for demo (Bitcoin uses ~20)
    let side_difficulty = 2;
    
    // Initialize Chain
    let mut blockchain = Chain::new(num_side_chains, master_difficulty);
    
    // Create sample transactions
    println!("\n--- Creating Sample Transactions ---");
    
    for i in 0..9 {
        let utxo = UTXO {
            tx_hash: format!("prev_tx_{}", i),
            output_index: i,
            amount: 100 + i as u64 * 10,
            owner: format!("address_{}", i),
        };
        
        let new_utxo = UTXO {
            tx_hash: format!("new_tx_{}", i),
            output_index: 0,
            amount: 100 + i as u64 * 10,
            owner: format!("address_{}", (i + 1) % 10),
        };
        
        let tx = Transaction::new(vec![utxo], vec![new_utxo]);
        blockchain.assign_transaction(tx);
    }
    
    // Simulate side chain block generation (1 minute intervals)
    println!("\n--- Simulating Side Chain Block Generation ---");
    let mut all_side_refs = Vec::new();
    
    for round in 1..=3 {
        println!("\n[Round {} - 1 minute interval]", round);
        let refs = blockchain.generate_side_chain_blocks(side_difficulty);
        all_side_refs.extend(refs);
        
        // Add more transactions for next round
        if round < 3 {
            for i in 0..3 {
                let utxo = UTXO {
                    tx_hash: format!("tx_r{}_i{}", round, i),
                    output_index: i,
                    amount: 50,
                    owner: format!("addr_r{}_i{}", round, i),
                };
                
                let new_utxo = UTXO {
                    tx_hash: format!("new_tx_r{}_i{}", round, i),
                    output_index: 0,
                    amount: 50,
                    owner: format!("addr_dest_r{}_i{}", round, i),
                };
                
                let tx = Transaction::new(vec![utxo], vec![new_utxo]);
                blockchain.assign_transaction(tx);
            }
        }
    }
    
    // Generate master chain block (10 minute interval)
    println!("\n--- Master Chain Block Generation (10 min) ---");
    blockchain.generate_master_block(all_side_refs);
    
    // Display statistics
    blockchain.display_stats();
    
    // Demonstrate miner assignment algorithm
    println!("--- Miner Assignment Algorithm ---");
    for miner_id in 0..5 {
        let (sc1, sc2) = assign_miner_to_sidechains(miner_id, num_side_chains);
        println!("⛏️  Miner {} → Side Chains ({}, {})", miner_id, sc1, sc2);
    }
    
    // Display theoretical scalability analysis
    println!("\n--- Theoretical Scalability Analysis ---");
    for n in [1, 5, 10, 20] {
        let temp_chain = Chain::new(n, master_difficulty);
        let tps = temp_chain.calculate_tps(1000, 100);
        println!("   {} side chains → {:.2} TPS", n, tps);
    }
    
    println!("\n✅ Chain demonstration completed successfully!\n");
}
