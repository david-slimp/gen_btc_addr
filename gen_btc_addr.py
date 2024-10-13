# gen_btc_addr.py
# A script to generate Bitcoin private keys, public keys, and addresses in various formats.
# Author: David Slimp <rock808@David-Slimp.com>
# 
# Changelog
# 20241012 - 0.1.0 - Rewrote the script from scratch (using ChatGPT 4o) without using the bitcoinlib module

import os
import sys
import ecdsa
import hashlib
import base58
import binascii
import base64
import bech32

def generate_key_pair(private_key_hex=None):
    # Hardcoded curve order
    HARDCODED_CURVE_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    # Curve order from the library
    CURVE_ORDER = ecdsa.SECP256k1.order

    # Check if the library's curve order matches the hardcoded value
    if CURVE_ORDER != HARDCODED_CURVE_ORDER:
        raise ValueError("Curve order mismatch: the library's curve order does not match the expected hardcoded value.")

    if private_key_hex:
        # Step 1: Use the provided private key
        try:
            private_key_bytes = bytes.fromhex(private_key_hex)
        except ValueError:
            raise ValueError("Invalid private key format: must be a valid hexadecimal string.")

        private_key_int = int(private_key_hex, 16)
        if private_key_int >= CURVE_ORDER or private_key_int == 0:
            raise ValueError("Invalid private key: must be a number between 1 and curve order - 1.")
        if len(private_key_bytes) != 32:
            raise ValueError("Invalid private key length: must be 32 bytes.")
    else:
        # Step 1: Generate a 32-byte private key using /dev/urandom
        while True:
            private_key_bytes = os.urandom(32)
            private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
            if 0 < private_key_int < CURVE_ORDER:
                break

    private_key_hex = private_key_bytes.hex()

    # Convert private key to WIF (Wallet Import Format) - Uncompressed
    extended_key = b'\x80' + private_key_bytes  # Add 0x80 byte in front for mainnet
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
    wif = base58.b58encode(extended_key + checksum).decode()

    # Convert private key to WIF (Wallet Import Format) - Compressed
    extended_key_compressed = b'\x80' + private_key_bytes + b'\x01'  # Add 0x80 byte in front for mainnet, plus 0x01 for compressed
    checksum_compressed_wif = hashlib.sha256(hashlib.sha256(extended_key_compressed).digest()).digest()[:4]
    wif_compressed = base58.b58encode(extended_key_compressed + checksum_compressed_wif).decode()

    # Convert private key to Base64
    private_key_base64 = base64.b64encode(private_key_bytes).decode()

    # Step 2: Generate a public key using the ECDSA library and secp256k1 curve
    sk = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    public_key_bytes = b'\x04' + vk.to_string()  # Add 0x04 prefix to indicate uncompressed key

    if vk.to_string()[-1] % 2 == 0:
        public_key_bytes_compressed = b'\x02' + vk.to_string()[:32]
    else:
        public_key_bytes_compressed = b'\x03' + vk.to_string()[:32]

    public_key_hex = public_key_bytes.hex()
    public_key_compressed_hex = public_key_bytes_compressed.hex()

    # Step 3: Generate the Bitcoin address from the uncompressed public key
    # Hash the public key using SHA-256, then RIPEMD-160
    sha256_hash = hashlib.sha256(public_key_bytes).digest()
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(sha256_hash)
    public_key_hash = ripemd160.digest()

    # Add network byte (0x00 for mainnet)
    network_byte = b'\x00'
    public_key_hash_with_network = network_byte + public_key_hash

    # Double hash using SHA-256 to calculate checksum
    checksum = hashlib.sha256(hashlib.sha256(public_key_hash_with_network).digest()).digest()[:4]

    # Append the checksum to the public key hash with network byte
    address_bytes = public_key_hash_with_network + checksum

    # Encode in Base58 to get the final Bitcoin address (uncompressed)
    public_address_uncompressed = base58.b58encode(address_bytes).decode()

    # Step 4: Generate the Bitcoin address from the compressed public key
    # Hash the compressed public key using SHA-256, then RIPEMD-160
    sha256_hash_compressed = hashlib.sha256(public_key_bytes_compressed).digest()
    ripemd160_compressed = hashlib.new('ripemd160')
    ripemd160_compressed.update(sha256_hash_compressed)
    public_key_hash_compressed = ripemd160_compressed.digest()

    # Add network byte (0x00 for mainnet)
    public_key_hash_with_network_compressed = network_byte + public_key_hash_compressed

    # Double hash using SHA-256 to calculate checksum
    checksum_compressed = hashlib.sha256(hashlib.sha256(public_key_hash_with_network_compressed).digest()).digest()[:4]

    # Append the checksum to the public key hash with network byte
    address_bytes_compressed = public_key_hash_with_network_compressed + checksum_compressed

    # Encode in Base58 to get the final Bitcoin address (compressed)
    public_address_compressed = base58.b58encode(address_bytes_compressed).decode()

    # Step 5: Generate the Bech32 address from the compressed public key
    # Hash the compressed public key using SHA-256, then RIPEMD-160
    sha256_hash_compressed = hashlib.sha256(public_key_bytes_compressed).digest()
    ripemd160_compressed = hashlib.new('ripemd160')
    ripemd160_compressed.update(sha256_hash_compressed)
    witness_program = ripemd160_compressed.digest()  # Using the compressed public key hash
    hrp = 'bc'  # Human-readable part for mainnet
    witness_version = 0  # Bech32 address witness version is 0 for P2WPKH
    bech32_data = bech32.convertbits(witness_program, 8, 5, True)
    if bech32_data is None:
        raise ValueError("Error converting witness program to 5-bit.")

    # Generate the Bech32 address
    bech32_address = bech32.bech32_encode(hrp, [witness_version] + bech32_data)

    return private_key_hex, wif, wif_compressed, private_key_base64, public_key_hex, public_key_compressed_hex, public_address_uncompressed, public_address_compressed, bech32_address

if __name__ == "__main__":
    # Parse command-line arguments
    private_key_hex = None
    if len(sys.argv) > 1 and sys.argv[1] == "-k":
        if len(sys.argv) > 2:
            private_key_hex = sys.argv[2]
        else:
            print("Error: No private key provided after '-k' argument.")
            sys.exit(1)

    # Generate keys and address
    try:
        private_key, wif, wif_compressed, private_key_base64, public_key, public_key_compressed, public_address_uncompressed, public_address_compressed, bech32_address = generate_key_pair(private_key_hex)
        print(f"PUBLIC:")
        print(f"    Bitcoin Address (Uncompressed, Base58): {public_address_uncompressed}")
        print(f"    Bitcoin Address (Compressed, Base58): {public_address_compressed}")
        print(f"    Public Key (uncompressed Hex): {public_key} (Length: {len(public_key)})")
        print(f"    Public Key compressed (Hex): {public_key_compressed} (Length: {len(public_key_compressed)})")
        print(f"    Public Bech32 Address: {bech32_address}")

        print(f"PRIVATE:")
        print(f"    Private Key WIF (uncompressed): {wif} (Length: {len(wif)})")
        print(f"    Private Key WIF (Compressed): {wif_compressed} (Length: {len(wif_compressed)})")
        print(f"    Private Key (Hex): {private_key} (Length: {len(private_key)})")
        print(f"    Private Key (Base64): {private_key_base64} (Length: {len(private_key_base64)})")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
