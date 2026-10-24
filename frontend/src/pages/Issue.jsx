import { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api.js';
import { makeCertificatePdf, sha256Hex } from '../lib/pdf.js';
import { chainStats, issueOnChain, ETHERSCAN, short, friendlyError } from '../lib/chain.js';
import Certificate from '../components/Certificate.jsx';
import { fmtDate, Hash } from '../components/ui.jsx';
import { useApp } from '../state.jsx';

const COURSES = [
  'Blockchain Technology',
  'Applied Cryptography',
  'Distributed Systems',
  'Web Engineering',
  'Artificial Intelligence & ML',
  'Cloud Security & Architecture'
];

const PRESETS = [
  { name: 'Keerthi Katuri', email: 'keerthi@gcet.edu', course: 'Blockchain Technology', achievement: 'Excellence in Smart Contracts' },
  { name: 'Sarah Connor', email: 'sarah.c@institute.edu', course: 'Applied Cryptography', achievement: 'Advanced Cryptographic Protocols' },
  { name: 'David Chen', email: 'david.chen@tech.org', course: 'Distributed Systems', achievement: 'Mastery in Consensus Algorithms' }
];

const TX = ['Certificate generated', 'Document fingerprinted', 'Broadcasting to Sepolia', 'Mining block on-chain', 'Database & PDF synchronized', 'Blockchain record active'];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export default function Issue() {
  const { wallet, rightNetwork, setWalletOpen, toast } = useApp();
  const [step, setStep] = useState(1);
  const [method, setMethod] = useState('relayer'); // 'relayer' | 'wallet'
  const [f, setF] = useState({ name: '', email: '', course: COURSES[0], achievement: '', template: 'premium' });
  const [doc, setDoc] = useState(null);
  const [cur, setCur] = useState(0);
  const [txh, setTxh] = useState('');
  const [chainRes, setChainRes] = useState(null);
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);
  const [authorizing, setAuthorizing] = useState(false);

  const set = (k) => (e) => setF({ ...f, [k]: e.target.value });

  const applyPreset = (p) => {
    setF({ ...f, ...p });
    toast(`✓ Loaded preset: ${p.name}`);
  };

  const generate = async (e) => {
    e.preventDefault();
    if (!f.name.trim() || !f.email.trim() || !f.achievement.trim()) {
      return toast('⚠ Fill in all required fields');
    }
    setBusy(true);
    try {
      const { certId } = await api.nextId();
      const issued = fmtDate(Date.now());
      const issuerDisplay = method === 'wallet' && wallet.addr ? short(wallet.addr) : '0xe23ce9…ceF1 (Inst. Authority)';
      const bytes = await makeCertificatePdf({
        certId,
        name: f.name.trim(),
        course: f.course,
        achievement: f.achievement.trim(),
        issued,
        issuer: issuerDisplay
      });
      const hash = await sha256Hex(bytes);
      setDoc({ certId, bytes, hash, issued, issuerDisplay });
      setStep(2);
      toast('✓ Certificate rendered and ready for signing');
    } catch (x) {
      toast('✕ ' + friendlyError(x));
    } finally {
      setBusy(false);
    }
  };

  const authorizeWallet = async () => {
    if (!wallet.addr) return toast('⚠ Connect wallet first');
    setAuthorizing(true);
    try {
      const res = await api.authorizeIssuer(wallet.addr);
      toast(res.alreadyIssuer ? '✓ Wallet is already an authorized issuer' : '✓ Wallet authorized as issuer on Sepolia!');
      setErr('');
    } catch (x) {
      toast('✕ ' + friendlyError(x));
    } finally {
      setAuthorizing(false);
    }
  };

  const issue = async () => {
    setStep(4);
    setErr('');
    setBusy(true);
    setCur(0);

    try {
      let res = chainRes;
      let issuerAddress = '';

      if (!res) {
        await sleep(400);
        setCur(1); // fingerprinted
        await sleep(400);
        setCur(2); // broadcasting

        if (method === 'wallet') {
          if (!rightNetwork) {
            toast('⚠ Connect your wallet to Sepolia first');
            setWalletOpen(true);
            setStep(3);
            return;
          }
          const cs = await chainStats(wallet.addr);
          if (!cs.isIssuer) {
            setErr(`Your wallet (${short(wallet.addr)}) is not an authorized issuer on this contract.`);
            setStep(4);
            return;
          }
          res = await issueOnChain(doc.certId, doc.hash, (h) => {
            setTxh(h);
            setCur(3);
          });
          issuerAddress = wallet.addr;
        } else {
          // Relayed issuance using institutional deployer key
          const relRes = await api.relayIssue({ certId: doc.certId, docHash: doc.hash });
          res = { txHash: relRes.txHash, block: relRes.blockNumber };
          issuerAddress = relRes.issuer;
          setTxh(relRes.txHash);
          setCur(3);
        }

        setChainRes(res);
      }

      await sleep(600);
      setCur(4); // Database sync

      // Persist metadata and upload PDF to backend
      await api.save({
        certId: doc.certId,
        recipientName: f.name.trim(),
        recipientEmail: f.email.trim(),
        course: f.course,
        achievement: f.achievement.trim(),
        template: f.template,
        docHash: doc.hash,
        issuer: issuerAddress,
        issueTx: res.txHash
      });
      await api.uploadPdf(doc.certId, doc.bytes);

      setCur(5); // Blockchain verified
      await sleep(500);
      toast('✓ Certificate permanently anchored on Ethereum Sepolia!');
      setStep(5);
    } catch (x) {
      setErr(friendlyError(x));
      toast('✕ ' + friendlyError(x));
    } finally {
      setBusy(false);
    }
  };

  const again = () => {
    setStep(1);
    setDoc(null);
    setChainRes(null);
    setTxh('');
    setErr('');
    setF({ ...f, name: '', email: '', achievement: '' });
  };

  return (
    <>
      <div className="eyebrow">Institutional Authority</div>
      <h1 className="h2" style={{ marginBottom: 16 }}>Issue Verified<br />Certificate</h1>
      <div className="steps" aria-label={`Step ${step} of 5`}>
        {[1, 2, 3, 4, 5].map((n) => (
          <span key={n} className={n <= step ? 'on' : ''} />
        ))}
      </div>

      <div className="glass wiz">
        {step === 1 && (
          <form onSubmit={generate}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
              <div>
                <div className="eyebrow">Step 01</div>
                <h2 className="vt" style={{ textAlign: 'left', margin: '4px 0 0' }}>Certificate Details</h2>
              </div>
              <div className="wrap">
                <span style={{ fontSize: '.75rem', color: 'var(--muted)', alignSelf: 'center' }}>Quick Presets:</span>
                {PRESETS.map((p) => (
                  <button key={p.name} type="button" className="btn ghost sm" style={{ fontSize: '.72rem', padding: '0 10px' }} onClick={() => applyPreset(p)}>
                    ⚡ {p.name.split(' ')[0]}
                  </button>
                ))}
              </div>
            </div>

            {/* Issuance mode selector */}
            <div style={{ background: 'rgba(255,255,255,.03)', border: '1px solid var(--glass-b)', borderRadius: 16, padding: '14px 18px', marginBottom: 20 }}>
              <div className="eyebrow" style={{ marginBottom: 8 }}>Signing & Blockchain Method</div>
              <div className="grid g2" style={{ gap: 12 }}>
                <label style={{ display: 'flex', gap: 10, alignItems: 'flex-start', cursor: 'pointer', padding: 10, borderRadius: 10, background: method === 'relayer' ? 'rgba(51,214,255,.1)' : 'transparent', border: `1px solid ${method === 'relayer' ? 'var(--cyan)' : 'transparent'}` }}>
                  <input type="radio" name="method" checked={method === 'relayer'} onChange={() => setMethod('relayer')} style={{ marginTop: 4 }} />
                  <div>
                    <strong style={{ display: 'block', color: 'var(--cyan)' }}>⚡ Institution Relayer (Gasless / Instant)</strong>
                    <small style={{ color: 'var(--muted)', fontSize: '.8rem' }}>Uses the institution's authorized deployer key on Sepolia. Ideal for quick demos and evaluator tests.</small>
                  </div>
                </label>

                <label style={{ display: 'flex', gap: 10, alignItems: 'flex-start', cursor: 'pointer', padding: 10, borderRadius: 10, background: method === 'wallet' ? 'rgba(139,92,246,.1)' : 'transparent', border: `1px solid ${method === 'wallet' ? 'var(--violet)' : 'transparent'}` }}>
                  <input type="radio" name="method" checked={method === 'wallet'} onChange={() => setMethod('wallet')} style={{ marginTop: 4 }} />
                  <div>
                    <strong style={{ display: 'block', color: 'var(--lav)' }}>🦊 MetaMask Wallet (Self-Signed)</strong>
                    <small style={{ color: 'var(--muted)', fontSize: '.8rem' }}>Sign directly with your connected Web3 wallet on Ethereum Sepolia Testnet.</small>
                  </div>
                </label>
              </div>
            </div>

            <div className="grid g2">
              <label className="field">
                <span>Recipient Name *</span>
                <input className="input" value={f.name} onChange={set('name')} placeholder="e.g. Keerthi Katuri" maxLength={100} required />
              </label>
              <label className="field">
                <span>Recipient Email *</span>
                <input className="input" type="email" value={f.email} onChange={set('email')} placeholder="recipient@domain.com" required />
              </label>
              <label className="field">
                <span>Program / Course *</span>
                <select className="input" value={f.course} onChange={set('course')}>
                  {COURSES.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </label>
              <label className="field">
                <span>Achievement / Distinction *</span>
                <input className="input" value={f.achievement} onChange={set('achievement')} placeholder="e.g. First Class with Distinction" maxLength={60} required />
              </label>
            </div>

            <label className="field">
              <span>Certificate Template Styling</span>
              <select className="input" value={f.template} onChange={set('template')}>
                <option value="premium">Cosmic Premium (Dark Glass & Holographic Accents)</option>
                <option value="classic">Academic Classic (Royal Gold & Parchment Style)</option>
                <option value="minimal">Modern Minimal (Clean Obsidian)</option>
              </select>
            </label>

            <button className="btn action" disabled={busy} style={{ marginTop: 8 }}>
              {busy ? 'Rendering Document…' : 'Generate & Preview Certificate →'}
            </button>
          </form>
        )}

        {step === 2 && (
          <>
            <div className="eyebrow" style={{ marginBottom: 8 }}>Step 02 • Document Render</div>
            <h2 className="vt" style={{ textAlign: 'left', marginBottom: 16 }}>Live Document Preview</h2>
            <Certificate
              tpl={f.template}
              name={f.name}
              course={f.course}
              achievement={f.achievement}
              certId={doc.certId}
              issued={doc.issued}
              issuer={doc.issuerDisplay}
            />
            <div className="wrap" style={{ marginTop: 24 }}>
              <button className="btn action" onClick={() => setStep(3)}>Proceed to Cryptographic Hashing →</button>
              <button className="btn ghost" onClick={() => setStep(1)}>← Edit Details</button>
            </div>
          </>
        )}

        {step === 3 && (
          <>
            <div className="eyebrow" style={{ marginBottom: 8 }}>Step 03 • Cryptographic Hash</div>
            <h2 className="vt" style={{ textAlign: 'left' }}>Document Fingerprint</h2>
            <p className="lead" style={{ fontSize: '.95rem' }}>
              The SHA-256 cryptographic digest of the exact byte sequence of this generated PDF. This immutable 32-byte hash will be anchored permanently onto the Ethereum Sepolia smart contract.
            </p>
            <div className="hashbox hash" style={{ fontSize: '1rem', padding: '18px', background: 'rgba(51,214,255,.05)', border: '1px solid rgba(51,214,255,.3)' }}>
              {doc.hash}
            </div>
            <div className="wrap" style={{ marginBottom: 20 }}>
              <span className="pill ok"><span className="dot" />SHA-256 Fingerprint Generated</span>
              <span className="pill info">Target Chain: Ethereum Sepolia</span>
              <span className="pill warn">Method: {method === 'wallet' ? 'MetaMask' : '⚡ Institution Relayer'}</span>
            </div>
            <div className="wrap">
              <button className="btn action" disabled={busy} onClick={issue}>
                Anchor to Ethereum Sepolia →
              </button>
              <button className="btn ghost" onClick={() => setStep(2)}>← Back to Preview</button>
            </div>
          </>
        )}

        {step === 4 && (
          <>
            <div className="eyebrow" style={{ marginBottom: 8 }}>Step 04 • On-Chain Transaction</div>
            <h2 className="vt" style={{ textAlign: 'left' }}>Broadcasting to Ethereum</h2>
            <ol className="tx">
              {TX.map((t, i) => (
                <li key={t} className={i < cur ? 'done' : i === cur ? 'on' : ''}>
                  <b>{t}</b>
                  {i === 1 && <small>SHA-256 Digest: {short(doc?.hash, 10, 8)}</small>}
                  {i === 3 && txh && <small>Tx Hash: {short(txh, 10, 8)}</small>}
                </li>
              ))}
            </ol>

            {err && (
              <div style={{ background: 'rgba(255,107,107,.1)', border: '1px solid var(--bad)', borderRadius: 14, padding: 18, margin: '20px 0' }}>
                <div className="err" role="alert" style={{ margin: 0, fontWeight: 600 }}>⚠ {err}</div>
                {err.includes('not an authorized issuer') && (
                  <div style={{ marginTop: 12 }}>
                    <p style={{ fontSize: '.85rem', color: 'var(--muted)', margin: '0 0 10px' }}>
                      You can authorize your current wallet with one click using the institutional owner relayer:
                    </p>
                    <button className="btn action sm" disabled={authorizing} onClick={authorizeWallet}>
                      {authorizing ? 'Authorizing on-chain…' : '⚡ Authorize My Wallet as Issuer'}
                    </button>
                  </div>
                )}
                <div className="wrap" style={{ marginTop: 14 }}>
                  <button className="btn sm" disabled={busy} onClick={issue}>Try Again</button>
                  <button className="btn ghost sm" onClick={() => { setMethod('relayer'); setErr(''); }}>
                    Switch to Gasless Relayer
                  </button>
                </div>
              </div>
            )}
          </>
        )}

        {step === 5 && (
          <div style={{ textAlign: 'center' }}>
            <div className="rhead ok-c">
              <div className="badge">
                <svg viewBox="0 0 42 42"><path d="M6 21l10 10L36 11" /></svg>
              </div>
              <div className="rt">Certificate Anchored on Sepolia</div>
              <div style={{ color: 'var(--muted)', fontSize: '.95rem' }}>
                The cryptographic SHA-256 hash has been verified and permanently mined on the blockchain.
              </div>
            </div>

            <div className="rows">
              <div style={{ '--i': 0 }}><span>Certificate ID</span><em>{doc.certId}</em></div>
              <div style={{ '--i': 1 }}><span>Recipient</span><em>{f.name} ({f.email})</em></div>
              <div style={{ '--i': 2 }}><span>Course</span><em>{f.course}</em></div>
              <div style={{ '--i': 3 }}><span>Document SHA-256</span><em><Hash value={doc.hash} /></em></div>
              <div style={{ '--i': 4 }}><span>Transaction Hash</span><em><Hash value={chainRes?.txHash} tx /></em></div>
              <div style={{ '--i': 5 }}><span>Confirmed Block</span><em>#{chainRes?.block || 'Mined'}</em></div>
            </div>

            <div className="wrap" style={{ justifyContent: 'center', marginTop: 24 }}>
              <Link className="btn action" to={`/verify/${doc.certId}`}>Public Verification Portal →</Link>
              <a className="btn ghost" href={api.pdfUrl(doc.certId)} target="_blank" rel="noreferrer">
                Download Official PDF 📄
              </a>
              {chainRes?.txHash && (
                <a className="btn ghost" href={`${ETHERSCAN}/tx/${chainRes.txHash}`} target="_blank" rel="noreferrer">
                  View on Etherscan ↗
                </a>
              )}
              <button className="btn ghost" onClick={again}>Issue Another Certificate</button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
