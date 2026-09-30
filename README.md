<p align="center">
  <img src="assets/flop_banner.png" alt="FLOP Network" width="520" />
</p>

# 🔒 FLOP Key Vault (Offline DID & Keypair Custody Toolkit)

### Sovereign Offline Ed25519 Identity Generator, Multicodec Inspector & Paper Wallet Custody

[![Technocore Schema](https://img.shields.io/badge/technocore--schema-v1-blue.svg)](https://technocore.chat)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-green.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Witness DID](https://img.shields.io/badge/Witnessed%20by-did%3Akey%3Az6MkoTfk...-blueviolet.svg)](#-cryptographic-proof-of-contribution)

> **Overview**: An air-gapped, zero-network cryptographic toolkit designed for **FLOP Network (flop.finance / Technocore)** node operators and validators.  
> Enables generation of encrypted PKCS#8 Ed25519 identities, derivation of W3C `did:key:z...` sovereign identifiers, offline DID payload inspection, and export of tamper-evident printable paper custody cards.

---

## 🔑 Cryptographic Proof of Contribution

This tool is cryptographically signed and maintained by the **bitonekf** validator node:
* **Operator DID**:  
  `did:key:z6MkoTfkJhMK5deG5fVPLcAlsLNtxhrdsx8p7KsC5g1S58BN`
* **Canonical Specification**: `technocore-contribution-proof-v1`
* **Witness File**: [`contribution-proof.json`](contribution-proof.json)

---

## 🛡 Security Architecture & Capabilities

```text
┌─────────────────────────────────────────────────────────────┐
│                 AIR-GAPPED ENVIRONMENT                      │
│                                                             │
│   [ Ed25519 Entropy ] ──> PKCS#8 Passphrase Encryption      │
│            │              └─> identity.pem (chmod 0600)     │
│            ▼                                                │
│   Multicodec (0xed01) + Raw Pubkey ──> Base58BTC Encode     │
│            │                                                │
│            ├─> did:key:z6Mk... (W3C Standard)               │
│            ├─> inspect_did.py (Offline Hex Verification)    │
│            └─> paper_wallet_generator.py (Physical Storage) │
└─────────────────────────────────────────────────────────────┘
```

* 🛡 **Zero-Network Architecture**: Absolutely zero external network calls, preventing side-channel exfiltration or MITM leaks.
* 🔐 **PKCS#8 Scrypt/AES Encryption**: Private keys are protected using industry-standard encrypted envelopes with user passphrases.
* 📜 **Printable Paper Custody**: Generates formatted ASCII custody cards with SHA-256 fingerprint verification groups.
* 🔍 **Offline DID Inspector**: Decodes `did:key:z...` to reveal multicodec bytes, raw 32-byte public keys, and cryptographic curves without external APIs.
* 🧪 **Deterministic Test Suite**: Complete unit tests covering Base58BTC roundtrips, key derivation, and decryption fidelity.

---

## 📁 Repository Structure

```text
FLOP-Key-Vault/
├── vault/
│   ├── key_vault.py              # Sovereign DID generator and encrypted exporter
│   ├── inspect_did.py            # Offline W3C did:key decoder and public key extractor
│   └── paper_wallet_generator.py # Formatted paper custody card generator
├── tests/
│   └── test_crypto.py            # Cryptographic roundtrip and security test suite
├── assets/
│   └── flop_banner.png           # Official visual branding
├── contribution-proof.json       # Cryptographic Ed25519 signature proof
├── SECURITY.md                   # Air-gap custody and key hygiene policy
├── LICENSE                       # MIT License
└── README.md
```

---

## 🚀 Quickstart

### 1. Generate Encrypted DID Identity
```bash
# Generate offline keypair under ./vault_keys/
python3 vault/key_vault.py --out ./my_vault
```

### 2. Inspect and Decode DID
```bash
python3 vault/inspect_did.py did:key:z6MkoTfkJhMK5deG5fVPLcAlsLNtxhrdsx8p7KsC5g1S58BN
```

### 3. Export Paper Custody Card
```bash
python3 vault/paper_wallet_generator.py \
  --did did:key:z6MkoTfkJhMK5deG5fVPLcAlsLNtxhrdsx8p7KsC5g1S58BN \
  --key ./my_vault/identity.pem \
  --label "Validator Node Tab 2"
```

### 4. Run Offline Test Suite
```bash
python3 -m unittest discover -s tests
```

---

## ⚖️ License
Released under the [MIT License](LICENSE).
