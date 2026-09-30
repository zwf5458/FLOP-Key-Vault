#!/usr/bin/env python3
"""
FLOP Technocore Key Vault (Offline DID Security Toolkit)
Zero-network cryptographic generator, PKCS#8 encrypted exporter, and paper backup utility.
Author: Technocore Key Guardians
License: MIT
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

BASE58BTC_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
MULTICODEC_ED25519 = b"\xed\x01"

def base58btc_encode(data: bytes) -> str:
    """Encode bytes using Base58BTC format without third-party dependencies."""
    numeric = int.from_bytes(data, byteorder="big")
    chars = []
    while numeric > 0:
        numeric, remainder = divmod(numeric, 58)
        chars.append(BASE58BTC_ALPHABET[remainder])
    leading_zero_count = len(data) - len(data.lstrip(b"\x00"))
    chars.extend(BASE58BTC_ALPHABET[0] for _ in range(leading_zero_count))
    return "".join(reversed(chars))

def did_from_private_key(priv_key: Ed25519PrivateKey) -> str:
    pub_bytes = priv_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    payload = MULTICODEC_ED25519 + pub_bytes
    return f"did:key:z{base58btc_encode(payload)}"

def generate_vault_identity(out_dir: Path, passphrase: str) -> dict:
    """Generate an offline, PKCS#8 encrypted Ed25519 keypair."""
    out_dir.mkdir(parents=True, exist_ok=True)
    key = Ed25519PrivateKey.generate()
    did = did_from_private_key(key)
    
    enc = serialization.BestAvailableEncryption(passphrase.encode("utf-8"))
    pem_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=enc,
    )
    
    pem_path = out_dir / "identity.pem"
    if pem_path.exists():
        raise FileExistsError(f"Target identity already exists at {pem_path}")
        
    with open(pem_path, "wb") as f:
        f.write(pem_bytes)
    os.chmod(pem_path, 0o600)
    
    # Paper backup fingerprint
    sha = hashlib.sha256(pem_bytes).hexdigest()
    
    return {
        "did": did,
        "pem_path": str(pem_path),
        "fingerprint_sha256": sha,
    }

def print_paper_wallet(info: dict) -> None:
    print("\n" + "=" * 62)
    print("🔒 FLOP Technocore Cold Storage Paper Backup")
    print("=" * 62)
    print(f"Decentralized ID (DID):  {info['did']}")
    print(f"Keyfile Location:        {info['pem_path']} (chmod 600)")
    print(f"Keyfile SHA-256 Hash:    {info['fingerprint_sha256']}")
    print("-" * 62)
    print("⚠️  COLD VAULT DIRECTIVE:")
    print("  • Keep this passphrase offline.")
    print("  • Never commit 'identity.pem' to Git or upload to servers.")
    print("  • This DID represents your sovereign Proof-of-Inference credit.")
    print("=" * 62 + "\n")

def main():
    parser = argparse.ArgumentParser(description="FLOP Technocore Offline Key Vault")
    parser.add_argument("--out", default="./vault_keys", help="Directory to save generated identity.pem")
    args = parser.parse_args()
    
    print("--- 🔐 Generating Offline Sovereign DID ---")
    p1 = getpass.getpass("Enter strong encryption passphrase: ")
    p2 = getpass.getpass("Confirm encryption passphrase: ")
    if p1 != p2:
        print("Error: Passphrases do not match.", file=sys.stderr)
        sys.exit(1)
    if len(p1) < 8:
        print("Error: Passphrase must be at least 8 characters.", file=sys.stderr)
        sys.exit(1)
        
    try:
        info = generate_vault_identity(Path(args.out), p1)
        print_paper_wallet(info)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
