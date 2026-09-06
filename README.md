# Comparison of Block Cipher Modes of Operation
### Cryptography Practical / TAE Web Application Simulator

[![Deploy to GitHub Pages](https://github.com/mayurmathare/aes-cipher-modes-comparator/actions/workflows/deploy.yml/badge.svg)](https://github.com/mayurmathare/aes-cipher-modes-comparator/actions/workflows/deploy.yml)

🌐 **Live Interactive Web Simulator**: [https://mayurmathare.github.io/aes-cipher-modes-comparator/](https://mayurmathare.github.io/aes-cipher-modes-comparator/)

An interactive, educational web application designed to demonstrate, analyze, and compare the five NIST standard AES block cipher modes of operation:
1. **ECB (Electronic Codebook)**
2. **CBC (Cipher Block Chaining)**
3. **CFB (Cipher Feedback)**
4. **OFB (Output Feedback)**
5. **CTR (Counter Mode)**

---

## 🚀 Key Features

- **Side-by-Side Mode Comparison**: Encrypts a common plaintext with the exact same 128-bit AES key across all five modes simultaneously.
- **Dual Deployment Architecture**:
  - **Local Python Server**: Runs Flask + PyCryptodome for native server-side cryptographic execution.
  - **Live GitHub Pages Deployment**: Fully functional static deployment executing in-browser AES operations with zero server setup required.
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
├── .github/
│   └── workflows/
│       └── deploy.yml      # Automated GitHub Actions workflow for GitHub Pages
├── index.html              # Static entry point for GitHub Pages (live online simulator)
├── app.py                  # Flask server & REST API routes (/api/compare, /api/ecb-demo)
├── crypto_engine.py        # Core AES crypto implementation via PyCryptodome
├── test_crypto.py          # Automated verification test suite
├── requirements.txt        # Dependencies: Flask, pycryptodome
├── deploy_to_github.bat    # 1-Click push & deploy to GitHub
├── run.bat                 # 1-Click local Windows runner
├── templates/
│   └── index.html          # Jinja2 template for Flask local server
└── static/
    ├── css/
    │   └── style.css       # Academic styling, color badges, block cards
    └── js/
        └── main.js         # Reactive UI, byte counters, async API calls, block visualizer
```

---

## 🌐 Deploying to GitHub & GitHub Pages

### 1. Push to GitHub
Run [`deploy_to_github.bat`](file:///C:/Users/MAYUR/.gemini/antigravity/scratch/aes-cipher-modes-comparator/deploy_to_github.bat) or execute:
```powershell
cd "C:\Users\MAYUR\.gemini\antigravity\scratch\aes-cipher-modes-comparator"
git add .
git commit -m "Deploy AES Block Cipher Modes Comparison to GitHub Pages"
git push -u origin main
```

### 2. Enable GitHub Pages (One-Time Setup)
1. Go to your repository settings:
   `https://github.com/mayurmathare/aes-cipher-modes-comparator/settings/pages`
2. Under **Build and deployment** > **Source**:
   - Select **GitHub Actions** (recommended, deploys automatically via `.github/workflows/deploy.yml`).
   - *Or* select **Deploy from a branch** > branch **`main`** > folder **`/ (root)`** and click **Save**.
3. Within 1-2 minutes, your website will be live at:
   **`https://mayurmathare.github.io/aes-cipher-modes-comparator/`**

---

## ⚙️ Running Locally with Python & Flask

Double-click [`run.bat`](file:///C:/Users/MAYUR/.gemini/antigravity/scratch/aes-cipher-modes-comparator/run.bat) or run:
```powershell
pip install -r requirements.txt
python app.py
```
Open your browser at: `http://127.0.0.1:5000`