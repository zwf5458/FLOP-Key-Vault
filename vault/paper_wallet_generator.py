#!/usr/bin/env python3
"""
FLOP Technocore Cold Storage Paper Wallet Exporter
Formats and exports cryptographic credentials into human-readable, printable ASCII paper custody cards.
Designed for high-security cold-air-gapped DID preservation.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path


def generate_paper_card(did: str, pem_path: str, label: str = "Technocore Contributor") -> str:
    pem_file = Path(pem_path)
    if not pem_file.exists():
        raise FileNotFoundError(f"PEM file not found at {pem_path}")

    with open(pem_file, "rb") as f:
        pem_content = f.read()

    sha256_fingerprint = hashlib.sha256(pem_content).hexdigest().upper()
    timestamp_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Format fingerprint in 8-char spaced groups
    spaced_fp = " ".join([sha256_fingerprint[i : i + 8] for i in range(0, len(sha256_fingerprint), 8)])

    border = "═" * 72
    card = f"""
╔{border}╗
║             FLOP NETWORK TECHNOCORE COLD STORAGE VAULT CARD           ║
║                     PROOF OF INFERENCE & CONTRIBUTION                 ║
╠{border}╣
║ Label:          {label:<54}║
║ Created At:     {timestamp_utc:<54}║
║ Status:         ENCRYPTED AIR-GAPPED CUSTODY                          ║
╠{border}╣
║ Sovereign DID:                                                        ║
║   {did:<68}║
╠{border}╣
║ Keyfile Path:                                                         ║
║   {str(pem_file.resolve()):<68}║
║ SHA-256 Checksum:                                                     ║
║   {spaced_fp[:68]:<68}║
║   {spaced_fp[68:]:<68}║
╠{border}╣
║ ⚠️  OPERATIONAL SECURITY DIRECTIVES:                                   ║
║  1. Store this printed card and private key passphrase separately.    ║
║  2. Never store your decryption passphrase on the same storage media. ║
║  3. Never commit 'identity.pem' to any public or private git repository.║
║  4. If key file is lost, signed proofs from this DID cannot be claimed.║
╚{border}╝
"""
    return card.strip()


def main():
    parser = argparse.ArgumentParser(description="Export Technocore Paper Wallet Card")
    parser.add_argument("--did", required=True, help="Decentralized Identifier (did:key:z...)")
    parser.add_argument("--key", required=True, help="Path to encrypted identity.pem")
    parser.add_argument("--label", default="Technocore Node Contributor", help="Label description")
    parser.add_argument("--out", default="", help="Optional output text file path")
    args = parser.parse_args()

    try:
        card = generate_paper_card(args.did, args.key, label=args.label)
        if args.out:
            out_file = Path(args.out)
            out_file.write_text(card, encoding="utf-8")
            print(f"📄 Paper custody card exported to: {out_file.resolve()}")
        else:
            print(card)
    except Exception as e:
        print(f"❌ Error generating paper card: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
