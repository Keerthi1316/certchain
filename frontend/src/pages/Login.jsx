import { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { api } from '../lib/api.js';
import { useApp } from '../state.jsx';

export default function Login() {
  const { token, setToken, toast } = useApp();
  const nav = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState('');
  const [busy, setBusy] = useState(false);

  if (token) return <Navigate to="/admin" replace />;

  const fillDemo = () => {
    setEmail('admin@institute.edu');
    setPassword('admin123');
    toast('✓ Demo admin credentials loaded');
  };

  const submit = async (e) => {
    e?.preventDefault();
    setBusy(true);
    setErr('');
    try {
      const { token: t } = await api.login(email || 'admin@institute.edu', password || 'admin123');
      setToken(t);
      toast('✓ Signed in to Admin Portal');
      nav('/admin');
    } catch (x) {
      setErr(x.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <main style={{ minHeight: '100svh', display: 'grid', placeItems: 'center', padding: '110px 16px 40px' }}>
      <form className="glass vcard" style={{ maxWidth: 440, width: '100%' }} onSubmit={submit}>
        <div style={{ textAlign: 'center' }}>
          <div className="eyebrow">Institutional Portal</div>
          <h1 className="vt" style={{ marginTop: 8, fontSize: '2rem' }}>Admin Sign In</h1>
          <p className="lead" style={{ fontSize: '.88rem', margin: '4px auto 20px' }}>
            Access the certificate authority console and blockchain issuing engine.
          </p>
        </div>

        <div style={{ background: 'rgba(79,124,255,.08)', border: '1px dashed rgba(79,124,255,.3)', borderRadius: 12, padding: '10px 14px', marginBottom: 18, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ fontSize: '.8rem' }}>
            <span style={{ color: 'var(--muted)', display: 'block' }}>Default Test Account:</span>
            <strong style={{ color: 'var(--cyan)' }}>admin@institute.edu</strong> / <strong style={{ color: 'var(--lav)' }}>admin123</strong>
          </div>
          <button type="button" className="btn ghost sm" style={{ padding: '0 12px', fontSize: '.75rem' }} onClick={fillDemo}>
            ⚡ Auto-Fill
          </button>
        </div>

        <label className="field">
          <span>Email Address</span>
          <input className="input" type="email" required autoComplete="username" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="admin@institute.edu" />
        </label>
        <label className="field">
          <span>Password</span>
          <input className="input" type="password" required autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" />
        </label>

        {err && <div className="err" role="alert" style={{ marginBottom: 14 }}>⚠ {err}</div>}

        <button className="btn action" disabled={busy} style={{ width: '100%', justifyContent: 'center' }}>
          {busy ? 'Authenticating…' : 'Sign in to Dashboard →'}
        </button>
      </form>
    </main>
  );
}
