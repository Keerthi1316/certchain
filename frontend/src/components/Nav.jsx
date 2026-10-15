import { useState } from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useApp } from '../state.jsx';
import { short } from '../lib/chain.js';

export const Logo = () => (
  <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true">
    <rect x="3" y="3" width="11" height="11" rx="3" stroke="url(#lg)" strokeWidth="2" />
    <rect x="18" y="18" width="11" height="11" rx="3" stroke="url(#lg)" strokeWidth="2" />
    <path d="M14 8h6a3 3 0 013 3v7M9 14v6a3 3 0 003 3h6" stroke="url(#lg)" strokeWidth="2" />
    <path d="M20 10l2.5 2.5L27 7" stroke="#34e5a0" strokeWidth="2" strokeLinecap="round" />
    <defs>
      <linearGradient id="lg" x1="0" y1="0" x2="32" y2="32">
        <stop stopColor="#33d6ff" />
        <stop offset="1" stopColor="#8b5cf6" />
      </linearGradient>
    </defs>
  </svg>
);

export default function Nav() {
  const { wallet, rightNetwork, setWalletOpen, token, setToken, toast } = useApp();
  const [open, setOpen] = useState(false);
  const items = [
    ['/verify', 'Verify'],
    ['/certificates', 'Certificates'],
    ['/admin', 'Admin Console']
  ];

  const handleLogout = () => {
    setToken(null);
    toast('✓ Logged out of Admin');
  };

  return (
    <>
      <nav aria-label="Main">
        <Link className="logo" to="/" aria-label="CERTCHAIN home" onClick={() => setOpen(false)}>
          <Logo /> CERTCHAIN
        </Link>
        <div className="links">
          {items.map(([to, l]) => (
            <NavLink key={to} to={to}>{l}</NavLink>
          ))}
          {token && (
            <button
              onClick={handleLogout}
              style={{ background: 'none', border: 'none', color: 'var(--muted)', cursor: 'pointer', font: 'inherit', padding: 0 }}
              title="Sign out of Admin"
            >
              Sign Out
            </button>
          )}
        </div>
        <div className="wrap" style={{ flexWrap: 'nowrap' }}>
          <button className="btn" onClick={() => setWalletOpen(true)}>
            {wallet.addr ? (
              <>
                <span className="dot" style={{ color: rightNetwork ? '#34e5a0' : '#ff9a3c' }} />
                {short(wallet.addr)}
              </>
            ) : (
              'Connect Wallet'
            )}
          </button>
          <button
            className="btn ghost menu"
            aria-label="Menu"
            aria-expanded={open}
            onClick={() => setOpen(!open)}
          >
            {open ? '✕' : '☰'}
          </button>
        </div>
      </nav>
      {open && (
        <div className="glass drop">
          {items.map(([to, l]) => (
            <Link key={to} to={to} onClick={() => setOpen(false)}>
              {l}
            </Link>
          ))}
          {token && (
            <button
              onClick={() => { handleLogout(); setOpen(false); }}
              className="btn ghost sm"
              style={{ width: '100%', justifyContent: 'center', marginTop: 6 }}
            >
              Sign Out
            </button>
          )}
        </div>
      )}
    </>
  );
}
