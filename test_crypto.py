"""
test_crypto.py
Automated test suite verifying the cryptographic requirements:
1. All 5 modes (ECB, CBC, CFB, OFB, CTR) encrypt and cleanly decrypt back.
2. Padding rules: PKCS#7 for ECB/CBC; stream-like (no traditional padding) for CFB/OFB/CTR.
3. IV/Nonce generation: 16-byte random IV for CBC, CFB, OFB; random nonce for CTR; none for ECB.
4. ECB Pattern leakage verification: identical 16-byte plaintext blocks produce identical ciphertext blocks in ECB, but unique blocks in CBC.
"""

from crypto_engine import compare_all_modes, demonstrate_ecb_pattern, validate_key
import binascii

def run_tests():
    print(">>> Starting Cryptographic Test Suite...")

    # Test 1: Key Validation
    print("Testing Key Validation...")
    valid_key = "0123456789abcdef" # 16 bytes
    k_bytes = validate_key(valid_key)
    assert len(k_bytes) == 16, "Key bytes length must be 16"

    try:
        validate_key("short_key")
        assert False, "Should have raised ValueError for invalid key length"
    except ValueError:
        pass
    print("  [PASSED] Key validation functions correctly.")

    # Test 2: Standard Plaintext Comparison across all 5 modes
    print("Testing Compare All Modes (ECB, CBC, CFB, OFB, CTR)...")
    plaintext = "HELLO HELLO HELLO HELLO"
    res = compare_all_modes(plaintext, valid_key)

    assert 'ECB' in res['results']
    assert 'CBC' in res['results']
    assert 'CFB' in res['results']
    assert 'OFB' in res['results']
    assert 'CTR' in res['results']

    # Check decryption integrity for all modes
    for mode in ['ECB', 'CBC', 'CFB', 'OFB', 'CTR']:
        dec = res['results'][mode]['decrypted_plaintext']
        assert dec == plaintext, f"Decryption mismatch for mode {mode}: got {dec} instead of {plaintext}"
        assert len(res['results'][mode]['ciphertext_hex']) > 0, f"Ciphertext empty for {mode}"
        print(f"  [PASSED] {mode}: Encryption + Decryption verified identical.")

    # Check IV & Nonce specifications
    assert res['results']['ECB']['iv_hex'] is None, "ECB must not have an IV"
    assert res['results']['CBC']['iv_hex'] is not None and len(res['results']['CBC']['iv_hex']) == 32, "CBC must have 16-byte (32 hex char) IV"
    assert res['results']['CFB']['iv_hex'] is not None and len(res['results']['CFB']['iv_hex']) == 32, "CFB must have 16-byte (32 hex char) IV"
    assert res['results']['OFB']['iv_hex'] is not None and len(res['results']['OFB']['iv_hex']) == 32, "OFB must have 16-byte (32 hex char) IV"
    assert res['results']['CTR']['iv_hex'] is not None, "CTR must have Nonce"

    print("  [PASSED] IV / Nonce assignment conforms to requirements.")

    # Test 3: Stream Cipher Lengths (CFB, OFB, CTR)
    # Plaintext length: 7 bytes. CFB, OFB, CTR ciphertext must be exactly 7 bytes (14 hex chars)
    short_pt = "TEST123"
    short_res = compare_all_modes(short_pt, valid_key)
    for m in ['CFB', 'OFB', 'CTR']:
        ct_bytes_len = len(bytes.fromhex(short_res['results'][m]['ciphertext_hex']))
        assert ct_bytes_len == len(short_pt.encode('utf-8')), f"{m} should not pad: expected {len(short_pt)} bytes, got {ct_bytes_len}"
    print("  [PASSED] Stream modes (CFB, OFB, CTR) preserve exact byte lengths with no traditional padding.")

    # Test 4: ECB Pattern Demonstration (Requirement 15)
    print("Testing ECB Pattern Leakage Demonstration...")
    repeated_32 = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" # 32 'A's: two identical 16-byte blocks
    demo_res = demonstrate_ecb_pattern(repeated_32, valid_key)

    assert demo_res['duplicates_found'] is True, "ECB demo must detect duplicates for 32 A's"
    ecb_b1 = demo_res['ecb_blocks'][0]['hex']
    ecb_b2 = demo_res['ecb_blocks'][1]['hex']
    assert ecb_b1 == ecb_b2, f"ECB repeated blocks must produce identical ciphertext blocks! Got B1={ecb_b1}, B2={ecb_b2}"

    cbc_b1 = demo_res['cbc_blocks'][0]['hex']
    cbc_b2 = demo_res['cbc_blocks'][1]['hex']
    assert cbc_b1 != cbc_b2, f"CBC repeated blocks must produce different ciphertext blocks! Got B1={cbc_b1}, B2={cbc_b2}"

    print(f"  [PASSED] ECB duplicate confirmed: Block 1 ({ecb_b1}) == Block 2 ({ecb_b2})")
    print(f"  [PASSED] CBC uniqueness confirmed: Block 1 ({cbc_b1}) != Block 2 ({cbc_b2})")

    print("\n>>> ALL CRYPTOGRAPHIC TESTS COMPLETED SUCCESSFULLY! <<<")

if __name__ == '__main__':
    run_tests()
