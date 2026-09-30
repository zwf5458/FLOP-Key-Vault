# Security & Key Management Policy

## 🔒 Security Standards for FLOP Technocore Key Vault

The **FLOP-Key-Vault** is an offline cryptographic utility engineered for the Arthur Hayes FLOP Network and Technocore decentralized ecosystem. It manages high-value Ed25519 private keys and W3C `did:key` sovereign identities.

---

### 1. Air-Gapped Key Generation Principles

* **Zero Network Dependency**: None of the tools in `vault/` import network sockets, HTTP clients, or DNS resolution libraries. All derivations (Base58BTC, Multicodec `0xed01`, Ed25519) execute 100% locally.
* **Strict PKCS#8 Scrypt/AES Encryption**: Private keys are never written to disk in plaintext. All generated keys are encrypted using PKCS#8 format with user-supplied passphrases.
* **Posix File Permissions**: Newly generated keyfiles are created with atomic `chmod 0600` permissions, restricted solely to the executing user.

---

### 2. Operational Security Directives

1. **Air-Gap Recommendation**: High-value production DIDs should be generated on air-gapped workstations or live boot environments.
2. **Paper Backup Custody**: Printable custody cards generated via `paper_wallet_generator.py` should be stored in tamper-evident physical safes.
3. **Automated VPS Bot Segregation**: Do not deploy cold storage master DIDs on 24/7 cloud servers. Use independent ephemeral DIDs for VPS worker nodes.

---

### 3. Supported Versions

| Version | Supported          | Security Status |
| :---    | :---               | :---            |
| 1.1.x   | :white_check_mark: | Active Cryptographic Maintenance |
| 1.0.x   | :white_check_mark: | Legacy Maintenance |
| < 1.0   | :x:                | Deprecated |

---

### 4. Vulnerability Disclosure & Audit

To report cryptographic weaknesses, side-channel vulnerabilities, or entropy concerns:

* **Primary Maintainer DID (Tab 2 bitonekf)**:  
  `did:key:z6MkoTfkJhMK5deG5fVPLcAlsLNtxhrdsx8p7KsC5g1S58BN`
* **Maintainer Namespace**: `zwf5458/FLOP-Key-Vault`
* **Audit Channel**: Technocore Cryptography & Security Working Group. Disclosures will be acknowledged within 24 hours.
