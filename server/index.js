import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import jwt from 'jsonwebtoken';
import multer from 'multer';
import rateLimit from 'express-rate-limit';
import { DatabaseSync } from 'node:sqlite';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { JsonRpcProvider, Wallet, Contract } from 'ethers';

const { PORT = 4000, JWT_SECRET, ADMIN_EMAIL, ADMIN_PASSWORD, CORS_ORIGIN = 'http://localhost:5173',
  CONTRACT_ADDRESS = '', NETWORK = 'sepolia', RPC_URL = 'https://ethereum-sepolia-rpc.publicnode.com',
  RELAYER_PRIVATE_KEY = '' } = process.env;

if (!JWT_SECRET || !ADMIN_EMAIL || !ADMIN_PASSWORD) {
  console.error('Set JWT_SECRET, ADMIN_EMAIL and ADMIN_PASSWORD in server/.env (see .env.example)');
  process.exit(1);
}

const DATA = path.resolve('data');
fs.mkdirSync(path.join(DATA, 'pdfs'), { recursive: true });
const db = new DatabaseSync(path.join(DATA, 'certchain.db'));
db.exec('PRAGMA journal_mode = WAL');
db.exec(`
CREATE TABLE IF NOT EXISTS certificates(
  cert_id TEXT PRIMARY KEY, recipient_name TEXT NOT NULL, recipient_email TEXT, course TEXT NOT NULL,
  achievement TEXT, template TEXT, doc_hash TEXT NOT NULL, issuer TEXT NOT NULL, network TEXT,
  issue_tx TEXT, revoke_tx TEXT, revoked_by TEXT, status TEXT NOT NULL DEFAULT 'valid',
  issued_at TEXT NOT NULL, revoked_at TEXT, has_pdf INTEGER NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS counters(year INTEGER PRIMARY KEY, n INTEGER NOT NULL);`);

const RE = { id: /^CERT-\d{4}-\d{4,}$/, hash: /^0x[0-9a-fA-F]{64}$/, addr: /^0x[0-9a-fA-F]{40}$/ };
const str = (v, max = 200) => (typeof v === 'string' && v.trim() && v.length <= max ? v.trim() : null);
const sha = (s) => crypto.createHash('sha256').update(s).digest();

const ABI = [
  'function owner() view returns (address)',
  'function isIssuer(address) view returns (bool)',
  'function issuerCount() view returns (uint256)',
  'function totalIssued() view returns (uint256)',
  'function totalRevoked() view returns (uint256)',
  'function addIssuer(address a)',
  'function removeIssuer(address a)',
  'function issue(string certId, bytes32 docHash)',
  'function revoke(string certId)',
  'function verify(string certId, bytes32 docHash) view returns (uint8)',
  'function getCertificate(string certId) view returns (tuple(bytes32 docHash, address issuer, uint64 issuedAt, uint64 revokedAt, address revokedBy, bool exists))'
];

let relayerWallet = null;
let relayerContract = null;
if (RELAYER_PRIVATE_KEY && CONTRACT_ADDRESS) {
  try {
    const provider = new JsonRpcProvider(RPC_URL);
    relayerWallet = new Wallet(RELAYER_PRIVATE_KEY, provider);
    relayerContract = new Contract(CONTRACT_ADDRESS, ABI, relayerWallet);
  } catch (err) {
    console.warn('Relayer wallet initialization skipped:', err.message);
  }
}

const app = express();
const allowedOrigins = (CORS_ORIGIN || '*').split(',').map(s => s.trim());
app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes('*') || allowedOrigins.includes(origin)) {
      return callback(null, true);
    }
    // Allow any Vercel preview/production domains
    if (origin.endsWith('.vercel.app')) {
      return callback(null, true);
    }
    return callback(null, true);
  },
  credentials: true
}));
app.use(express.json({ limit: '100kb' }));
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 5 * 1024 * 1024 } });

function auth(req, res, next) {
  const t = (req.headers.authorization || '').replace('Bearer ', '');
  try { jwt.verify(t, JWT_SECRET); next(); } catch { res.status(401).json({ error: 'Sign in required' }); }
}

app.get('/api/health', (_, res) => res.json({ ok: true }));
app.get('/api/config', (_, res) => res.json({
  contractAddress: CONTRACT_ADDRESS,
  network: NETWORK,
  relayerAddress: relayerWallet ? relayerWallet.address : null,
  hasRelayer: !!relayerContract
}));

// Quick samples for the verification page to make it interactive immediately
app.get('/api/samples', (_, res) => {
  const samples = db.prepare('SELECT cert_id, recipient_name, course, status FROM certificates ORDER BY issued_at DESC LIMIT 5').all();
  res.json(samples.map(s => ({
    certId: s.cert_id,
    recipientName: s.recipient_name,
    course: s.course,
    status: s.status
  })));
});

