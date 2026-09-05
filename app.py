"""
app.py
Flask Application for AES Block Cipher Modes Comparison.
Interactive simulator comparing ECB, CBC, CFB, OFB, and CTR modes.
"""

import sys
import os
import subprocess
import threading
import webbrowser
import traceback

# Auto-install dependencies if missing in current environment
try:
    import flask
    from Crypto.Cipher import AES
except ImportError:
    print("=" * 70)
    print("[Setup] Missing required modules (Flask or PyCryptodome).")
    print("        Automatically installing now using pip...")
    print("=" * 70)
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "pycryptodome"])
        import flask
        from Crypto.Cipher import AES
        print("[Setup] Installation successful! Proceeding to launch application...")
    except Exception as err:
        print(f"[Error] Automatic installation failed: {err}")
        print("Please manually run: pip install flask pycryptodome")

from flask import Flask, render_template, request, jsonify
from crypto_engine import compare_all_modes, demonstrate_ecb_pattern

app = Flask(__name__, template_folder='templates', static_folder='static')

# Comparison table static matrix conforming strictly to project requirement 14
COMPARISON_MATRIX = [
    {
        "mode": "ECB",
        "full_name": "Electronic Codebook",
        "pattern_hiding": "No",
        "pattern_class": "badge-danger",
        "padding": "Yes",
        "iv_nonce": "None",
        "parallel_encryption": "Yes",
        "parallel_class": "badge-success",
        "security_concern": "Identical plaintext blocks produce identical ciphertext blocks."
    },
    {
        "mode": "CBC",
        "full_name": "Cipher Block Chaining",
        "pattern_hiding": "Yes",
        "pattern_class": "badge-success",
        "padding": "Yes",
        "iv_nonce": "IV",
        "parallel_encryption": "No for encryption",
        "parallel_class": "badge-warning",
        "security_concern": "IV must be unpredictable; CBC alone does not provide authentication."
    },
    {
        "mode": "CFB",
        "full_name": "Cipher Feedback",
        "pattern_hiding": "Yes",
        "pattern_class": "badge-success",
        "padding": "No traditional padding",
        "iv_nonce": "IV",
        "parallel_encryption": "No",
        "parallel_class": "badge-warning",
        "security_concern": "IV reuse must be avoided."
    },
    {
        "mode": "OFB",
        "full_name": "Output Feedback",
        "pattern_hiding": "Yes",
        "pattern_class": "badge-success",
        "padding": "No traditional padding",
        "iv_nonce": "IV",
        "parallel_encryption": "No",
        "parallel_class": "badge-warning",
        "security_concern": "IV reuse must be avoided."
    },
    {
        "mode": "CTR",
        "full_name": "Counter Mode",
        "pattern_hiding": "Yes",
        "pattern_class": "badge-success",
        "padding": "No",
        "iv_nonce": "Nonce/counter",
        "parallel_encryption": "Yes",
        "parallel_class": "badge-success",
        "security_concern": "Never reuse the same nonce/counter with the same key."
    }
]


@app.route('/')
def index():
    return render_template('index.html', comparison_matrix=COMPARISON_MATRIX)


@app.route('/api/compare', methods=['POST'])
def api_compare():
    try:
        data = request.get_json(force=True, silent=True) or {}
        plaintext = data.get('plaintext', 'HELLO HELLO HELLO HELLO')
        key = data.get('key', '0123456789abcdef')
        
        if not plaintext:
            return jsonify({'success': False, 'error': 'Plaintext cannot be empty.'}), 400
        
        if not key:
            return jsonify({'success': False, 'error': 'Key cannot be empty.'}), 400
        
        result = compare_all_modes(plaintext, key)
        return jsonify({'success': True, 'data': result})
    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': f"Internal server error: {str(e)}"}), 500


@app.route('/api/ecb-demo', methods=['POST'])
def api_ecb_demo():
    try:
        data = request.get_json(force=True, silent=True) or {}
        repeated_text = data.get('repeated_text', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        key = data.get('key', '0123456789abcdef')
        
        if not repeated_text:
            return jsonify({'success': False, 'error': 'Demonstration text cannot be empty.'}), 400
        
        result = demonstrate_ecb_pattern(repeated_text, key)
        return jsonify({'success': True, 'data': result})
    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': f"Internal server error: {str(e)}"}), 500


def open_browser_after_delay():
    threading.Timer(1.2, lambda: webbrowser.open("http://127.0.0.1:5000")).start()


if __name__ == '__main__':
    print("=" * 75)
    print(" AES Block Cipher Modes Comparison (Cryptography Practical / TAE)")
    print("=" * 75)
    print(" Starting Flask server...")
    print(" Local URL: http://127.0.0.1:5000")
    print(" Press Ctrl+C in this terminal window to stop the server.")
    print("=" * 75)

    # Open browser automatically if not in reloader child process
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        open_browser_after_delay()

    app.run(debug=True, host='127.0.0.1', port=5000)