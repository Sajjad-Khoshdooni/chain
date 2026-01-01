// Auto-generated benchmark script
use chain::{Chain, Transaction, UTXO};
use std::time::Instant;

fn main() {
    let num_side_chains = 10;
    let num_transactions = 500;
    let rounds = 3;
    let master_difficulty = 2;
    let side_difficulty = 2;
    
    println!("BENCHMARK_START");
    println!("CONFIG: side_chains={}, transactions={}, rounds={}", num_side_chains, num_transactions, rounds);
    
    // Initialize blockchain
    let init_start = Instant::now();
    let mut blockchain = Chain::new(num_side_chains, master_difficulty);
    let init_time = init_start.elapsed();
    println!("INIT_TIME: {:.3}", init_time.as_secs_f64());
    
    // Phase 1: Transaction creation and assignment
    let tx_start = Instant::now();
    for i in 0..num_transactions {
        let utxo = UTXO {
            tx_hash: format!("prev_tx_{}", i),
            output_index: i as u32,
            amount: 100 + i as u64 * 10,
            owner: format!("address_{}", i % 100),
        };
        
        let new_utxo = UTXO {
            tx_hash: format!("new_tx_{}", i),
            output_index: 0,
            amount: 100 + i as u64 * 10,
            owner: format!("address_{}", (i + 1) % 100),
        };
        
        let tx = Transaction::new(vec![utxo], vec![new_utxo]);
        blockchain.assign_transaction(tx);
    }
    let tx_time = tx_start.elapsed();
    println!("TX_CREATION_TIME: {:.3}", tx_time.as_secs_f64());
    
    // Phase 2: Side chain block generation
    let mut all_side_refs = Vec::new();
    let mut side_times = Vec::new();
    
    for round in 0..rounds {
        let round_start = Instant::now();
        let refs = blockchain.generate_side_chain_blocks(side_difficulty);
        let round_time = round_start.elapsed();
        side_times.push(round_time.as_secs_f64());
        println!("SIDE_ROUND_{}_TIME: {:.3}", round, round_time.as_secs_f64());
        all_side_refs.extend(refs);
    }
    
    let avg_side_time = side_times.iter().sum::<f64>() / side_times.len() as f64;
    println!("AVG_SIDE_TIME: {:.3}", avg_side_time);
    
    // Phase 3: Master block generation
    let master_start = Instant::now();
    blockchain.generate_master_block(all_side_refs);
    let master_time = master_start.elapsed();
    println!("MASTER_TIME: {:.3}", master_time.as_secs_f64());
    
    // Calculate statistics
    let total_time = init_time.as_secs_f64() + tx_time.as_secs_f64() + 
                     side_times.iter().sum::<f64>() + master_time.as_secs_f64();
    let tps = num_transactions as f64 / total_time;
    
    println!("TOTAL_TIME: {:.3}", total_time);
    println!("TPS: {:.2}", tps);
    println!("TOTAL_TRANSACTIONS: {}", num_transactions);
    
    // Block statistics
    println!("MASTER_BLOCKS: {}", blockchain.master_chain.blocks.len());
    println!("SIDE_BLOCKS: {}", blockchain.side_chains.iter().map(|sc| sc.blocks.len()).sum::<usize>());
    
    println!("BENCHMARK_END");
}
