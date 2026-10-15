import { useApp } from '../state.jsx';
import { ETHERSCAN, short } from '../lib/chain.js';

export const fmtDate = (d) => new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

export function Toasts() {
  const { toasts } = useApp();
  return <div className="toasts" aria-live="polite">{toasts.map((t) => <div key={t.id} className="toast">{t.m}</div>)}</div>;
}

const PILLS = {
  valid: ['ok', '✓ Verified'], revoked: ['bad', '⚠ Revoked'], pending: ['pend', '● Pending'],
  notfound: ['bad', '✕ Not found'], mismatch: ['warn', '⚠ Hash mismatch'],
};
export const StatusPill = ({ status }) => {
  const [c, l] = PILLS[status] || PILLS.pending;
  return <span className={`pill ${c}`}>{l}</span>;
};

export function Hash({ value, tx }) {
  const { toast } = useApp();
  if (!value) return <span>—</span>;
  const copy = async () => { try { await navigator.clipboard.writeText(value); toast('✓ Copied'); } catch { toast('✕ Copy failed'); } };
  return (
    <span className="hash">
      {tx ? <a href={`${ETHERSCAN}/tx/${value}`} target="_blank" rel="noreferrer">{short(value)}</a> : short(value)}{' '}
      <button className="cp-b" aria-label="Copy" onClick={copy}>⧉</button>
    </span>
  );
}

export const Section = ({ eyebrow, title, children }) => (
  <section style={{ paddingTop: 130 }}>
    <div className="eyebrow">{eyebrow}</div>
    <h2 className="h2">{title}</h2>
    {children}
  </section>
);
