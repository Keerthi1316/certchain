import { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { connectWallet, switchToSepolia, hasWallet, SEPOLIA_ID, friendlyError } from './lib/chain.js';

const Ctx = createContext(null);
export const useApp = () => useContext(Ctx);

export function AppProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const [wallet, setWallet] = useState({ addr: null, chainId: null });
  const [walletOpen, setWalletOpen] = useState(false);
  const [token, setTokenState] = useState(() => {
    const t = localStorage.getItem('cc_token');
    return t && t !== 'null' && t !== 'undefined' ? t : null;
  });

  const toast = useCallback((m) => {
    const id = Math.random();
    setToasts((t) => [...t, { id, m }]);
    setTimeout(() => setToasts((t) => t.filter((x) => x.id !== id)), 3600);
  }, []);

  const setToken = (t) => { t ? localStorage.setItem('cc_token', t) : localStorage.removeItem('cc_token'); setTokenState(t); };
  const rightNetwork = wallet.addr && wallet.chainId === SEPOLIA_ID;

  const connect = async () => {
    try { setWallet(await connectWallet()); toast('✓ Wallet connected'); }
    catch (e) { toast('✕ ' + friendlyError(e)); }
  };
  const switchNet = async () => {
    try { await switchToSepolia(); toast('✓ Switched to Sepolia'); } catch (e) { toast('✕ ' + friendlyError(e)); }
  };
  const disconnect = () => setWallet({ addr: null, chainId: null });

  useEffect(() => {
    if (!hasWallet()) return;
    const onAcc = (a) => setWallet((w) => (a.length ? { ...w, addr: a[0] } : { addr: null, chainId: null }));
    const onChain = (c) => setWallet((w) => ({ ...w, chainId: parseInt(c, 16) }));
    window.ethereum.on?.('accountsChanged', onAcc);
    window.ethereum.on?.('chainChanged', onChain);
    return () => { window.ethereum.removeListener?.('accountsChanged', onAcc); window.ethereum.removeListener?.('chainChanged', onChain); };
  }, []);

  return (
    <Ctx.Provider value={{ toasts, toast, wallet, rightNetwork, connect, switchNet, disconnect, walletOpen, setWalletOpen, token, setToken }}>
      {children}
    </Ctx.Provider>
  );
}
