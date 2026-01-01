// Demonstration of enhanced architecture features
// This showcases: Cryptography, Consensus, Validation, and Cross-Chain Communication

use chain::{
    Chain, Transaction, UTXO,
    Wallet, Signature,
    ConsensusRules, ForkResolver, ByzantineFaultTolerance,
    TransactionValidator, UtxoSet,
    CrossChainBridge, TransferStatus,
};

fn main() {
    println!("╔════════════════════════════════════════════════╗");
    println!("║    Chain - Enhanced Architecture Demo         ║");
    println!("║  Cryptography | Consensus | Validation | XChain║");
    println!("╚════════════════════════════════════════════════╝\n");
    
    // ========== 1. CRYPTOGRAPHY DEMO ==========
    println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("1️⃣  CRYPTOGRAPHY MODULE");
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    
    // Create wallets
    let alice = Wallet::new(100);
    let bob = Wallet::new(200);
    let charlie = Wallet::new(300);
    
    println!("✅ Created 3 wallets:");
    println!("   Alice:   {} ", &alice.address[..30]);
    println!("   Bob:     {}", &bob.address[..30]);
    println!("   Charlie: {}", &charlie.address[..30]);
    
    // Sign and verify
    let message = "Transfer 50 coins to Bob";
    let signature = alice.sign(message);
    let is_valid = Wallet::verify(message, &signature);
    
    println!("\n🔐 Digital Signature:");
    println!("   Message: {}", message);
    println!("   Signature valid: ✓ {}", is_valid);
    println!("   Owner verified: ✓ {}", signature.verify_ownership(&alice.address));
    
    // ========== 2. CONSENSUS DEMO ==========
    println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("2️⃣  CONSENSUS MODULE");
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    
    // Fork resolution
    let rules = ConsensusRules::new();
    let resolver = ForkResolver::new(rules);
    
    let chain_a = Chain::new(3, 3);
    let mut chain_b = Chain::new(3, 3);
    
    // Make chain B longer
    chain_b.generate_master_block(vec![]);
    chain_b.generate_master_block(vec![]);
    
    println!("🔀 Fork Resolution:");
    println!("   Chain A length: {}", chain_a.master_chain.blocks.len());
    println!("   Chain B length: {}", chain_b.master_chain.blocks.len());
    
    // Validate chain
    match resolver.validate_chain(&chain_a.master_chain) {
        Ok(_) => println!("   ✓ Chain A is valid"),
        Err(e) => println!("   ✗ Chain A is invalid: {:?}", e),
    }
    
    // Finality check
    let is_finalized = resolver.is_finalized(1, 10);
    println!("   Block #1 finalized at height 10: ✓ {}", is_finalized);
    
    // Byzantine Fault Tolerance
    let bft = ByzantineFaultTolerance::new(10);
    println!("\n🛡️  Byzantine Fault Tolerance:");
    println!("   Total nodes: 10");
    println!("   Max Byzantine nodes tolerated: {}", bft.max_byzantine_nodes());
    println!("   Consensus with 7 votes: ✓ {}", bft.has_consensus(7));
    println!("   Consensus with 6 votes: ✗ {}", bft.has_consensus(6));
    
    // ========== 3. TRANSACTION VALIDATION DEMO ==========
    println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("3️⃣  TRANSACTION VALIDATION MODULE");
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    
    // Create UTXO set
    let mut utxo_set = UtxoSet::new();
    
    // Add initial UTXO for Alice
    let genesis_utxo = UTXO {
        tx_hash: "genesis".to_string(),
        output_index: 0,
        amount: 100_000,
        owner: alice.address.clone(),
    };
    utxo_set.add_utxo(genesis_utxo.clone());
    
    println!("💰 Initial Balances:");
    println!("   Alice: {} satoshis", utxo_set.get_balance(&alice.address));
    println!("   Bob:   {} satoshis", utxo_set.get_balance(&bob.address));
    
    // Create valid transaction
    let tx = Transaction::new(
        vec![genesis_utxo],
        vec![
            UTXO {
                tx_hash: String::new(),
                output_index: 0,
                amount: 50_000,
                owner: bob.address.clone(),
            },
            UTXO {
                tx_hash: String::new(),
                output_index: 1,
                amount: 48_000,
                owner: alice.address.clone(),  // Change back to Alice
            },
        ],
    );
    
    println!("\n📝 Transaction created:");
    println!("   ID: {}", &tx.id[..16]);
    println!("   Inputs:  1 (100,000 satoshis)");
    println!("   Outputs: 2 (50,000 + 48,000 = 98,000 satoshis)");
    println!("   Fee:     2,000 satoshis");
    
    // Validate transaction
    let mut validator = TransactionValidator::with_utxo_set(utxo_set);
    
    match validator.validate_transaction(&tx) {
        Ok(_) => {
            println!("   ✓ Transaction is valid");
            
            // Apply transaction
            validator.apply_transaction(&tx).unwrap();
            
            let utxo_set_ref = validator.get_utxo_set();
            println!("\n💰 Updated Balances:");
            println!("   Alice: {} satoshis", utxo_set_ref.get_balance(&alice.address));
            println!("   Bob:   {} satoshis", utxo_set_ref.get_balance(&bob.address));
        }
        Err(e) => println!("   ✗ Transaction invalid: {:?}", e),
    }
    
    // Test double-spend detection
    println!("\n🚨 Double-Spend Detection:");
    let double_spend_tx = Transaction::new(
        vec![UTXO {
            tx_hash: "genesis".to_string(),
            output_index: 0,
            amount: 100_000,
            owner: alice.address.clone(),
        }],
        vec![UTXO {
            tx_hash: String::new(),
            output_index: 0,
            amount: 99_000,
            owner: charlie.address.clone(),
        }],
    );
    
    match validator.validate_transaction(&double_spend_tx) {
        Ok(_) => println!("   ✗ Should have detected double-spend!"),
        Err(_) => println!("   ✓ Double-spend detected and rejected"),
    }
    
    // ========== 4. CROSS-CHAIN COMMUNICATION DEMO ==========
    println!("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    println!("4️⃣  CROSS-CHAIN COMMUNICATION MODULE");
    println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    
    let mut bridge = CrossChainBridge::new();
    
    // Initiate cross-chain transfer
    let transfer_id = bridge.initiate_transfer(
        0,  // From side chain 0
        2,  // To side chain 2
        25_000,
        alice.address.clone(),
        bob.address.clone(),
    ).unwrap();
    
    println!("   Transfer ID: {}", transfer_id);
    println!("   Status: {:?}", bridge.get_transfer_status(&transfer_id).unwrap());
    
    // Execute transfer protocol
    println!("\n🔄 Transfer Protocol Execution:");
    
    // Step 1: Lock funds
    bridge.lock_funds(&transfer_id).unwrap();
    println!("   Status: {:?}", bridge.get_transfer_status(&transfer_id).unwrap());
    
    // Step 2: Verify through master chain
    bridge.verify_transfer(&transfer_id, "master_block_abc123").unwrap();
    println!("   Status: {:?}", bridge.get_transfer_status(&transfer_id).unwrap());
    
    // Step 3: Complete on target chain
    let completed = bridge.complete_transfer(&transfer_id).unwrap();
    println!("   Status: {:?}", completed.status);
    println!("   ✅ Cross-chain transfer completed successfully!");
    
    // Atomic Swap Demo
    use chain::AtomicSwapProtocol;
    
    println!("\n⚛️  Atomic Swap Protocol:");
    let secret = "atomic_secret_12345";
    let time_lock = 9999999999;
    let swap = AtomicSwapProtocol::new(secret, time_lock);
    
    println!("   Hash lock: {}", &swap.hash_lock[..32]);
    println!("   Time lock: {}", time_lock);
    println!("   Secret verified: ✓ {}", swap.verify_secret(secret));
    println!("   Wrong secret rejected: ✓ {}", !swap.verify_secret("wrong"));
    
    // ========== SUMMARY ==========
    println!("\n╔════════════════════════════════════════════════╗");
    println!("║              DEMO COMPLETED                    ║");
    println!("╚════════════════════════════════════════════════╝");
    
    println!("\n📊 Enhanced Architecture Features:");
    println!("   ✅ Cryptography: Wallets, signatures, verification");
    println!("   ✅ Consensus: Fork resolution, BFT, finality");
    println!("   ✅ Validation: UTXO tracking, double-spend detection");
    println!("   ✅ Cross-Chain: Inter-sidechain transfers, atomic swaps");
    
    println!("\n🎯 Key Achievements:");
    println!("   • Deterministic wallet generation");
    println!("   • Byzantine Fault Tolerance (tolerates f < n/3 faults)");
    println!("   • Complete transaction validation pipeline");
    println!("   • 4-phase cross-chain transfer protocol");
    println!("   • Atomic swap with hash-time locks");
    
    println!("\n✨ Architecture now includes:");
    println!("   Original: Master Chain + Side Chains + PoW");
    println!("   Added:    Crypto + Consensus + Validation + Cross-Chain");
    println!("\n🎓 Ready for enhanced thesis presentation!\n");
}

