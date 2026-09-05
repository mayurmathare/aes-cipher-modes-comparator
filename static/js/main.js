/**
 * main.js
 * Interactive logic for AES Block Cipher Modes Comparison
 */

document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const ptInput = document.getElementById('plaintext-input');
    const ptByteCount = document.getElementById('pt-byte-count');
    const keyInput = document.getElementById('key-input');
    const keyByteCount = document.getElementById('key-byte-count');
    const btnCompare = document.getElementById('btn-compare');
    const btnRandKey = document.getElementById('btn-rand-key');
    const modesGrid = document.getElementById('modes-grid');
    const loadingState = document.getElementById('loading-state');
    const sharedParamsPreview = document.getElementById('shared-params-preview');
    const previewIv = document.getElementById('preview-iv');
    const previewNonce = document.getElementById('preview-nonce');

    // ECB Demo elements
    const ecbDemoInput = document.getElementById('ecb-demo-input');
    const btnRunEcbDemo = document.getElementById('btn-run-ecb-demo');
    const demoResults = document.getElementById('demo-results');

    // Helper: Byte size calculation for UTF-8 string
    function getByteLength(str) {
        return new TextEncoder().encode(str).length;
    }

    // Update byte counters
    function updateCounters() {
        const ptBytes = getByteLength(ptInput.value);
        ptByteCount.textContent = `${ptBytes} byte${ptBytes !== 1 ? 's' : ''}`;

        const keyBytes = getByteLength(keyInput.value);
        if (keyBytes === 16 || keyBytes === 24 || keyBytes === 32) {
            keyByteCount.textContent = `${keyBytes} bytes (Valid AES-${keyBytes * 8})`;
            keyByteCount.style.color = '#059669';
        } else {
            keyByteCount.textContent = `${keyBytes} bytes (Must be 16, 24, or 32)`;
            keyByteCount.style.color = '#dc2626';
        }
    }

    ptInput.addEventListener('input', updateCounters);
    keyInput.addEventListener('input', updateCounters);
    updateCounters();

    // Preset buttons for Plaintext
    document.querySelectorAll('.btn-preset').forEach(btn => {
        btn.addEventListener('click', () => {
            ptInput.value = btn.getAttribute('data-text');
            updateCounters();
            runComparison();
        });
    });

    // Preset buttons for ECB Demo
    document.querySelectorAll('.btn-preset-demo').forEach(btn => {
        btn.addEventListener('click', () => {
            ecbDemoInput.value = btn.getAttribute('data-text');
            runEcbDemo();
        });
    });

    // Generate random 16-character alphanumeric key
    btnRandKey.addEventListener('click', () => {
        const chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let randKey = '';
        for (let i = 0; i < 16; i++) {
            randKey += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        keyInput.value = randKey;
        updateCounters();
        runComparison();
    });

    // Copy to clipboard helper
    window.copyText = function(text, element) {
        navigator.clipboard.writeText(text).then(() => {
            const originalHtml = element.innerHTML;
            element.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
            element.style.color = '#059669';
            setTimeout(() => {
                element.innerHTML = originalHtml;
                element.style.color = '';
            }, 1600);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    };

    // Render Mode Card
    function renderModeCard(modeKey, modeData) {
        const isEcb = (modeKey === 'ECB');
        const bannerClass = isEcb ? 'banner-ecb' : 'banner-safe';
        const bannerIcon = isEcb ? 'fa-triangle-exclamation' : 'fa-shield';

        const ivDisplayHtml = modeData.iv_hex 
            ? `<code>${modeData.iv_hex}</code>` 
            : `<span class="tag-pill">None (Not Used)</span>`;

        // Blocks HTML
        let blocksHtml = '';
        if (modeData.blocks && modeData.blocks.length > 0) {
            blocksHtml = modeData.blocks.map(b => `
                <div class="block-row">
                    <span class="block-tag">Block ${b.index}</span>
                    <span class="block-hex">${b.formatted_hex}</span>
                    <span class="block-ascii">ASCII: "${b.ascii_preview}"</span>
                </div>
            `).join('');
        }

        return `
            <div class="mode-card" id="card-${modeKey.toLowerCase()}">
                <div class="mode-card-header">
                    <div class="mode-badge-title">
                        <span class="mode-code">${modeData.short_name}</span>
                        <span class="mode-full-name">${modeData.mode_name}</span>
                    </div>
                    <div>
                        <span class="tag-pill"><i class="fa-solid fa-bolt"></i> Parallel: ${modeData.parallel_encryption}</span>
                    </div>
                </div>

                <div class="mode-card-body">
                    <!-- Ciphertext Output -->
                    <div class="output-box">
                        <div class="output-header">
                            <span class="output-label">
                                <i class="fa-solid fa-lock"></i> Ciphertext (Hexadecimal)
                            </span>
                            <button type="button" class="btn-copy" onclick="copyText('${modeData.ciphertext_hex}', this)">
                                <i class="fa-regular fa-copy"></i> Copy Hex
                            </button>
                        </div>
                        <div class="cipher-hex-display">${modeData.ciphertext_formatted}</div>
                    </div>

                    <!-- Decrypted Plaintext Confirmation -->
                    <div class="decrypted-badge-row">
                        <strong><i class="fa-solid fa-unlock-keyhole"></i> Decrypted Plaintext:</strong>
                        <span class="decrypted-text">"${escapeHtml(modeData.decrypted_plaintext)}"</span>
                        <span class="badge badge-success"><i class="fa-solid fa-circle-check"></i> Verified Match</span>
                    </div>

                    <!-- Details Grid: Padding & IV -->
                    <div class="mode-details-grid">
                        <div class="detail-item">
                            <div class="detail-title">
                                <i class="fa-solid fa-layer-group"></i> Padding Requirement
                            </div>
                            <div class="detail-content">
                                ${modeData.padding_requirement}
                            </div>
                        </div>

                        <div class="detail-item">
                            <div class="detail-title">
                                <i class="fa-solid fa-dice-d20"></i> IV / Nonce Requirement
                            </div>
                            <div class="detail-content">
                                <div>${modeData.iv_nonce_requirement}</div>
                                <div style="margin-top: 4px;"><strong>Value:</strong> ${ivDisplayHtml}</div>
                            </div>
                        </div>
                    </div>

                    <!-- 16-Byte Block Inspector -->
                    <details class="block-visualizer">
                        <summary><i class="fa-solid fa-diagram-project"></i> Inspect 16-Byte Block Segments (${modeData.blocks.length} block${modeData.blocks.length !== 1 ? 's' : ''})</summary>
                        <div class="blocks-container">
                            ${blocksHtml}
                        </div>
                    </details>

                    <!-- Security Observation Banner -->
                    <div class="security-observation-banner ${bannerClass}">
                        <i class="fa-solid ${bannerIcon}"></i>
                        <div>
                            <div class="obs-title">Security Observation:</div>
                            <div class="obs-text">${modeData.security_observation}</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Escape HTML string
    function escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Execute Main Comparison
    async function runComparison() {
        const plaintext = ptInput.value;
        const key = keyInput.value;

        if (!plaintext) {
            alert('Please enter a plaintext message.');
            return;
        }

        if (!key) {
            alert('Please enter an AES key.');
            return;
        }

        btnCompare.disabled = true;
        loadingState.style.display = 'flex';
        modesGrid.innerHTML = '';

        try {
            const response = await fetch('/api/compare', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plaintext, key })
            });

            const resData = await response.json();

            if (!response.ok || !resData.success) {
                throw new Error(resData.error || 'Failed to compare modes');
            }

            const data = resData.data;

            // Update shared IV / Nonce preview
            previewIv.textContent = data.shared_iv_hex;
            previewNonce.textContent = data.shared_nonce_hex;
            sharedParamsPreview.style.display = 'flex';

            // Order of modes as specified: ECB, CBC, CFB, OFB, CTR
            const modeOrder = ['ECB', 'CBC', 'CFB', 'OFB', 'CTR'];
            let html = '';
            modeOrder.forEach(mKey => {
                if (data.results[mKey]) {
                    html += renderModeCard(mKey, data.results[mKey]);
                }
            });

            modesGrid.innerHTML = html;

        } catch (error) {
            modesGrid.innerHTML = `
                <div class="security-observation-banner banner-ecb" style="grid-column: 1 / -1;">
                    <i class="fa-solid fa-circle-exclamation"></i>
                    <div>
                        <div class="obs-title">Error Executing Ciphers:</div>
                        <div class="obs-text">${escapeHtml(error.message)}</div>
                    </div>
                </div>
            `;
        } finally {
            btnCompare.disabled = false;
            loadingState.style.display = 'none';
        }
    }

    // Execute ECB Pattern Demo (Requirement 15)
    async function runEcbDemo() {
        const repeatedText = ecbDemoInput.value;
        const key = keyInput.value;

        if (!repeatedText) {
            alert('Please enter repeated plaintext to test.');
            return;
        }

        btnRunEcbDemo.disabled = true;
        btnRunEcbDemo.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Testing...';

        try {
            const response = await fetch('/api/ecb-demo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repeated_text: repeatedText, key })
            });

            const resData = await response.json();
            if (!response.ok || !resData.success) {
                throw new Error(resData.error || 'Failed to execute pattern demo');
            }

            const data = resData.data;

            // Render ECB vs CBC columns
            let ecbCardsHtml = '';
            data.ecb_blocks.forEach(b => {
                const matchClass = b.is_duplicate ? 'match-highlight' : '';
                const badge = b.is_duplicate 
                    ? `<span class="match-badge"><i class="fa-solid fa-triangle-exclamation"></i> IDENTICAL CIPHERTEXT BLOCK</span>` 
                    : `<span class="unique-badge"><i class="fa-solid fa-check"></i> Unique Block</span>`;
                ecbCardsHtml += `
                    <div class="block-demo-chip ${matchClass}">
                        <div class="block-chip-head">
                            <span class="block-chip-num">Block ${b.index} (${b.byte_count} bytes)</span>
                            ${badge}
                        </div>
                        <div class="block-chip-hex">${b.formatted_hex}</div>
                        <div class="block-ascii">Plaintext ASCII: "${escapeHtml(b.ascii_preview)}"</div>
                    </div>
                `;
            });

            let cbcCardsHtml = '';
            data.cbc_blocks.forEach(b => {
                cbcCardsHtml += `
                    <div class="block-demo-chip unique-highlight">
                        <div class="block-chip-head">
                            <span class="block-chip-num">Block ${b.index} (${b.byte_count} bytes)</span>
                            <span class="unique-badge"><i class="fa-solid fa-shield-halved"></i> Pattern Hidden</span>
                        </div>
                        <div class="block-chip-hex">${b.formatted_hex}</div>
                        <div class="block-ascii">Plaintext ASCII: "${escapeHtml(b.ascii_preview)}"</div>
                    </div>
                `;
            });

            const alertHtml = data.duplicates_found
                ? `
                <div class="demo-alert-banner demo-alert-danger">
                    <i class="fa-solid fa-triangle-exclamation"></i>
                    <div>
                        <strong>Vulnerability Confirmed: Pattern Leakage in ECB Mode!</strong><br>
                        Repeated identical 16-byte plaintext blocks produced <strong>100% IDENTICAL</strong> ciphertext blocks highlighted in red below!
                        An adversary observing this ciphertext learns the pattern without knowing the AES key.
                        Notice that CBC with an IV completely diffuses the repeated text into randomized blocks.
                    </div>
                </div>
                `
                : `
                <div class="demo-alert-banner" style="background: #f0fdf4; border: 2px solid #10b981; color: #166534;">
                    <i class="fa-solid fa-circle-info" style="color: #10b981; font-size: 24px;"></i>
                    <div>
                        <strong>Input blocks are unique.</strong> To see ECB duplicate pattern leakage, enter at least two identical 16-byte blocks (e.g. 32 consecutive 'A's).
                    </div>
                </div>
                `;

            demoResults.innerHTML = `
                <div class="demo-results-wrapper">
                    ${alertHtml}

                    <div class="demo-comparison-columns">
                        <!-- ECB Column -->
                        <div class="demo-column-card ecb-col">
                            <div class="demo-col-header">
                                <h4><i class="fa-solid fa-xmark" style="color: var(--danger);"></i> ECB Mode (No Chaining)</h4>
                                <span class="tag-pill" style="color: var(--danger); font-weight: 700;">Leaking Patterns</span>
                            </div>
                            <p style="font-size: 0.84rem; color: #64748b;">
                                Formula: <code>C<sub>i</sub> = E<sub>K</sub>(P<sub>i</sub>)</code>. Every block encrypted with key in total isolation.
                            </p>
                            <div style="display: flex; flex-direction: column; gap: 10px;">
                                ${ecbCardsHtml}
                            </div>
                        </div>

                        <!-- CBC Column -->
                        <div class="demo-column-card cbc-col">
                            <div class="demo-col-header">
                                <h4><i class="fa-solid fa-check" style="color: var(--success);"></i> CBC Mode (With Chaining & IV)</h4>
                                <span class="tag-pill" style="color: var(--success); font-weight: 700;">Hiding Patterns</span>
                            </div>
                            <p style="font-size: 0.84rem; color: #64748b;">
                                Formula: <code>C<sub>i</sub> = E<sub>K</sub>(P<sub>i</sub> ⊕ C<sub>i-1</sub>)</code>. IV: <code>${data.cbc_iv_hex.substring(0, 16)}...</code>
                            </p>
                            <div style="display: flex; flex-direction: column; gap: 10px;">
                                ${cbcCardsHtml}
                            </div>
                        </div>
                    </div>
                </div>
            `;

        } catch (err) {
            demoResults.innerHTML = `
                <div class="security-observation-banner banner-ecb">
                    <i class="fa-solid fa-circle-exclamation"></i>
                    <div>
                        <div class="obs-title">Error running pattern test:</div>
                        <div class="obs-text">${escapeHtml(err.message)}</div>
                    </div>
                </div>
            `;
        } finally {
            btnRunEcbDemo.disabled = false;
            btnRunEcbDemo.innerHTML = '<i class="fa-solid fa-flask-vial"></i> Test Pattern Leakage';
        }
    }

    // Attach button listeners
    btnCompare.addEventListener('click', runComparison);
    btnRunEcbDemo.addEventListener('click', runEcbDemo);

    // Initial runs with defaults
    runComparison();
    runEcbDemo();
});
