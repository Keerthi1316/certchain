import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../lib/api.js';
import { revokeOnChain, friendlyError } from '../lib/chain.js';
import { downloadCertificatePdf, openCertificatePdf, getPdfBlob } from '../lib/pdf.js';
import { Hash, StatusPill, fmtDate } from '../components/ui.jsx';
import { useApp } from '../state.jsx';

const COLS = { gridTemplateColumns: '1.2fr 1fr 1.3fr 1fr .9fr 1.1fr 1.4fr', minWidth: 980 };

export default function Certificates() {
  const { rightNetwork, wallet, setWalletOpen, toast, setToken } = useApp();
  const [rows, setRows] = useState(null);
  const [q, setQ] = useState('');
  const [revokingId, setRevokingId] = useState(null);
  const [downloadingId, setDownloadingId] = useState(null);
  const [previewCert, setPreviewCert] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const load = () => {
    api.list()
      .then((data) => setRows(Array.isArray(data) ? data : []))
      .catch((e) => {
        if (e?.status === 401) setToken(null);
        else toast('✕ ' + (e?.message || 'Failed to load registry'));
        setRows([]);
      });
  };

  useEffect(() => {
    load();
    /* eslint-disable-next-line */
  }, []);

  const handleDownloadPdf = async (c) => {
    const id = c.certId || c.cert_id;
    setDownloadingId(id);
    toast('Generating official certificate PDF…');
    try {
      await downloadCertificatePdf(c);
      toast(`✓ Downloaded ${id}.pdf`);
    } catch (err) {
      toast('✕ Failed to download PDF: ' + (err.message || 'Error'));
    } finally {
      setDownloadingId(null);
    }
  };

  const handlePreviewPdf = async (c) => {
    const id = c.certId || c.cert_id;
    toast('Opening certificate preview…');
    try {
      const blob = await getPdfBlob(c);
      const url = URL.createObjectURL(blob);
      setPreviewUrl(url);
      setPreviewCert(c);
    } catch (err) {
      toast('✕ Error loading PDF preview: ' + err.message);
    }
  };

  const closePreview = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(null);
    setPreviewCert(null);
  };

  const revoke = async (c) => {
    const certId = c?.certId || c?.cert_id;
    if (!window.confirm(`Are you sure you want to revoke ${certId}? This action is irreversibly recorded on Ethereum Sepolia.`)) {
      return;
    }

    setRevokingId(certId);
    toast('Revoking on-chain… please wait');

    try {
      if (wallet.addr && rightNetwork) {
        // Use connected wallet
        const { txHash } = await revokeOnChain(certId);
        await api.revoke(certId, { txHash, revokedBy: wallet.addr });
      } else {
        // Use institutional authority relayer
        await api.relayRevoke(certId);
      }
      toast(`✓ Certificate ${certId} successfully revoked on-chain`);
      load();
    } catch (e) {
      toast('✕ ' + friendlyError(e));
    } finally {
      setRevokingId(null);
    }
  };

  const safeRows = Array.isArray(rows) ? rows : [];
  const list = safeRows.filter((c) => {
    if (!c) return false;
    const certId = c.certId || c.cert_id || '';
    const name = c.recipientName || c.recipient_name || '';
    const course = c.course || '';
    return [certId, name, course].join(' ').toLowerCase().includes((q || '').toLowerCase());
  });

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
              <Link className="btn ghost sm" style={{ padding: '0 8px', fontSize: '.72rem' }} to={`/verify/${c.certId}`}>
                Verify
              </Link>
              <button
                className="btn ghost sm"
                style={{ padding: '0 8px', fontSize: '.72rem' }}
                onClick={() => handlePreviewPdf(c)}
                title="View Certificate PDF in modal"
              >
                View PDF 📄
              </button>
              <button
                className="btn ghost sm"
                style={{ padding: '0 8px', fontSize: '.72rem' }}
                disabled={downloadingId === c.certId}
                onClick={() => handleDownloadPdf(c)}
                title="Download Certificate PDF directly"
              >
                {downloadingId === c.certId ? '⏳' : '📥'}
              </button>
              {c.status === 'valid' && (
                <button
                  className="btn danger sm"
                  style={{ padding: '0 8px', fontSize: '.72rem' }}
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

      {/* Certificate PDF Preview Modal */}
      {previewCert && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(5, 5, 17, 0.85)', backdropFilter: 'blur(8px)', zIndex: 9999, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 20 }}>
          <div className="glass" style={{ width: '92vw', maxWidth: 960, maxHeight: '92vh', display: 'flex', flexDirection: 'column', padding: 24, borderRadius: 20, boxShadow: '0 25px 60px rgba(0,0,0,0.7)', border: '1px solid rgba(139, 92, 246, 0.4)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 12 }}>
              <div>
                <div className="eyebrow" style={{ marginBottom: 4 }}>Authentic Institutional Credential</div>
                <h3 style={{ margin: 0, fontSize: '1.25rem', fontFamily: 'var(--font-d)' }}>
                  {previewCert.certId || previewCert.cert_id} — {previewCert.recipientName || previewCert.recipient_name}
                </h3>
              </div>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                <button className="btn action sm" onClick={() => handleDownloadPdf(previewCert)}>
                  Download PDF 📥
                </button>
                <button className="btn ghost sm" onClick={() => openCertificatePdf(previewCert)}>
                  Open in Tab ↗
                </button>
                <button className="btn ghost sm" onClick={closePreview} style={{ fontSize: '1rem', padding: '0 12px' }}>
                  ✕
                </button>
              </div>
            </div>

            <div style={{ flex: 1, minHeight: 480, background: '#050511', borderRadius: 12, overflow: 'hidden', border: '1px solid rgba(255,255,255,0.08)' }}>
              {previewUrl ? (
                <iframe src={previewUrl} title="Certificate PDF Preview" style={{ width: '100%', height: '100%', border: 'none', minHeight: 520 }} />
              ) : (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)' }}>
                  Loading certificate preview…
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
