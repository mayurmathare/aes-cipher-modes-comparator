# Comparison of Block Cipher Modes of Operation
### Cryptography Practical / TAE Web Application Simulator

An interactive, educational web application designed to demonstrate, analyze, and compare the five NIST standard AES block cipher modes of operation:
1. **ECB (Electronic Codebook)**
2. **CBC (Cipher Block Chaining)**
3. **CFB (Cipher Feedback)**
4. **OFB (Output Feedback)**
5. **CTR (Counter Mode)**

---

## 🚀 Key Features

- **Side-by-Side Mode Comparison**: Encrypts a common plaintext with the exact same 128-bit AES key across all five modes simultaneously.
- **Cryptographic Parameter Management**:
  - Secure random 16-byte IV generated for **CBC**, **CFB**, and **OFB**.
  - Secure random Nonce generated for **CTR**.
  - Explicit omission of IV/Nonce for **ECB** conforming to standard specifications.
- **Strict Padding Adherence**:
  - **PKCS#7 Padding** applied to ECB and CBC.
  - **Zero Traditional Padding** for stream-style modes CFB, OFB, and CTR (arbitrary byte length support).
- **Dual-Verification Display**: Displays ciphertext in formatted hexadecimal alongside the decrypted plaintext to verify round-trip integrity.
- **16-Byte Block Inspector**: Breaks down any ciphertext into its constituent 16-byte (128-bit) blocks with formatted hex and ASCII character maps.
- **Standardized Comparative Matrix**: Evaluates pattern hiding, padding, IV requirements, parallelizability, and security concerns.
- **Interactive ECB Pattern Leakage Lab**: Directly proves that identical 16-byte plaintext blocks (e.g. `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA`) yield 100% identical ciphertext blocks in ECB, while CBC randomizes them completely.

---

## 📊 Standard Comparative Matrix

| Mode | Pattern Hiding | Padding | IV / Nonce | Parallel Encryption | Security Concern |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **ECB** | **No** | **Yes** (PKCS#7) | None | **Yes** | Identical plaintext blocks produce identical ciphertext blocks. |
| **CBC** | **Yes** | **Yes** (PKCS#7) | IV | **No** for encryption | IV must be unpredictable; CBC alone does not provide authentication. |
| **CFB** | **Yes** | **No traditional padding** | IV | **No** | IV reuse must be avoided. |
| **OFB** | **Yes** | **No traditional padding** | IV | **No** | IV reuse must be avoided. |
| **CTR** | **Yes** | **No** | Nonce/counter | **Yes** | Never reuse the same nonce/counter with the same key. |

---

## 📂 Project Architecture

```
aes-cipher-modes-comparator/
├── app.py                  # Flask server & REST API routes (/api/compare, /api/ecb-demo)
├── crypto_engine.py        # Core AES crypto implementation via PyCryptodome
├── test_crypto.py          # Automated verification test suite
├── requirements.txt        # Dependencies: Flask, pycryptodome
├── run.bat                 # One-click Windows runner
├── templates/
│   └── index.html          # Semantic HTML5 frontend layout & comparison table
└── static/
    ├── css/
    │   └── style.css       # Academic styling, color badges, block cards
    └── js/
        └── main.js         # Reactive UI, byte counters, async API calls, block visualizer
```

---

## ⚙️ Installation & Running

### Option 1: Quick Launch (Windows)
Double-click `run.bat`. It will:
1. Automatically install dependencies from `requirements.txt`.
2. Run the automated cryptographic test suite (`test_crypto.py`).
3. Launch the web server at `http://127.0.0.1:5000`.

### Option 2: Manual Terminal Execution
1. Open PowerShell or Command Prompt in this folder:
   ```bash
   cd "C:\Users\MAYUR\.gemini\antigravity\scratch\aes-cipher-modes-comparator"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run verification tests:
   ```bash
   python test_crypto.py
   ```

4. Start the Flask application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 🔬 Practical / TAE Observations

1. **Why ECB is Insecure**:
   Because ECB transforms each block independently ($C_i = E_K(P_i)$), two identical plaintext blocks will always encrypt to identical ciphertext blocks. This leaks structural data (notably shown by the famous ECB Penguin experiment).
2. **Why CBC Eliminates Patterns**:
   CBC XORs each plaintext block with the previous ciphertext block ($C_i = E_K(P_i \oplus C_{i-1})$) starting with an unpredictable IV. Even if 1,000 blocks are identical, each ciphertext block is dependent on the preceding block, rendering the output pseudorandom.
3. **Stream vs Block**:
   CFB, OFB, and CTR transform AES from a block cipher into a stream cipher. Plaintext is XORed with a keystream, eliminating the need to pad messages to 16-byte multiples.
