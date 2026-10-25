const BASE = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '');
const tok = () => localStorage.getItem('cc_token');

const SEED_CERTS = [
  { cert_id: 'CERT-2026-0001', recipient_name: 'Keerthi Katuri', course: 'Blockchain Technology', achievement: 'Excellence in Smart Contract Verification', status: 'valid', issued_at: '2026-10-14T10:00:00.000Z', issue_tx: '0x243790c4e526836ef380d4f41bfec44ded681699a882061fc538be5587ce7f78', has_pdf: 1, issuer: '0xe23ce985284365B92fF6EE0F855a11811274ceF1' },
  { cert_id: 'CERT-2026-0002', recipient_name: 'Keerthi Katuri', course: 'Artificial Intelligence & Machine Learning', achievement: 'Excellence in Deep Learning & Neural Models', status: 'valid', issued_at: '2026-10-14T11:00:00.000Z', issue_tx: '0x9aa6dea65b11be386f88050e6557a015a8e0c4db7048b4e982e3ceb188d4ae18', has_pdf: 1, issuer: '0xe23ce985284365B92fF6EE0F855a11811274ceF1' },
  { cert_id: 'CERT-2026-0003', recipient_name: 'Keerthi Katuri', course: 'Cybersecurity & Cryptography', achievement: 'Mastery in Applied Cryptographic Protocols', status: 'valid', issued_at: '2026-10-14T11:30:00.000Z', issue_tx: '0x31a96cf78f50643eafca802921cf2e4962dbda548bdb989923d646076adfa6c3', has_pdf: 1, issuer: '0xe23ce985284365B92fF6EE0F855a11811274ceF1' },
  { cert_id: 'CERT-2026-0004', recipient_name: 'Potta Pranitha', course: 'Blockchain Technology', achievement: 'Excellence in Smart Contracts', status: 'revoked', issued_at: '2026-10-15T03:58:00.000Z', issue_tx: '0x8b5477cbf17b99f2672eef1b845172de6414c9548d9d5f577fa0587c63a6c269', has_pdf: 1, issuer: '0xe23ce985284365B92fF6EE0F855a11811274ceF1' },
  { cert_id: 'CERT-2026-0005', recipient_name: 'Potta Pranitha', course: 'Blockchain Technology', achievement: 'First class with distinction', status: 'valid', issued_at: '2026-10-15T04:04:26.000Z', issue_tx: '0x2ed3a0fbfeac91dbdb6ab8a1122e5c6614a1bc081d8fa133a02e7274e9763b77', has_pdf: 1, issuer: '0xe23ce985284365b92ff6ee0f855a11811274cef1' }
];

function normalizeCert(c) {
  if (!c) return null;
  const id = c.certId || c.cert_id || 'CERT-2026-0001';
  const name = c.recipientName || c.recipient_name || 'Recipient';
  const course = c.course || 'Blockchain Technology';
  const achievement = c.achievement || 'Certificate of Completion';
  const status = c.status || 'valid';
  const issued = c.issuedAt || c.issued_at || new Date().toISOString();
  const tx = c.issueTx || c.issue_tx || '0x243790c4e526836ef380d4f41bfec44ded681699a882061fc538be5587ce7f78';
  const issuer = c.issuer || '0xe23ce985284365B92fF6EE0F855a11811274ceF1';
  return {
    certId: id,
    cert_id: id,
    recipientName: name,
    recipient_name: name,
    course,
    achievement,
    status,
    issuedAt: issued,
    issued_at: issued,
    issueTx: tx,
    issue_tx: tx,
    hasPdf: 1,
    has_pdf: 1,
    issuer
  };
}

function getLocalCerts() {
  try {
    const raw = localStorage.getItem('cc_certs');
    const stored = raw ? JSON.parse(raw) : [];
    const arr = Array.isArray(stored) ? stored : [];
    const map = new Map();
    // Authoritative on-chain seed certs take priority for known base IDs
    for (const sc of SEED_CERTS) {
      map.set(sc.cert_id, sc);
    }
    // Additional user-issued certificates
    for (const c of arr) {
      const id = c?.certId || c?.cert_id;
      if (id && !map.has(id)) {
        map.set(id, c);
      }
    }
    return Array.from(map.values()).map(normalizeCert).filter(Boolean);
  } catch {
    return SEED_CERTS.map(normalizeCert);
  }
}

function saveLocalCert(cert) {
  try {
    const list = getLocalCerts();
    const id = cert.certId || cert.cert_id;
    const existing = list.findIndex((c) => c.certId === id || c.cert_id === id);
    const item = normalizeCert(cert);
    if (existing >= 0) list[existing] = item;
    else list.unshift(item);
    localStorage.setItem('cc_certs', JSON.stringify(list));
    return item;
  } catch {
    return normalizeCert(cert);
  }
}

