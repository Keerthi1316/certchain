const BASE = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '');
const tok = () => localStorage.getItem('cc_token');

async function call(path, opts = {}, auth = false) {
  const headers = { ...(opts.body && !(opts.body instanceof FormData) ? { 'Content-Type': 'application/json' } : {}) };
  if (auth && tok()) headers.Authorization = `Bearer ${tok()}`;
  const res = await fetch(`${BASE}/api${path}`, { ...opts, headers,
    body: opts.body && !(opts.body instanceof FormData) ? JSON.stringify(opts.body) : opts.body });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) { const e = new Error(data.error || `Request failed (${res.status})`); e.status = res.status; throw e; }
  return data;
}

export const api = {
  config: () => call('/config'),
  samples: () => call('/samples'),
  login: (email, password) => call('/auth/login', { method: 'POST', body: { email, password } }),
  nextId: () => call('/next-id', {}, true),
  list: () => call('/certificates', {}, true),
  stats: () => call('/stats', {}, true),
  save: (body) => call('/certificates', { method: 'POST', body }, true),
  revoke: (id, body) => call(`/certificates/${id}/revoke`, { method: 'POST', body }, true),
  relayIssue: (body) => call('/issuer/relay-issue', { method: 'POST', body }, true),
  relayRevoke: (id) => call('/issuer/relay-revoke', { method: 'POST', body: { certId: id } }, true),
  authorizeIssuer: (address) => call('/issuer/authorize', { method: 'POST', body: { address } }, true),
  uploadPdf: (id, bytes) => {
    const f = new FormData(); f.append('file', new Blob([bytes], { type: 'application/pdf' }), `${id}.pdf`);
    return call(`/certificates/${id}/pdf`, { method: 'POST', body: f }, true);
  },
  meta: (id) => call(`/certificates/${encodeURIComponent(id)}`),
  pdfUrl: (id) => `${BASE}/api/certificates/${encodeURIComponent(id)}/pdf`,
};
