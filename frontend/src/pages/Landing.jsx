import { Link } from 'react-router-dom';
import { QR } from '../components/Certificate.jsx';
import { CONTRACT_ADDRESS, ETHERSCAN, short } from '../lib/chain.js';

const NODES = ['Academic Certificate', 'SHA-256 Digest', 'Smart Contract', 'Sepolia Block', 'Zero-Knowledge Proof'];
const STEPS = [
  ['Details & Template', 'Enter recipient, degree program, and achievement details.'],
  ['Deterministic PDF', 'Vector PDF generated with embedded QR verification code.'],
  ['Cryptographic Fingerprint', 'Raw bytes hashed with SHA-256 in browser/server.'],
  ['Ethereum Sepolia Block', 'Immutable transaction permanently anchored on-chain.'],
  ['Instant Verification', 'Anyone globally can verify status directly from RPC.']
];

export default function Landing() {
  const currentOrigin = typeof window !== 'undefined' ? window.location.origin : 'http://localhost:5173';
  const sampleUrl = `${currentOrigin}/verify/CERT-2026-0001`;

  return (
    <main>
      <section className="hero">
        <div>
          <div className="rays" />
          <div className="eyebrow">Cryptographic Trust • Ethereum Sepolia</div>
          <h1 className="display">
            Certificates.<br />
            <span className="grad-text">Verified</span><br />
            On-Chain.
          </h1>
          <p className="lead">
            Eliminate credential fraud forever. Issue tamper-proof academic credentials anchored directly on the Ethereum blockchain with SHA-256 document hashing.
          </p>
          <div className="cta">
            <Link className="btn action" to="/verify/CERT-2026-0001">
              Verify Sample Certificate →
            </Link>
            <Link className="btn ghost" to="/admin/issue">
              Issue Credential ✍
            </Link>
          </div>
          <div className="wrap" style={{ marginTop: 28, alignItems: 'center' }}>
            <span className="pill ok"><span className="dot" />Ethereum Sepolia Live</span>
            <span className="pill info">SHA-256 Cryptography</span>
            <a
              className="pill info mono"
              href={`${ETHERSCAN}/address/${CONTRACT_ADDRESS}`}
              target="_blank"
              rel="noreferrer"
              style={{ textDecoration: 'none' }}
              title="View Smart Contract on Sepolia Etherscan"
            >
              Contract: {short(CONTRACT_ADDRESS, 6, 4)} ↗
            </a>
          </div>
        </div>

        <div className="stage" style={{ cursor: 'pointer' }}>
          <div className="orbit" />
          <span className="frag f1">0x5E9…EE9</span>
          <span className="frag f2">Sepolia #11914754</span>
          <span className="frag f3">✓ Validated</span>

          <Link to="/verify/CERT-2026-0001" style={{ textDecoration: 'none', display: 'block', width: '100%' }}>
            <article className="cert hero-qr">
              <small>CERTCHAIN • Institute of Technology</small>
              <h3>Certificate of<br />Excellence</h3>
              <div className="who">Keerthi Katuri</div>
              <small>Blockchain Technology</small>
              <div className="row">
                <div>
                  <small>CERT-2026-0001</small>
                  <span className="pill ok" style={{ marginTop: 8 }}>✓ Sepolia Verified</span>
                </div>
                <QR text={sampleUrl} />
              </div>
            </article>
          </Link>
        </div>
      </section>

      <section>
        <div className="eyebrow">Cryptographic Protocol</div>
        <h2 className="h2">Zero Trust.<br />Mathematical Proof.</h2>
        <div className="glass demo">
          <div className="chain">
            {NODES.flatMap((n, i) => [
              i ? <div key={'l' + i} className="line" /> : null,
              <div key={n} className="node">{n}</div>
            ])}
          </div>
          <div className="grid">
            {STEPS.map(([t, d], i) => (
              <div key={t} className="glass lift step">
                <i>STEP 0{i + 1}</i>
                <h4>{t}</h4>
                <p>{d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section>
        <div className="glass" style={{ padding: 48, textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
          <div className="eyebrow" style={{ marginBottom: 12 }}>Next-Gen Institutional Credentialing</div>
          <h2 className="h2" style={{ maxWidth: 640, margin: '0 auto 20px' }}>
            Permanent, verifiable <span className="grad-text">academic records.</span>
          </h2>
          <p className="lead" style={{ margin: '0 auto 30px' }}>
            Empower employers and evaluators to authenticate degrees and awards in milliseconds without intermediaries.
          </p>
          <div className="wrap" style={{ justifyContent: 'center', gap: 14 }}>
            <Link className="btn action" to="/verify">
              Launch Verification Engine →
            </Link>
            <Link className="btn ghost" to="/login">
              Institutional Admin Portal
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
