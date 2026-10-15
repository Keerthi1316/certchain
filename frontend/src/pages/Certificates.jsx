import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api.js';
import { revokeOnChain, friendlyError } from '../lib/chain.js';
import { Hash, StatusPill, fmtDate } from '../components/ui.jsx';
import { useApp } from '../state.jsx';

const COLS = { gridTemplateColumns: '1.2fr 1fr 1.3fr 1fr .9fr 1.1fr 1.3fr', minWidth: 960 };

export default function Certificates() {
  const { rightNetwork, wallet, setWalletOpen, toast, setToken } = useApp();
  const [rows, setRows] = useState(null);
  const [q, setQ] = useState('');
  const [revokingId, setRevokingId] = useState(null);

  const load = () => {
    api.list()
      .then(setRows)
      .catch((e) => {
        if (e.status === 401) setToken(null);
        else toast('✕ ' + e.message);
        setRows([]);
      });
  };

  useEffect(() => {
    load();
    /* eslint-disable-next-line */
  }, []);

  const revoke = async (c) => {
    if (!window.confirm(`Are you sure you want to revoke ${c.certId}? This action is irreversibly recorded on Ethereum Sepolia.`)) {
      return;
    }

    setRevokingId(c.certId);
    toast('Revoking on-chain… please wait');

    try {
      if (wallet.addr && rightNetwork) {
        // Use connected wallet
        const { txHash } = await revokeOnChain(c.certId);
        await api.revoke(c.certId, { txHash, revokedBy: wallet.addr });
      } else {
        // Use institutional authority relayer
        await api.relayRevoke(c.certId);
      }
      toast(`✓ Certificate ${c.certId} successfully revoked on-chain`);
      load();
    } catch (e) {
      toast('✕ ' + friendlyError(e));
    } finally {
      setRevokingId(null);
    }
  };

  const list = (rows || []).filter((c) =>
    [c.certId, c.recipientName, c.course].join(' ').toLowerCase().includes(q.toLowerCase())
  );

  return (
    <>
      <div className="eyebrow">Institutional Registry</div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 12 }}>
        <h1 className="h2" style={{ margin: 0 }}>Certificate Registry</h1>
        <Link className="btn action sm" to="/admin/issue">
          + Issue New Certificate
        </Link>
      </div>

      <input
        className="input"
        placeholder="🔍 Search registry by ID, recipient name, or course title…"
        aria-label="Search certificates"
        value={q}
        onChange={(e) => setQ(e.target.value)}
        style={{ marginBottom: 20 }}
      />

      <div className="glass tbl">
        {list.length > 0 && (
          <div className="tr th" style={COLS}>
            <span>Certificate ID</span>
            <span>Recipient</span>
            <span>Course</span>
            <span>Issued Date</span>
            <span>Status</span>
            <span>Transaction</span>
            <span>Actions</span>
          </div>
        )}

        {list.map((c) => (
          <div key={c.certId} className="tr" style={COLS}>
            <b>{c.certId}</b>
            <span>{c.recipientName}</span>
            <span>{c.course}</span>
            <span>{fmtDate(c.issuedAt)}</span>
            <StatusPill status={c.status} />
            <Hash value={c.issueTx} tx />
            <span className="wrap" style={{ gap: 6, flexWrap: 'nowrap' }}>
              <Link className="btn ghost sm" style={{ padding: '0 10px', fontSize: '.72rem' }} to={`/verify/${c.certId}`}>
                Verify
              </Link>
              {c.hasPdf && (
                <a className="btn ghost sm" style={{ padding: '0 10px', fontSize: '.72rem' }} href={api.pdfUrl(c.certId)} target="_blank" rel="noreferrer">
                  PDF 📄
                </a>
              )}
              {c.status === 'valid' && (
                <button
                  className="btn danger sm"
                  style={{ padding: '0 10px', fontSize: '.72rem' }}
                  disabled={revokingId === c.certId}
                  onClick={() => revoke(c)}
                >
                  {revokingId === c.certId ? 'Revoking…' : 'Revoke'}
                </button>
              )}
            </span>
          </div>
        ))}

        {rows && !list.length && (
          <div className="empty">
            <div className="rt" style={{ fontSize: '1.3rem' }}>{q ? 'No matching certificates' : 'No certificates issued yet'}</div>
            <p className="lead" style={{ margin: '6px auto 16px', fontSize: '.9rem' }}>
              {q ? 'Try adjusting your search criteria.' : 'Certificates issued by your institution will appear here.'}
            </p>
            {!q && <Link className="btn action" to="/admin/issue">Issue Your First Certificate →</Link>}
          </div>
        )}

        {!rows && (
          <div className="empty">
            <p className="lead" style={{ margin: 'auto' }}>Loading immutable blockchain records…</p>
          </div>
        )}
      </div>
    </>
  );
}
