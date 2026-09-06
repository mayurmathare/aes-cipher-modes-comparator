"""
crypto_engine.py
Core cryptographic service for AES Block Cipher Modes of Operation:
1. ECB (Electronic Codebook)
2. CBC (Cipher Block Chaining)
3. CFB (Cipher Feedback)
4. OFB (Output Feedback)
5. CTR (Counter Mode)
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import binascii


def validate_key(key_str: str) -> bytes:
    """
    Validates and converts key string to bytes.
    Standard AES keys must be 16, 24, or 32 bytes (128, 192, or 256 bits).
    Default key: '0123456789abcdef' (16 bytes).
    """
    key_bytes = key_str.encode('utf-8')
    if len(key_bytes) not in (16, 24, 32):
        raise ValueError(
            f"Invalid key length ({len(key_bytes)} bytes). AES key must be exactly 16, 24, or 32 bytes (128, 192, or 256 bits)."
        )
    return key_bytes


def format_hex_blocks(data: bytes, block_size: int = 16) -> list:
    """
    Splits byte data into block-sized chunks and returns their hex representations,
    indices, and raw text preview.
    """
    blocks = []
    total_blocks = (len(data) + block_size - 1) // block_size if len(data) > 0 else 0
    for i in range(total_blocks):
        chunk = data[i * block_size : (i + 1) * block_size]
        blocks.append({
            "index": i + 1,
            "hex": chunk.hex(),
            "formatted_hex": " ".join(chunk.hex()[j:j+2] for j in range(0, len(chunk.hex()), 2)),
            "byte_count": len(chunk),
            "ascii_preview": "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
        })
    return blocks


def compare_all_modes(plaintext: str, key_str: str) -> dict:
    """
    Encrypts the plaintext using ECB, CBC, CFB, OFB, and CTR modes with the same key.
    Generates IV / Nonce where required and verifies decryption.
    """
    key = validate_key(key_str)
    pt_bytes = plaintext.encode('utf-8')
    
    # 1. Generate fresh secure random IV (16 bytes) and Nonce (8 bytes)
    iv_16 = get_random_bytes(16)
    nonce_8 = get_random_bytes(8)
    
    results = {}
    
    # -------------------------------------------------------------
    # 1. ECB (Electronic Codebook)
    # -------------------------------------------------------------
    # No IV or Nonce
    # Requires PKCS#7 padding
    padded_pt_ecb = pad(pt_bytes, AES.block_size, style='pkcs7')
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    ct_ecb = cipher_ecb.encrypt(padded_pt_ecb)
    
    dec_cipher_ecb = AES.new(key, AES.MODE_ECB)
    decrypted_ecb = unpad(dec_cipher_ecb.decrypt(ct_ecb), AES.block_size, style='pkcs7').decode('utf-8', errors='replace')
    
    results['ECB'] = {
        'mode_name': 'ECB - Electronic Codebook',
        'short_name': 'ECB',
        'ciphertext_hex': ct_ecb.hex(),
        'ciphertext_formatted': " ".join(ct_ecb.hex()[i:i+2] for i in range(0, len(ct_ecb.hex()), 2)),
        'blocks': format_hex_blocks(ct_ecb, AES.block_size),
        'decrypted_plaintext': decrypted_ecb,
        'padding_requirement': 'Yes (PKCS#7 padding required to pad plaintext to 16-byte block multiple)',
        'padding_type': 'PKCS#7',
        'iv_nonce_requirement': 'None (ECB does not take an IV or Nonce)',
        'iv_hex': None,
        'security_observation': 'Repeated plaintext patterns can be revealed; identical plaintext blocks produce identical ciphertext blocks. Lacks semantic security; does not provide authentication.',
        'pattern_hiding': 'No',
        'parallel_encryption': 'Yes'
    }
    
    # -------------------------------------------------------------
    # 2. CBC (Cipher Block Chaining)
    # -------------------------------------------------------------
    # Requires 16-byte random IV
    # Requires PKCS#7 padding
    padded_pt_cbc = pad(pt_bytes, AES.block_size, style='pkcs7')
    cipher_cbc = AES.new(key, AES.MODE_CBC, iv=iv_16)
    ct_cbc = cipher_cbc.encrypt(padded_pt_cbc)
    
    dec_cipher_cbc = AES.new(key, AES.MODE_CBC, iv=iv_16)
    decrypted_cbc = unpad(dec_cipher_cbc.decrypt(ct_cbc), AES.block_size, style='pkcs7').decode('utf-8', errors='replace')
    
    results['CBC'] = {
        'mode_name': 'CBC - Cipher Block Chaining',
        'short_name': 'CBC',
        'ciphertext_hex': ct_cbc.hex(),
        'ciphertext_formatted': " ".join(ct_cbc.hex()[i:i+2] for i in range(0, len(ct_cbc.hex()), 2)),
        'blocks': format_hex_blocks(ct_cbc, AES.block_size),
        'decrypted_plaintext': decrypted_cbc,
        'padding_requirement': 'Yes (PKCS#7 padding required before chaining XOR operations)',
        'padding_type': 'PKCS#7',
        'iv_nonce_requirement': 'IV (16-byte random, unpredictable Initialization Vector)',
        'iv_hex': iv_16.hex(),
        'security_observation': 'Hides plaintext patterns. Requires an unpredictable IV; encryption is sequential; does not provide authentication or integrity.',
        'pattern_hiding': 'Yes',
        'parallel_encryption': 'No (Sequential)'
    }
    
    # -------------------------------------------------------------
    # 3. CFB (Cipher Feedback)
    # -------------------------------------------------------------
    # Requires 16-byte random IV
    # Operates as stream cipher: No traditional padding needed
    cipher_cfb = AES.new(key, AES.MODE_CFB, iv=iv_16, segment_size=128)
    ct_cfb = cipher_cfb.encrypt(pt_bytes)
    
    dec_cipher_cfb = AES.new(key, AES.MODE_CFB, iv=iv_16, segment_size=128)
    decrypted_cfb = dec_cipher_cfb.decrypt(ct_cfb).decode('utf-8', errors='replace')
    
    results['CFB'] = {
        'mode_name': 'CFB - Cipher Feedback',
        'short_name': 'CFB',
        'ciphertext_hex': ct_cfb.hex(),
        'ciphertext_formatted': " ".join(ct_cfb.hex()[i:i+2] for i in range(0, len(ct_cfb.hex()), 2)),
        'blocks': format_hex_blocks(ct_cfb, AES.block_size),
        'decrypted_plaintext': decrypted_cfb,
        'padding_requirement': 'No traditional padding (Acts as a stream cipher, ciphertexts match plaintext length exactly)',
        'padding_type': 'None',
        'iv_nonce_requirement': 'IV (16-byte Initialization Vector)',
        'iv_hex': iv_16.hex(),
        'security_observation': 'Hides plaintext patterns. Requires an IV; encryption is sequential; does not provide authentication.',
        'pattern_hiding': 'Yes',
        'parallel_encryption': 'No (Sequential)'
    }
    
    # -------------------------------------------------------------
    # 4. OFB (Output Feedback)
    # -------------------------------------------------------------
    # Requires 16-byte random IV
    # Generates independent keystream: No traditional padding needed
    cipher_ofb = AES.new(key, AES.MODE_OFB, iv=iv_16)
    ct_ofb = cipher_ofb.encrypt(pt_bytes)
    
    dec_cipher_ofb = AES.new(key, AES.MODE_OFB, iv=iv_16)
    decrypted_ofb = dec_cipher_ofb.decrypt(ct_ofb).decode('utf-8', errors='replace')
    
    results['OFB'] = {
        'mode_name': 'OFB - Output Feedback',
        'short_name': 'OFB',
        'ciphertext_hex': ct_ofb.hex(),
        'ciphertext_formatted': " ".join(ct_ofb.hex()[i:i+2] for i in range(0, len(ct_ofb.hex()), 2)),
        'blocks': format_hex_blocks(ct_ofb, AES.block_size),
        'decrypted_plaintext': decrypted_ofb,
        'padding_requirement': 'No traditional padding (Keystream is generated iteratively and XORed directly with plaintext)',
        'padding_type': 'None',
        'iv_nonce_requirement': 'Unique IV (Requires unique 16-byte Initialization Vector)',
        'iv_hex': iv_16.hex(),
        'security_observation': 'Hides plaintext patterns. Requires a unique IV (never reuse); encryption is sequential; does not provide authentication.',
        'pattern_hiding': 'Yes',
        'parallel_encryption': 'No (Sequential)'
    }
    
    # -------------------------------------------------------------
    # 5. CTR (Counter Mode)
    # -------------------------------------------------------------
    # Requires secure Nonce
    # No padding needed
    cipher_ctr = AES.new(key, AES.MODE_CTR, nonce=nonce_8)
    ct_ctr = cipher_ctr.encrypt(pt_bytes)
    
    dec_cipher_ctr = AES.new(key, AES.MODE_CTR, nonce=nonce_8)
    decrypted_ctr = dec_cipher_ctr.decrypt(ct_ctr).decode('utf-8', errors='replace')
    
    results['CTR'] = {
        'mode_name': 'CTR - Counter Mode',
        'short_name': 'CTR',
        'ciphertext_hex': ct_ctr.hex(),
        'ciphertext_formatted': " ".join(ct_ctr.hex()[i:i+2] for i in range(0, len(ct_ctr.hex()), 2)),
        'blocks': format_hex_blocks(ct_ctr, AES.block_size),
        'decrypted_plaintext': decrypted_ctr,
        'padding_requirement': 'No (Stream cipher mode; encrypted counter blocks are XORed directly with plaintext bytes)',
        'padding_type': 'None',
        'iv_nonce_requirement': 'Unique Nonce/counter (Secure random nonce ensuring unique counter inputs)',
        'iv_hex': nonce_8.hex(),
        'security_observation': 'Hides plaintext patterns. Requires a unique nonce/counter; no padding; supports parallel encryption, random access, and efficient processing. The same nonce/counter must never be reused with the same key.',
        'pattern_hiding': 'Yes',
        'parallel_encryption': 'Yes (Parallelizable)'
    }
    
    return {
        'plaintext': plaintext,
        'plaintext_length_bytes': len(pt_bytes),
        'key_hex': key.hex(),
        'shared_iv_hex': iv_16.hex(),
        'shared_nonce_hex': nonce_8.hex(),
        'results': results
    }


def demonstrate_ecb_pattern(repeated_text: str, key_str: str) -> dict:
    """
    Demonstrates ECB pattern leakage on repeated 16-byte blocks.
    Compares ECB against CBC with the same key.
    """
    key = validate_key(key_str)
    pt_bytes = repeated_text.encode('utf-8')
    
    # 1. Plaintext blocks breakdown
    pt_blocks = format_hex_blocks(pt_bytes, AES.block_size)
    
    # 2. ECB Encryption with PKCS#7
    padded_ecb = pad(pt_bytes, AES.block_size, style='pkcs7')
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    ct_ecb = cipher_ecb.encrypt(padded_ecb)
    ecb_blocks = format_hex_blocks(ct_ecb, AES.block_size)
    
    # Mark identical blocks in ECB
    # Find matching hexes among blocks
    hex_counts = {}
    for blk in ecb_blocks:
        hex_counts[blk['hex']] = hex_counts.get(blk['hex'], 0) + 1
    
    for blk in ecb_blocks:
        blk['is_duplicate'] = (hex_counts[blk['hex']] > 1)
        blk['duplicate_count'] = hex_counts[blk['hex']]
        start = (blk['index'] - 1) * 16
        blk['pt_slice'] = repeated_text[start:start+16] if start < len(repeated_text) else '(PKCS#7 Padding Block)'
    
    # 3. CBC Encryption with PKCS#7 for contrast
    iv_cbc = get_random_bytes(16)
    padded_cbc = pad(pt_bytes, AES.block_size, style='pkcs7')
    cipher_cbc = AES.new(key, AES.MODE_CBC, iv=iv_cbc)
    ct_cbc = cipher_cbc.encrypt(padded_cbc)
    cbc_blocks = format_hex_blocks(ct_cbc, AES.block_size)
    
    for blk in cbc_blocks:
        blk['is_duplicate'] = False
        blk['duplicate_count'] = 1
        start = (blk['index'] - 1) * 16
        blk['pt_slice'] = repeated_text[start:start+16] if start < len(repeated_text) else '(PKCS#7 Padding Block)'

    # Check if ECB actually leaked patterns
    duplicates_found = any(blk['is_duplicate'] for blk in ecb_blocks)
    
    return {
        'plaintext': repeated_text,
        'key_hex': key.hex(),
        'cbc_iv_hex': iv_cbc.hex(),
        'duplicates_found': duplicates_found,
        'plaintext_blocks': pt_blocks,
        'ecb_blocks': ecb_blocks,
        'cbc_blocks': cbc_blocks,
        'ecb_ciphertext_hex': ct_ecb.hex(),
        'cbc_ciphertext_hex': ct_cbc.hex(),
        'explanation': (
            "Because ECB operates on each 16-byte block independently with no chaining or IV, "
            "any identical plaintext block results in an IDENTICAL ciphertext block. "
            "In CBC mode, the preceding ciphertext block is XORed with the next plaintext block, "
            "guaranteeing completely different ciphertext blocks even if the plaintext is 100% repetitive."
        )
    }