app.post('/api/auth/login', rateLimit({ windowMs: 15 * 60 * 1000, limit: 30 }), (req, res) => {
  const { email = '', password = '' } = req.body || {};
  const ok = crypto.timingSafeEqual(sha(String(email).toLowerCase()), sha(ADMIN_EMAIL.toLowerCase()))
    & crypto.timingSafeEqual(sha(String(password)), sha(ADMIN_PASSWORD));
  if (!ok) return res.status(401).json({ error: 'Email or password is incorrect' });
  res.json({ token: jwt.sign({ role: 'admin' }, JWT_SECRET, { expiresIn: '8h' }) });
});

// Reserve the next sequential ID: CERT-YYYY-NNNN
app.get('/api/next-id', auth, (_, res) => {
  const year = new Date().getFullYear();
  db.exec('BEGIN IMMEDIATE');
  try {
    db.prepare('INSERT INTO counters(year,n) VALUES(?,0) ON CONFLICT(year) DO NOTHING').run(year);
    db.prepare('UPDATE counters SET n=n+1 WHERE year=?').run(year);
    const n = db.prepare('SELECT n FROM counters WHERE year=?').get(year).n;
    db.exec('COMMIT');
    res.json({ certId: `CERT-${year}-${String(n).padStart(4, '0')}` });
  } catch (err) {
    db.exec('ROLLBACK');
    throw err;
  }
});

// Relayed issuance using the institution's authorized deployer wallet
app.post('/api/issuer/relay-issue', auth, async (req, res) => {
  if (!relayerContract) return res.status(503).json({ error: 'Relayer wallet not configured' });
  const { certId, docHash } = req.body || {};
  if (!certId || !docHash || !RE.id.test(certId) || !RE.hash.test(docHash)) {
    return res.status(400).json({ error: 'Invalid certId or docHash' });
  }
  try {
    const tx = await relayerContract.issue(certId, docHash);
    const receipt = await tx.wait();
    res.json({
      ok: true,
      txHash: tx.hash,
      blockNumber: receipt.blockNumber,
      issuer: relayerWallet.address
    });
  } catch (err) {
    res.status(500).json({ error: err.reason || err.shortMessage || err.message });
  }
});

// Authorize connected wallet as an issuer
app.post('/api/issuer/authorize', auth, async (req, res) => {
  if (!relayerContract) return res.status(503).json({ error: 'Relayer wallet not configured' });
  const { address } = req.body || {};
  if (!RE.addr.test(address || '')) return res.status(400).json({ error: 'Invalid Ethereum address' });
  try {
    const isAlready = await relayerContract.isIssuer(address);
    if (isAlready) return res.json({ ok: true, alreadyIssuer: true, address });
    const tx = await relayerContract.addIssuer(address);
    await tx.wait();
    res.json({ ok: true, txHash: tx.hash, address });
  } catch (err) {
    res.status(500).json({ error: err.reason || err.shortMessage || err.message });
  }
});

// Relayed revocation using institutional authority
app.post('/api/issuer/relay-revoke', auth, async (req, res) => {
  if (!relayerContract) return res.status(503).json({ error: 'Relayer wallet not configured' });
  const { certId } = req.body || {};
  if (!certId || !RE.id.test(certId)) return res.status(400).json({ error: 'Invalid certId' });
  try {
    const tx = await relayerContract.revoke(certId, { gasLimit: 300000 });
    const receipt = await tx.wait();
    db.prepare(`UPDATE certificates SET status='revoked',revoke_tx=?,revoked_by=?,revoked_at=? WHERE cert_id=? AND status='valid'`)
      .run(tx.hash, relayerWallet.address, new Date().toISOString(), certId);
    res.json({ ok: true, txHash: tx.hash, blockNumber: receipt.blockNumber });
  } catch (err) {
    res.status(500).json({ error: err.reason || err.shortMessage || err.message });
  }
});

const adminRow = (r) => ({ certId: r.cert_id, recipientName: r.recipient_name, recipientEmail: r.recipient_email,
  course: r.course, achievement: r.achievement, template: r.template, docHash: r.doc_hash, issuer: r.issuer,
  network: r.network, issueTx: r.issue_tx, revokeTx: r.revoke_tx, revokedBy: r.revoked_by, status: r.status,
  issuedAt: r.issued_at, revokedAt: r.revoked_at, hasPdf: !!r.has_pdf });
// Public view: never exposes the recipient's email
const publicRow = (r) => { const { recipientEmail, ...p } = adminRow(r); return p; };

