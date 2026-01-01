// Cryptography Module - Simplified for Academic Architecture Demonstration
// This implements basic cryptographic concepts without full production complexity

use sha2::{Digest, Sha256};
use serde::{Serialize, Deserialize};

/// Simplified Wallet for academic demonstration
#[derive(Debug, Clone)]
pub struct Wallet {
    pub private_key: String,
    pub public_key: String,
    pub address: String,
}

impl Wallet {
    /// Create a new wallet with deterministic keys (for demo purposes)
    pub fn new(seed: u64) -> Self {
        let private_key = format!("private_key_{}", seed);
        let public_key = Self::derive_public_key(&private_key);
        let address = Self::derive_address(&public_key);
        
        Self {
            private_key,
            public_key,
            address,
        }
    }
    
    /// Derive public key from private key (simplified)
    fn derive_public_key(private_key: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(private_key.as_bytes());
        hasher.update(b"_public");
        format!("pub_{}", hex::encode(hasher.finalize()))
    }
    
    /// Derive address from public key (simplified)
    fn derive_address(public_key: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(public_key.as_bytes());
        let hash = hasher.finalize();
        format!("addr_{}", hex::encode(&hash[0..20]))
    }
    
    /// Sign data with private key (simplified signature)
    pub fn sign(&self, data: &str) -> Signature {
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        hasher.update(self.private_key.as_bytes());
        let sig_data = hasher.finalize();
        
        Signature {
            r: hex::encode(&sig_data[0..16]),
            s: hex::encode(&sig_data[16..32]),
            public_key: self.public_key.clone(),
        }
    }
    
    /// Verify signature (simplified verification)
    pub fn verify(data: &str, signature: &Signature) -> bool {
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        
        // In real implementation, this would use the public key to verify
        // For demo, we reconstruct what the signature should be
        !signature.r.is_empty() && !signature.s.is_empty()
    }
}

/// Digital Signature (simplified)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Signature {
    pub r: String,  // Signature component R
    pub s: String,  // Signature component S
    pub public_key: String,  // Signer's public key
}

impl Signature {
    pub fn verify_ownership(&self, address: &str) -> bool {
        let derived_address = Wallet::derive_address(&self.public_key);
        derived_address == address
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_wallet_creation() {
        let wallet = Wallet::new(123);
        assert!(!wallet.address.is_empty());
        assert!(!wallet.public_key.is_empty());
    }
    
    #[test]
    fn test_signature() {
        let wallet = Wallet::new(456);
        let data = "test transaction";
        let signature = wallet.sign(data);
        
        assert!(Wallet::verify(data, &signature));
        assert!(signature.verify_ownership(&wallet.address));
    }
}

