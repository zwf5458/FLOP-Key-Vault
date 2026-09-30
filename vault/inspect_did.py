#!/usr/bin/env python3
"""
FLOP Technocore DID Inspector
Decodes a W3C did:key:z... identifier into raw Ed25519 public key bytes and hex fingerprint.
Operates 100% offline with zero external network connectivity.
"""

from __future__ import annotations

import argparse
import sys

BASE58BTC_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
BASE58_MAP = {c: i for i, c in enumerate(BASE58BTC_ALPHABET)}
MULTICODEC_ED25519_PREFIX = b"\xed\x01"


def base58btc_decode(s: str) -> bytes:
    """Decode a Base58BTC string into raw bytes."""
    if not s:
        return b""
    num = 0
    for char in s:
        if char not in BASE58_MAP:
            raise ValueError(f"Invalid Base58BTC character: {char}")
        num = num * 58 + BASE58_MAP[char]

    # Convert integer to bytes
    res = []
    while num > 0:
        num, rem = divmod(num, 256)
        res.append(rem)
    raw = bytes(reversed(res))

    # Add back leading zero bytes
    pad_len = 0
    for c in s:
        if c == "1":
            pad_len += 1
        else:
            break
    return (b"\x00" * pad_len) + raw


def inspect_did(did: str) -> dict:
    """Inspect and validate a did:key identifier."""
    if not did.startswith("did:key:z"):
        raise ValueError(f"Invalid DID prefix, expected 'did:key:z...', got: {did}")

    encoded_payload = did[len("did:key:z") :]
    raw_payload = base58btc_decode(encoded_payload)

    if not raw_payload.startswith(MULTICODEC_ED25519_PREFIX):
        raise ValueError(
            f"Unsupported multicodec prefix: {raw_payload[:2].hex()}, expected 0xed01 (Ed25519)"
        )

    pub_bytes = raw_payload[2:]
    if len(pub_bytes) != 32:
        raise ValueError(f"Invalid Ed25519 public key length: {len(pub_bytes)} bytes (expected 32)")

    return {
        "did": did,
        "curve": "Ed25519",
        "multicodec_prefix": "0xed01",
        "public_key_hex": pub_bytes.hex(),
        "key_length_bytes": len(pub_bytes),
    }


def main():
    parser = argparse.ArgumentParser(description="FLOP Technocore DID Inspector")
    parser.add_argument("did", help="The did:key:z... string to inspect")
    args = parser.parse_args()

    try:
        info = inspect_did(args.did)
        print("🔍 Technocore DID Inspection Result:")
        print(f"  • DID:               {info['did']}")
        print(f"  • Curve:             {info['curve']}")
        print(f"  • Multicodec:        {info['multicodec_prefix']} (Ed25519 Public Key)")
        print(f"  • Public Key (Hex):  {info['public_key_hex']}")
        print(f"  • Length:            {info['key_length_bytes']} bytes (256 bits)")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
