<p align="center">
  <img src="assets/flop_banner.png" alt="FLOP Network" width="520" />
</p>

# 🔐 FLOP Key Vault (Offline DID Security Toolkit)

### Zero-Network Sovereign Identity Generator & PKCS#8 Cold Storage Vault for FLOP Technocore

[![Technocore Schema](https://img.shields.io/badge/technocore--schema-v1-blue.svg)](https://technocore.chat)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-green.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Witness DID](https://img.shields.io/badge/Witnessed%20by-did%3Akey%3Az6MkoTfk...-blueviolet.svg)](#-cryptographic-proof-of-contribution)

> **Overview**: A standalone, zero-network utility designed for **FLOP Network (flop.finance / Technocore)** developers and node operators.  
> Ensures sovereign Ed25519 identity generation, PKCS#8 passphrase-protected encryption, Base58BTC multibase derivation, and air-gapped paper wallet exports.

---

## 🔑 Cryptographic Proof of Contribution

This tool is cryptographically signed and maintained by the **bitonekf** validator node:
* **Operator DID**:  
  `did:key:z6MkoTfkJhMK5deG5fVPLcAlsLNtxhrdsx8p7KsC5g1S58BN`
* **Canonical Specification**: `technocore-contribution-proof-v1`

---

## 🛡 Security Design Principles

* 🔌 **100% Air-Gapped**: Zero network socket calls, zero third-party telemetry. Can be executed on fully disconnected offline machines.
* 🔐 **PKCS#8 Best-Available Encryption**: Encrypts private keys using AES-256-CBC/PBKDF2 via standard OpenSSL cryptographic primitives.
* 📜 **Paper Backup Generation**: Derives deterministic SHA-256 integrity checksums for cold storage verification.

---

## 🚀 Quickstart

```bash
# 1. Clone repository
git clone https://github.com/zwf5458/FLOP-Key-Vault.git
cd FLOP-Key-Vault

# 2. Install minimal cryptographic primitives
pip install cryptography>=41.0.0

# 3. Generate a secure, encrypted offline identity
python3 vault/key_vault.py --out ./my_cold_keys
```

---

## ⚖️ License
Released under the [MIT License](LICENSE).
