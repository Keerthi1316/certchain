import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api.js';
import { chainStats, manageIssuer, short, friendlyError, CONTRACT_ADDRESS, ETHERSCAN } from '../lib/chain.js';
import { useApp } from '../state.jsx';
import { StatusPill } from '../components/ui.jsx';
import { downloadCertificatePdf } from '../lib/pdf.js';

export default function Dashboard() {
  const { wallet, rightNetwork, toast, setToken } = useApp();
  const [s, setS] = useState({ total: 0, valid: 0, revoked: 0 });
  const [recent, setRecent] = useState([]);
  const [chain, setChain] = useState(null);
  const [addr, setAddr] = useState('');
  const [authorizing, setAuthorizing] = useState(false);

  const loadData = () => {
    api.stats().then(res => {
      if (res && typeof res.total === 'number') setS(res);
    }).catch((e) => { if (e?.status === 401) setToken(null); });

    api.list().then((l) => {
      const arr = Array.isArray(l) ? l : [];
      setRecent(arr.slice(0, 6));
    }).catch(() => setRecent([]));
  };

  useEffect(() => {
    loadData();
  }, [setToken]);

  useEffect(() => {
    chainStats(wallet.addr).then(setChain).catch(() => setChain(null));
  }, [wallet.addr]);

  const issuer = async (add) => {
    try {
      await manageIssuer(add, addr.trim());
      toast(add ? '✓ Issuer authorized on Sepolia' : '✓ Issuer revoked');
      setAddr('');
      setChain(await chainStats(wallet.addr));
      loadData();
    } catch (e) {
      toast('✕ ' + friendlyError(e));
    }
  };

  const quickAuthorize = async () => {
    if (!wallet.addr) return toast('⚠ Connect your wallet first');
    setAuthorizing(true);
    try {
      const res = await api.authorizeIssuer(wallet.addr);
      toast(res.alreadyIssuer ? '✓ Wallet is already an authorized issuer' : '✓ Wallet authorized as issuer on Sepolia!');
      setChain(await chainStats(wallet.addr));
    } catch (e) {
      toast('✕ ' + friendlyError(e));
    } finally {
      setAuthorizing(false);
    }
  };

  const cards = [
    ['Total Certificates', s.total, 'var(--g-cool)', ['info', 'Database Records']],
    ['On-Chain Valid', s.valid, 'linear-gradient(135deg,#34e5a0,#33d6ff)', ['ok', '✓ Sepolia Anchored']],
    ['Revoked Records', s.revoked, 'linear-gradient(135deg,#ff6b6b,#ff8a1f)', ['bad', '⚠ Revoked']],
    ['Authorized Issuers', chain?.issuers ?? '—', 'var(--g-hot)', ['info', 'Smart Contract']]
  ];

  return (
    <>
      <div className="eyebrow">Institutional Certificate Authority</div>
      <h1 className="h2" style={{ marginBottom: 12 }}>Admin Command Center</h1>

      <div className="wrap" style={{ marginBottom: 20, alignItems: 'center' }}>
        <span className={`pill ${rightNetwork ? 'ok' : 'warn'}`}>
          {rightNetwork ? <><span className="dot" />Sepolia connected</> : wallet.addr ? '⚠ Switch to Sepolia' : 'Wallet not connected'}
        </span>
        {wallet.addr && <span className="pill info mono2">{short(wallet.addr)}</span>}
        {chain?.isOwner && <span className="pill ok">Contract Owner</span>}
        {chain?.isIssuer && <span className="pill info">Authorized Issuer</span>}
        {wallet.addr && !chain?.isIssuer && (
          <button className="btn action sm" disabled={authorizing} onClick={quickAuthorize}>
            {authorizing ? 'Authorizing…' : '⚡ Authorize My Wallet as Issuer'}
          </button>
        )}
      </div>

      {/* Contract info banner */}
      <div style={{ background: 'rgba(51,214,255,.05)', border: '1px solid rgba(51,214,255,.2)', borderRadius: 16, padding: '14px 20px', marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
        <div>
          <span style={{ fontSize: '.75rem', textTransform: 'uppercase', letterSpacing: '.15em', color: 'var(--muted)', display: 'block' }}>Smart Contract Address</span>
          <span className="mono" style={{ color: 'var(--cyan)', fontWeight: 600 }}>{CONTRACT_ADDRESS}</span>
        </div>
        <div className="wrap">
          <a className="btn ghost sm" href={`${ETHERSCAN}/address/${CONTRACT_ADDRESS}`} target="_blank" rel="noreferrer">
            View on Sepolia Etherscan ↗
          </a>
          <Link className="btn action sm" to="/admin/issue">
            + Issue New Certificate
          </Link>
        </div>
      </div>

      <div className="grid g4">
        {cards.map(([l, n, c, [pc, pt]]) => (
          <div key={l} className="glass stat lift" style={{ '--c': c }}>
            <span className="eyebrow">{l}</span>
            <b>{n}</b>
            <span className={`pill ${pc}`}>{pt}</span>
          </div>
        ))}
      </div>

      <div style={{ marginTop: 32, marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
        <div>
          <div className="eyebrow">Registry Overview</div>
          <h3 className="vt" style={{ textAlign: 'left', margin: '4px 0 0' }}>Recent Issuances</h3>
        </div>
        <Link className="btn ghost sm" to="/certificates">
          View All Registry ({s.total}) →
        </Link>
      </div>

      <div className="glass tbl">
        <div className="tr th" style={{ gridTemplateColumns: '1.2fr 1fr 1.3fr .9fr 1fr' }}>
          <span>Certificate ID</span>
          <span>Recipient</span>
          <span>Course</span>
          <span>Status</span>
          <span>Action</span>
        </div>
        {Array.isArray(recent) && recent.length ? (
          recent.map((c) => {
            const certId = c?.certId || c?.cert_id || 'CERT-2026-0001';
            const name = c?.recipientName || c?.recipient_name || '—';
            return (
              <div key={certId} className="tr" style={{ gridTemplateColumns: '1.2fr 1fr 1.3fr .9fr 1fr' }}>
                <b>{certId}</b>
                <span>{name}</span>
                <span>{c?.course || '—'}</span>
                <StatusPill status={c?.status || 'valid'} />
                <div className="wrap" style={{ gap: 6, flexWrap: 'nowrap' }}>
                  <Link className="btn ghost sm" style={{ padding: '0 10px', fontSize: '.72rem' }} to={`/verify/${certId}`}>
                    Verify
                  </Link>
                  <button
                    className="btn ghost sm"
                    style={{ padding: '0 10px', fontSize: '.72rem' }}
                    onClick={async () => {
                      toast('Downloading certificate PDF…');
                      try {
                        await downloadCertificatePdf(c);
                        toast(`✓ Downloaded ${certId}.pdf`);
                      } catch (err) {
                        toast('✕ Download error: ' + err.message);
                      }
                    }}
                    title="Download Certificate PDF"
                  >
                    PDF 📄
                  </button>
                </div>
              </div>
            );
          })
        ) : (
          <div className="empty">
            <div className="rt" style={{ fontSize: '1.3rem' }}>No certificates yet</div>
            <p className="lead" style={{ margin: '6px auto 16px', fontSize: '.9rem' }}>
              Issue your first blockchain certificate to populate the institutional registry.
            </p>
            <Link className="btn action" to="/admin/issue">Issue First Certificate →</Link>
          </div>
        )}
      </div>

      {/* Issuer management */}
      <div className="glass" style={{ padding: 24, marginTop: 24 }}>
        <div className="eyebrow" style={{ marginBottom: 8 }}>Issuer Authority Management</div>
        <h4 style={{ margin: '0 0 10px', fontFamily: 'var(--font-d)' }}>Authorize or Revoke Issuer Wallets</h4>
        <p className="lead" style={{ fontSize: '.88rem', margin: '0 0 16px' }}>
          Grant specific Ethereum wallets authority to sign and issue verified credentials onto the smart contract.
        </p>
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <input
            className="input"
            style={{ flex: 1, minWidth: 280 }}
            placeholder="0x… Ethereum wallet address to authorize or revoke"
            value={addr}
            onChange={(e) => setAddr(e.target.value)}
            aria-label="Issuer address"
          />
          <button className="btn action sm" disabled={!addr.trim()} onClick={() => issuer(true)}>
            + Authorize Issuer
          </button>
          <button className="btn ghost sm" disabled={!addr.trim()} onClick={() => issuer(false)}>
            - Remove Issuer
          </button>
        </div>
      </div>
    </>
  );
}