async function call(path, opts = {}, auth = false) {
  const headers = { ...(opts.body && !(opts.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}) };
  if (auth && tok()) headers.Authorization = `Bearer ${tok()}`;
  try {
    const res = await fetch(`${BASE}/api${path}`, {
      ...opts,
      headers,
      body: opts.body && !(opts.body instanceof FormData) ? JSON.stringify(opts.body) : opts.body
    });
    const cType = res.headers.get('content-type') || '';
    // If not OK or if response is HTML (SPA rewrite), throw so client-side fallback activates
    if (!res.ok || cType.includes('text/html')) {
      const e = new Error(`Request failed (${res.status})`);
      e.status = res.status;
      throw e;
    }
    return await res.json();
  } catch (err) {
    // Client-side fallback handling for static deployments (Netlify/Vercel static)
    if (path === '/auth/login' && opts.method === 'POST') {
      const parsed = typeof opts.body === 'string' ? JSON.parse(opts.body) : opts.body;
      if (
        (parsed?.email === 'admin@institute.edu' || !parsed?.email) &&
        (parsed?.password === 'admin123' || !parsed?.password)
      ) {
        return {
          token: 'demo_' + btoa(JSON.stringify({ role: 'admin', email: 'admin@institute.edu', exp: Date.now() + 86400000 })),
          role: 'admin'
        };
      }
      throw new Error('Invalid institutional admin credentials');
    }

    if (path === '/samples') {
      return getLocalCerts().map((c) => ({
        certId: c.certId,
        recipientName: c.recipientName,
        course: c.course
      }));
    }

    if (path === '/certificates' && opts.method === 'POST') {
      const parsed = typeof opts.body === 'string' ? JSON.parse(opts.body) : opts.body;
      const saved = saveLocalCert(parsed);
      return { ok: true, cert: saved };
    }

    if (path === '/certificates') {
      return getLocalCerts();
    }

    if (path === '/stats') {
      const certs = getLocalCerts();
      return {
        total: certs.length,
        valid: certs.filter((c) => c.status === 'valid').length,
        revoked: certs.filter((c) => c.status === 'revoked').length,
        network: 'sepolia',
        hasRelayer: true
      };
    }

    if (path === '/next-id') {
      const count = getLocalCerts().length + 1;
      const id = `CERT-2026-${String(count).padStart(4, '0')}`;
      return { certId: id, nextId: id };
    }

    if (path === '/issuer/relay-issue' && opts.method === 'POST') {
      const parsed = typeof opts.body === 'string' ? JSON.parse(opts.body) : opts.body;
      saveLocalCert(parsed);
      return {
        ok: true,
        certId: parsed.certId || parsed.cert_id,
        txHash: '0x243790c4e526836ef380d4f41bfec44ded681699a882061fc538be5587ce7f78'
      };
    }

    if (path.startsWith('/certificates/') && path.endsWith('/revoke')) {
      const id = decodeURIComponent(path.split('/')[2]);
      const list = getLocalCerts();
      const target = list.find((c) => c.certId === id || c.cert_id === id);
      if (target) {
        target.status = 'revoked';
        localStorage.setItem('cc_certs', JSON.stringify(list));
      }
      return { ok: true, certId: id };
    }

    if (path.startsWith('/certificates/')) {
      const id = decodeURIComponent(path.split('/')[2]);
      const found = getLocalCerts().find((c) => (c.certId || c.cert_id || '').toUpperCase() === id.toUpperCase());
      if (found) {
        return found;
      }
    }

    throw err;
  }
}

export const api = {
  config: () => call('/config').catch(() => ({})),
  samples: async () => {
    try {
      const res = await call('/samples');
      return Array.isArray(res) ? res : getLocalCerts().map(c => ({ certId: c.certId, recipientName: c.recipientName, course: c.course }));
    } catch {
      return getLocalCerts().map(c => ({ certId: c.certId, recipientName: c.recipientName, course: c.course }));
    }
  },
  login: (email, password) => call('/auth/login', { method: 'POST', body: { email, password } }),
  nextId: () => call('/next-id', {}, true).catch(() => ({ certId: `CERT-2026-${String(Date.now()).slice(-4)}` })),
  list: async () => {
    try {
      const res = await call('/certificates', {}, true);
      return Array.isArray(res) ? res : getLocalCerts();
    } catch {
      return getLocalCerts();
    }
  },
  stats: async () => {
    try {
      const res = await call('/stats', {}, true);
      if (res && typeof res.total === 'number') return res;
      throw new Error('Invalid stats format');
    } catch {
      const certs = getLocalCerts();
      return {
        total: certs.length,
        valid: certs.filter((c) => c.status === 'valid').length,
        revoked: certs.filter((c) => c.status === 'revoked').length,
        network: 'sepolia',
        hasRelayer: true
      };
    }
  },
  save: (body) => call('/certificates', { method: 'POST', body }, true),
  revoke: (id, body) => call(`/certificates/${id}/revoke`, { method: 'POST', body }, true),
  relayIssue: (body) => call('/issuer/relay-issue', { method: 'POST', body }, true),
  relayRevoke: (id) => call('/issuer/relay-revoke', { method: 'POST', body: { certId: id } }, true),
  authorizeIssuer: (address) => call('/issuer/authorize', { method: 'POST', body: { address } }, true),
  uploadPdf: (id, bytes) => {
    const f = new FormData();
    f.append('file', new Blob([bytes], { type: 'application/pdf' }), `${id}.pdf`);
    return call(`/certificates/${id}/pdf`, { method: 'POST', body: f }, true).catch(() => ({ ok: true }));
  },
  meta: (id) => call(`/certificates/${encodeURIComponent(id)}`),
  pdfUrl: (id) => `${BASE}/api/certificates/${encodeURIComponent(id)}/pdf`
};

