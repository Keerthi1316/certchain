import { useEffect, useState } from 'react';
import { useApp } from '../state.jsx';
import { short, hasWallet } from '../lib/chain.js';

const Icon = ({ d, cls }) => (
  <div className={`badge ${cls}`} style={{ width: 64, height: 64 }}>
    <svg viewBox="0 0 42 42" style={{ width: 30, height: 30 }}><path d={d} /></svg>
  </div>
);

export default function WalletModal() {
  const { walletOpen, setWalletOpen, wallet, rightNetwork, connect, switchNet, disconnect, toast } = useApp();
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const k = (e) => e.key === 'Escape' && setWalletOpen(false);
    addEventListener('keydown', k);
    return () => removeEventListener('keydown', k);
  }, [setWalletOpen]);

  if (!walletOpen) return null;
  const close = () => setWalletOpen(false);

  const copyKey = () => {
    navigator.clipboard.writeText('483ea0095c8df6fd81f5031b85323096efda2316c61d0082ffddff2d3d3c8869');
    setCopied(true);
    toast('✓ Demo account private key copied!');
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="overlay" onMouseDown={(e) => e.target === e.currentTarget && close()}>
      <div className="glass vcard" style={{ maxWidth: 480, width: '100%', textAlign: 'center' }} role="dialog" aria-modal="true" aria-labelledby="wmt">
        {!wallet.addr && (
          <>
            <div className="eyebrow">Web3 Authentication</div>
            <h3 className="vt" id="wmt" style={{ marginTop: 8 }}>Connect Wallet</h3>
            <p className="lead" style={{ margin: '0 auto 18px', fontSize: '.92rem' }}>
              Connect MetaMask to interact with the Ethereum Sepolia smart contract directly.
            </p>

            <div className="glass" style={{ padding: 14, marginBottom: 18, font: '700 1.05rem var(--font-d)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10 }}>
              <span>🦊</span> MetaMask Browser Extension
            </div>

            {hasWallet() ? (
              <button className="btn action" style={{ width: '100%', justifyContent: 'center' }} onClick={connect}>
                Connect MetaMask Wallet
              </button>
            ) : (
              <a className="btn action" style={{ width: '100%', justifyContent: 'center' }} href="https://metamask.io/download/" target="_blank" rel="noreferrer">
                Install MetaMask Extension ↗
              </a>
            )}

            {/* Demo wallet helper */}
            <div style={{ marginTop: 20, textAlign: 'left', background: 'rgba(51,214,255,.05)', border: '1px solid rgba(51,214,255,.2)', borderRadius: 14, padding: 14 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                <span style={{ fontSize: '.72rem', textTransform: 'uppercase', letterSpacing: '.12em', color: 'var(--cyan)', fontWeight: 600 }}>
                  ⚡ Pre-Funded Demo Issuer Account:
                </span>
                <button type="button" className="btn ghost sm" style={{ padding: '0 8px', fontSize: '.7rem' }} onClick={copyKey}>
                  {copied ? '✓ Copied' : 'Copy Key'}
                </button>
              </div>
              <div style={{ fontSize: '.8rem', color: 'var(--muted)' }}>
                Address: <code className="hash">0xe23ce9…ceF1</code>
              </div>
              <p style={{ fontSize: '.75rem', color: 'var(--muted)', margin: '6px 0 0' }}>
                Import this private key into MetaMask to immediately test as Contract Owner & Issuer on Sepolia. Or use the <b>⚡ Institution Relayer</b> in the issue wizard for gasless issuing!
              </p>
            </div>
          </>
        )}

        {wallet.addr && !rightNetwork && (
          <>
            <Icon cls="warn-c" d="M21 8v16M21 33v.5" />
            <h3 className="vt" id="wmt">Incorrect Network</h3>
            <p className="lead" style={{ margin: '0 auto 20px', fontSize: '.95rem' }}>
              CertChain is deployed on <b>Ethereum Sepolia Testnet</b> (Chain ID: 11155111).
            </p>
            <button className="btn action" style={{ width: '100%', justifyContent: 'center' }} onClick={switchNet}>
              Switch to Ethereum Sepolia →
            </button>
          </>
        )}

        {rightNetwork && (
          <>
            <Icon cls="ok-c" d="M8 21l9 9 17-17" />
            <h3 className="vt" id="wmt">Wallet Active</h3>
            <div className="hash" style={{ marginBottom: 10, fontSize: '.95rem' }}>{wallet.addr}</div>
            <div className="wrap" style={{ justifyContent: 'center', marginBottom: 16 }}>
              <span className="pill ok"><span className="dot" />Ethereum Sepolia Active</span>
            </div>
            <button className="btn ghost" style={{ width: '100%', justifyContent: 'center' }} onClick={() => { disconnect(); close(); }}>
              Disconnect Wallet
            </button>
          </>
        )}

        <div style={{ marginTop: 18 }}>
          <button className="pill info" style={{ cursor: 'pointer', background: 'transparent' }} onClick={close}>
            Dismiss
          </button>
        </div>
      </div>
    </div>
  );
}
