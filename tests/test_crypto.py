#!/usr/bin/env python3
"""
Unit tests for FLOP Key Vault offline cryptographic operations.
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from vault.inspect_did import base58btc_decode, inspect_did
from vault.key_vault import base58btc_encode, did_from_private_key, generate_vault_identity


class TestKeyVault(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_base58_roundtrip(self):
        test_cases = [
            b"hello world",
            b"\x00\x00\x01\x02\x03",
            b"\xed\x01" + b"\xff" * 32,
            b"",
        ]
        for data in test_cases:
            encoded = base58btc_encode(data)
            decoded = base58btc_decode(encoded)
            self.assertEqual(data, decoded)

    def test_did_derivation_and_inspection(self):
        priv_key = Ed25519PrivateKey.generate()
        did = did_from_private_key(priv_key)
        self.assertTrue(did.startswith("did:key:z6Mk"))

        # Inspect the derived DID
        info = inspect_did(did)
        self.assertEqual(info["curve"], "Ed25519")
        self.assertEqual(info["key_length_bytes"], 32)
        raw_pub = priv_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        self.assertEqual(info["public_key_hex"], raw_pub.hex())

    def test_generate_vault_identity_encrypted(self):
        passphrase = "UltraSecurePassphrase123!"
        res = generate_vault_identity(self.temp_dir, passphrase)
        pem_path = Path(res["pem_path"])
        self.assertTrue(pem_path.exists())

        # Verify file permissions
        mode = pem_path.stat().st_mode & 0o777
        self.assertEqual(mode, 0o600)

        # Read back and decrypt key
        with open(pem_path, "rb") as f:
            pem_bytes = f.read()

        loaded_key = serialization.load_pem_private_key(
            pem_bytes,
            password=passphrase.encode("utf-8"),
        )
        self.assertIsInstance(loaded_key, Ed25519PrivateKey)
        self.assertEqual(did_from_private_key(loaded_key), res["did"])

    def test_paper_wallet_card_generation(self):
        from vault.paper_wallet_generator import generate_paper_card

        passphrase = "PaperWalletPassphrase999!"
        res = generate_vault_identity(self.temp_dir, passphrase)
        card = generate_paper_card(res["did"], res["pem_path"], label="Test Node")
        self.assertIn("FLOP NETWORK TECHNOCORE COLD STORAGE VAULT CARD", card)
        self.assertIn(res["did"], card)
        self.assertIn("Test Node", card)



if __name__ == "__main__":
    unittest.main()