app.get('/api/certificates', auth, (_, res) =>
  res.json(db.prepare('SELECT * FROM certificates ORDER BY issued_at DESC').all().map(adminRow)));

app.get('/api/stats', auth, (_, res) => res.json(db.prepare(
  `SELECT COUNT(*) total, COALESCE(SUM(status='valid'),0) valid, COALESCE(SUM(status='revoked'),0) revoked FROM certificates`).get()));

app.post('/api/certificates', auth, (req, res) => {
  const b = req.body || {};
  const certId = str(b.certId, 40), name = str(b.recipientName), course = str(b.course);
  if (!certId || !RE.id.test(certId) || !name || !course || !RE.hash.test(b.docHash || '') || !RE.addr.test(b.issuer || '')
    || !RE.hash.test(b.issueTx || '')) return res.status(400).json({ error: 'Missing or invalid certificate fields' });
  try {
    db.prepare(`INSERT INTO certificates(cert_id,recipient_name,recipient_email,course,achievement,template,doc_hash,issuer,network,issue_tx,issued_at)
      VALUES(?,?,?,?,?,?,?,?,?,?,?)`).run(certId, name, str(b.recipientEmail), course, str(b.achievement), str(b.template, 40),
      b.docHash.toLowerCase(), b.issuer, NETWORK, b.issueTx, new Date().toISOString());
    res.status(201).json({ ok: true });
  } catch (e) {
    if ((e.code === 'ERR_SQLITE_ERROR' && e.message?.includes('UNIQUE constraint')) || String(e.code).startsWith('SQLITE_CONSTRAINT')) {
      return res.status(409).json({ error: 'Certificate ID already exists' });
    }
    throw e;
  }
});

app.post('/api/certificates/:id/revoke', auth, (req, res) => {
  const { txHash, revokedBy } = req.body || {};
  if (!RE.hash.test(txHash || '') || !RE.addr.test(revokedBy || '')) return res.status(400).json({ error: 'Invalid revocation data' });
  const r = db.prepare(`UPDATE certificates SET status='revoked',revoke_tx=?,revoked_by=?,revoked_at=? WHERE cert_id=? AND status='valid'`)
    .run(txHash, revokedBy, new Date().toISOString(), req.params.id);
  r.changes ? res.json({ ok: true }) : res.status(404).json({ error: 'Certificate not found or already revoked' });
});

// PDF is stored only if its SHA-256 matches the hash recorded for this certificate
app.post('/api/certificates/:id/pdf', auth, upload.single('file'), (req, res) => {
  const row = db.prepare('SELECT doc_hash FROM certificates WHERE cert_id=?').get(req.params.id);
  if (!row) return res.status(404).json({ error: 'Certificate not found' });
  const buf = req.file?.buffer;
  if (!buf || buf.subarray(0, 4).toString() !== '%PDF') return res.status(400).json({ error: 'A PDF file is required' });
  if ('0x' + crypto.createHash('sha256').update(buf).digest('hex') !== row.doc_hash)
    return res.status(422).json({ error: 'PDF does not match the recorded hash' });
  fs.writeFileSync(path.join(DATA, 'pdfs', `${req.params.id}.pdf`), buf);
  db.prepare('UPDATE certificates SET has_pdf=1 WHERE cert_id=?').run(req.params.id);
  res.json({ ok: true });
});

// Public endpoints (certificate metadata and PDF, used by the verification page)
app.get('/api/certificates/:id', (req, res) => {
  const r = db.prepare('SELECT * FROM certificates WHERE cert_id=?').get(req.params.id);
  r ? res.json(publicRow(r)) : res.status(404).json({ error: 'Not found' });
});
app.get('/api/certificates/:id/pdf', (req, res) => {
  const r = db.prepare('SELECT has_pdf FROM certificates WHERE cert_id=?').get(req.params.id);
  if (!r?.has_pdf) return res.status(404).json({ error: 'No PDF stored' });
  res.type('application/pdf').sendFile(path.join(DATA, 'pdfs', `${req.params.id}.pdf`));
// Static serving for unified production deployment (Render / Single VPS)
const distPath = path.resolve('../frontend/dist');
if (fs.existsSync(distPath)) {
  app.use(express.static(distPath));
  app.get('*', (req, res, next) => {
    if (req.path.startsWith('/api')) return next();
    res.sendFile(path.join(distPath, 'index.html'));
  });
}

app.use((err, _req, res, _next) => { console.error(err); res.status(500).json({ error: 'Server error' }); });
app.listen(PORT, () => console.log(`CertChain API on http://localhost:${PORT}`));
