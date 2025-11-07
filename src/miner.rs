/// Assigns a miner to two distinct side chains based on their unique miner_id
/// 
/// Algorithm:
/// - side_chain_1 = miner_id % N
/// - side_chain_2 = (miner_id / N) % N
/// 
/// This ensures even distribution of miners across side chains
/// and prevents centralization of mining power
pub fn assign_miner_to_sidechains(miner_id: u64, num_side_chains: usize) -> (usize, usize) {
    let side_chain_1 = (miner_id % num_side_chains as u64) as usize;
    let side_chain_2 = ((miner_id / num_side_chains as u64) % num_side_chains as u64) as usize;
    (side_chain_1, side_chain_2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_miner_assignment() {
        let num_chains = 10;
        
        // Test miner 15 (from the paper example)
        let (sc1, sc2) = assign_miner_to_sidechains(15, num_chains);
        assert_eq!(sc1, 5);
        assert_eq!(sc2, 1);
        
        // Test miner 0
        let (sc1, sc2) = assign_miner_to_sidechains(0, num_chains);
        assert_eq!(sc1, 0);
        assert_eq!(sc2, 0);
    }
    
    #[test]
    fn test_miner_distribution() {
        let num_chains = 5;
        
        for miner_id in 0..25 {
            let (sc1, sc2) = assign_miner_to_sidechains(miner_id, num_chains);
            assert!(sc1 < num_chains);
            assert!(sc2 < num_chains);
        }
    }
}

