import { useEffect, useRef, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { verifyOnChain, ETHERSCAN, short, friendlyError } from '../lib/chain.js';
import { api } from '../lib/api.js';
import { sha256Hex } from '../lib/pdf.js';
import { fmtDate, Hash } from '../components/ui.jsx';
import { useApp } from '../state.jsx';
import QrScannerModal from '../components/QrScannerModal.jsx';

const META = {
  valid: ['CERTIFICATE AUTHENTIC & VERIFIED', 'Cryptographically verified against the Ethereum Sepolia blockchain.', 'M6 21l10 10L36 11', 'ok'],
  revoked: ['CERTIFICATE HAS BEEN REVOKED', 'This credential was revoked by an authorized institutional issuer.', 'M21 8v16M21 33v.5', 'bad'],
  mismatch: ['DOCUMENT INTEGRITY TAMPERED / MISMATCH', 'The uploaded PDF SHA-256 digest does not match the immutable blockchain record.', 'M21 8v16M21 33v.5', 'warn'],
  notfound: ['CERTIFICATE NOT FOUND ON-CHAIN', 'No immutable blockchain record exists for this Certificate ID.', 'M10 10l22 22M32 10L10 32', 'bad'],
};

const LOG = [
  'Querying Ethereum Sepolia smart contract…',
  'Verifying certificate key and status…',
  'Calculating SHA-256 document fingerprint…',
  'Validating cryptographic integrity…',
  'Checking institutional authority signature…'
];

export default function Verify() {
  const { id: param } = useParams();
  const nav = useNavigate();
  const { toast } = useApp();
  const [id, setId] = useState(param || '');
  const [file, setFile] = useState(null);
  const [fileHash, setFileHash] = useState('');
  const [dragging, setDragging] = useState(false);
  const [phase, setPhase] = useState('form'); // form | load | res
  const [step, setStep] = useState(0);
  const [res, setRes] = useState(null);
  const [samples, setSamples] = useState([]);
  const [scannerOpen, setScannerOpen] = useState(false);
  const fileRef = useRef();

  useEffect(() => {
    api.samples().then((s) => setSamples(Array.isArray(s) ? s : [])).catch(() => setSamples([]));
  }, []);

  const handleFile = async (f) => {
    if (!f) return;
    setFile(f);
    try {
      const h = await sha256Hex(new Uint8Array(await f.arrayBuffer()));
      setFileHash(h);
      toast('✓ PDF analyzed: SHA-256 computed');
    } catch {
      toast('✕ Error reading PDF file');
    }
  };

  const run = async (certId = id, f = file) => {
    certId = certId.trim().toUpperCase();
    if (!certId) return toast('⚠ Please enter a Certificate ID');
    setPhase('load');
    setStep(0);
    const tick = setInterval(() => setStep((s) => Math.min(s + 1, LOG.length)), 450);

    try {
      const uploaded = f ? (fileHash || await sha256Hex(new Uint8Array(await f.arrayBuffer()))) : null;
      const [chain, meta] = await Promise.all([
        verifyOnChain(certId, uploaded),
        api.meta(certId).catch(() => null)
      ]);
      await new Promise((r) => setTimeout(r, 1600)); // Smooth UX sequence
      setRes({ certId, uploaded, chain, meta });
      setPhase('res');
    } catch (e) {
      setPhase('form');
      toast('✕ ' + friendlyError(e));
    } finally {
      clearInterval(tick);
    }
  };

  useEffect(() => {
    if (param) run(param, null);
    /* eslint-disable-next-line */
  }, [param]);

  const selectSample = (sId) => {
    setId(sId);
    run(sId, null);
  };

  const reset = () => {
    setPhase('form');
    setRes(null);
    setFile(null);
    setFileHash('');
    setId('');
    if (param) nav('/verify');
  };

  const status = res?.chain.status;
  const m = META[status];
  const rows = !res ? [] : status === 'notfound'
    ? [['Queried ID', res.certId], ['Blockchain Status', 'Not Found in Registry']]
    : status === 'mismatch'
    ? [
        ['Certificate ID', res.certId],
        ['Uploaded PDF Hash', res.uploaded, 1],
        ['Smart Contract Hash', res.chain.docHash, 1],
        ['Integrity Verdict', 'TAMPERED / MISMATCH DETECTED']
      ]
    : status === 'revoked'
    ? [
        ['Certificate ID', res.certId],
        ['Status', 'REVOKED ON-CHAIN'],
        ['Revocation Date', fmtDate(res.chain.revokedAt)],
        ['Revoked by', res.chain.revokedBy, 1],
        ['Revocation Tx', res.meta?.revokeTx, 2]
      ]
    : [
        ['Certificate ID', res.certId],
        res.meta && ['Recipient', res.meta.recipientName],
        res.meta && ['Program / Course', res.meta.course],
        res.meta?.achievement && ['Achievement', res.meta.achievement],
        ['Issue Timestamp', fmtDate(res.chain.issuedAt)],
        ['Authorized Issuer', res.chain.issuer, 1],
        ['Blockchain Network', 'Ethereum Sepolia Testnet'],
        ['Document SHA-256', res.chain.docHash, 1],
        ['File Integrity Check', res.uploaded ? '✓ CRYPTOGRAPHIC MATCH CONFIRMED' : 'Passively Verified (Upload PDF for byte-level comparison)'],
        res.meta?.issueTx && ['Issuance Transaction', res.meta.issueTx, 2]
      ].filter(Boolean);

  return (
    <main style={{ paddingTop: 130 }}>
      <section style={{ paddingTop: 0 }}>
        <div style={{ textAlign: 'center', marginBottom: 20 }}>
          <div className="eyebrow">Public Blockchain Verification</div>
          <h1 className="h2">Verify Academic<br />Credentials</h1>
          <p className="lead" style={{ margin: '0 auto 16px' }}>
            Instant mathematical proof of authenticity anchored on Ethereum Sepolia.
          </p>

          {/* Quick sample chips */}
          <div className="wrap" style={{ justifyContent: 'center', gap: 8 }}>
            <span style={{ fontSize: '.75rem', color: 'var(--muted)', alignSelf: 'center' }}>Test on-chain:</span>
            <button className="btn ghost sm" style={{ fontSize: '.75rem', padding: '0 12px' }} onClick={() => selectSample('CERT-2026-0001')}>
              ⚡ CERT-2026-0001 (Live Verified)
            </button>
            {(Array.isArray(samples) ? samples : []).filter(s => (s?.certId || s?.cert_id) !== 'CERT-2026-0001').slice(0, 2).map((s) => {
              const sId = s?.certId || s?.cert_id;
              return (
                <button key={sId} className="btn ghost sm" style={{ fontSize: '.75rem', padding: '0 12px' }} onClick={() => selectSample(sId)}>
                  ⚡ {sId}
                </button>
              );
            })}
            <button
              className="btn ghost sm"
              style={{ fontSize: '.75rem', padding: '0 12px', color: 'var(--cyan)', borderColor: 'rgba(51,214,255,.35)' }}
              onClick={() => setScannerOpen(true)}
            >
              📷 Scan QR Code
            </button>
          </div>
        </div>

        <div className="vwrap">
          <div className="ring" aria-hidden="true" />
          <div
            className="glass vcard"
            data-s={phase === 'res' ? (status === 'valid' ? 'ok' : status === 'mismatch' ? 'warn' : 'bad') : undefined}
            aria-live="polite"
          >
            {phase === 'form' && (
              <>
                <h2 className="vt">Certificate Verification</h2>

                <label className="field">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                    <span>Certificate ID</span>
                    <button
                      type="button"
                      className="btn ghost sm"
                      style={{ fontSize: '.74rem', padding: '2px 8px', color: 'var(--cyan)', borderColor: 'rgba(51,214,255,.3)' }}
                      onClick={() => setScannerOpen(true)}
                    >
                      📷 Scan to Verify
                    </button>
                  </div>
                  <input
                    className="input"
                    placeholder="e.g. CERT-2026-0001"
                    value={id}
                    onChange={(e) => setId(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && run()}
                  />
                </label>

                {/* Drag and Drop Zone */}
                <div
                  onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
                  onDragLeave={() => setDragging(false)}
                  onDrop={(e) => {
                    e.preventDefault();
                    setDragging(false);
                    const dropped = e.dataTransfer.files[0];
                    if (dropped && dropped.type === 'application/pdf') handleFile(dropped);
                    else toast('⚠ Please upload a PDF file');
                  }}
                  onClick={() => fileRef.current?.click()}
                  style={{
                    border: `2px dashed ${dragging ? 'var(--cyan)' : file ? 'var(--ok)' : 'rgba(185,180,255,.25)'}`,
                    borderRadius: 16,
                    padding: '24px 16px',
                    textAlign: 'center',
                    cursor: 'pointer',
                    background: dragging ? 'rgba(51,214,255,.08)' : file ? 'rgba(52,229,160,.05)' : 'rgba(5,5,17,.4)',
                    marginBottom: 20,
                    transition: '.3s'
                  }}
                >
                  <input
                    ref={fileRef}
                    type="file"
                    accept="application/pdf"
                    style={{ display: 'none' }}
                    onChange={(e) => handleFile(e.target.files[0] || null)}
                  />
                  <div style={{ fontSize: '1.8rem', marginBottom: 4 }}>{file ? '📄' : '📤'}</div>
                  <strong style={{ display: 'block', color: file ? 'var(--ok)' : 'var(--text)' }}>
                    {file ? file.name : 'Upload Certificate PDF (Optional Document Integrity Check)'}
                  </strong>
                  <small style={{ color: 'var(--muted)', fontSize: '.8rem' }}>
                    {file ? `SHA-256 computed: ${short(fileHash, 10, 8)}` : 'Drag and drop your PDF here, or click to browse'}
                  </small>
                </div>

                <div className="wrap" style={{ justifyContent: 'center', gap: 10 }}>
                  <button className="btn action" onClick={() => run()}>
                    Verify On-Chain →
                  </button>
                  <button
                    type="button"
                    className="btn ghost"
                    style={{ color: 'var(--cyan)', borderColor: 'rgba(51,214,255,.35)' }}
                    onClick={() => setScannerOpen(true)}
                  >
                    📷 Scan QR Code
                  </button>
                </div>
                <p className="or" style={{ fontSize: '.72rem' }}>
                  Zero personal data is stored on-chain • Immutable cryptography
                </p>
              </>
            )}

            {phase === 'load' && (
              <>
                <h2 className="vt">Verifying On-Chain</h2>
                <div className="nodes">
                  {LOG.map((_, i) => [
                    i ? <b key={'b' + i} className={i <= step ? 'on' : ''} /> : null,
                    <i key={i} className={i <= step ? 'on' : ''} />
                  ])}
                </div>
                <ul className="log">
                  {LOG.slice(0, step + 1).map((l, i) => (
                    <li key={l} className={i < step ? 'd' : ''}>{l}</li>
                  ))}
                  {step >= LOG.length && <li className="d">Cryptographic verification finished</li>}
                </ul>
              </>
            )}

            {phase === 'res' && (
              <>
                <div className={`rhead ${m[3]}-c`}>
                  <div className="badge" role="img" aria-label={m[0]}>
                    <svg viewBox="0 0 42 42"><path d={m[2]} /></svg>
                  </div>
                  <div className="rt">{m[0]}</div>
                  <div style={{ color: 'var(--muted)', fontSize: '.9rem', maxWidth: 460, margin: 'auto' }}>
                    {m[1]}
                  </div>
                </div>

                {/* Hash comparison highlight for mismatch or valid with upload */}
                {res.uploaded && (
                  <div style={{ background: status === 'valid' ? 'rgba(52,229,160,.08)' : 'rgba(255,107,107,.1)', border: `1px solid ${status === 'valid' ? 'var(--ok)' : 'var(--bad)'}`, borderRadius: 14, padding: '14px 16px', margin: '14px 0', fontSize: '.85rem' }}>
                    <div style={{ fontWeight: 600, color: status === 'valid' ? 'var(--ok)' : 'var(--bad)', marginBottom: 6 }}>
                      {status === 'valid' ? '✓ Cryptographic Document Match:' : '✕ Cryptographic Document Mismatch:'}
                    </div>
                    <div style={{ display: 'grid', gap: 4 }}>
                      <div><span style={{ color: 'var(--muted)' }}>Uploaded: </span><code className="hash">{res.uploaded}</code></div>
                      <div><span style={{ color: 'var(--muted)' }}>On-Chain: </span><code className="hash">{res.chain.docHash}</code></div>
                    </div>
                  </div>
                )}

                <div className="rows">
                  {rows.map(([k, v, h], i) => (
                    <div key={k} style={{ '--i': i }}>
                      <span>{k}</span>
                      <em>{h ? <Hash value={v} tx={h === 2} /> : v}</em>
                    </div>
                  ))}
                </div>

                <div className="wrap" style={{ justifyContent: 'center', marginTop: 24, gap: 10 }}>
                  {status === 'valid' && res.meta?.hasPdf && (
                    <a className="btn action" href={api.pdfUrl(res.certId)} target="_blank" rel="noreferrer">
                      Download Official PDF 📄
                    </a>
                  )}
                  {status === 'valid' && res.meta?.issueTx && (
                    <a className="btn ghost" href={`${ETHERSCAN}/tx/${res.meta.issueTx}`} target="_blank" rel="noreferrer">
                      View on Sepolia Etherscan ↗
                    </a>
                  )}
                  <button className="btn ghost" onClick={reset}>
                    {status === 'notfound' ? 'Search Again' : 'Verify Another Credential'}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </section>

      <QrScannerModal
        isOpen={scannerOpen}
        onClose={() => setScannerOpen(false)}
        onScanSuccess={(scannedId) => {
          setId(scannedId);
          setScannerOpen(false);
          toast(`✓ Scanned Certificate ID: ${scannedId}`);
          run(scannedId);
        }}
      />
    </main>
  );
}
