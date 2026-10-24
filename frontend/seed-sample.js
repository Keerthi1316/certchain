import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';
import { JsonRpcProvider, Wallet, Contract } from 'ethers';
import { DatabaseSync } from 'node:sqlite';
import { jsPDF } from 'jspdf';
import QRCode from 'qrcode';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const SEPOLIA_RPC = 'https://ethereum-sepolia-rpc.publicnode.com';
const CONTRACT_ADDRESS = '0xba0553a92F82F62E62d38496398637f9CB11B37C';
const PRIVATE_KEY = '483ea0095c8df6fd81f5031b85323096efda2316c61d0082ffddff2d3d3c8869';

const ABI = [
  'function issue(string certId, bytes32 docHash)',
  'function verify(string certId, bytes32 docHash) view returns (uint8)',
  'function totalIssued() view returns (uint256)'
];

async function seed() {
  console.log('Generating seed certificate PDF...');
  const certId = 'CERT-2026-0001';
  const name = 'Keerthi Katuri';
  const course = 'Blockchain Technology';
  const achievement = 'Excellence in Smart Contract Verification';
  const issued = 'October 14, 2026';
  const issuer = '0xe23ce9…ceF1';

  const W = 842, H = 595;
  const doc = new jsPDF({ orientation: 'landscape', unit: 'pt', format: 'a4' });
  doc.setProperties({ title: `${certId} — ${name}`, creator: 'CERTCHAIN' });
  doc.setFillColor(8, 9, 26); doc.rect(0, 0, W, H, 'F');
  doc.setFillColor(40, 30, 90); doc.circle(W, 0, 220, 'F');
  doc.setFillColor(8, 9, 26); doc.circle(W, 0, 200, 'F');
  doc.setDrawColor(139, 92, 246); doc.setLineWidth(1.4); doc.roundedRect(26, 26, W - 52, H - 52, 14, 14);
  doc.setDrawColor(70, 80, 160); doc.setLineWidth(.5); doc.roundedRect(38, 38, W - 76, H - 76, 10, 10);

  doc.setFont('helvetica', 'bold'); doc.setTextColor(51, 214, 255); doc.setFontSize(12);
  doc.text('INSTITUTE OF TECHNOLOGY', 66, 78, { charSpace: 3 });
  doc.setTextColor(52, 229, 160); doc.setFontSize(9);
  doc.text('BLOCKCHAIN VERIFIED', W - 66, 78, { align: 'right', charSpace: 2 });

  doc.setTextColor(154, 160, 200); doc.setFontSize(10);
  doc.text('CERTIFICATE OF', W / 2, 150, { align: 'center', charSpace: 4 });
  doc.setTextColor(185, 180, 255); doc.setFontSize(40);
  doc.text(achievement.toUpperCase(), W / 2, 200, { align: 'center', maxWidth: W - 160 });
  doc.setTextColor(154, 160, 200); doc.setFontSize(10);
  doc.text('PROUDLY PRESENTED TO', W / 2, 252, { align: 'center', charSpace: 4 });
  doc.setTextColor(238, 240, 255); doc.setFontSize(34);
  doc.text(name, W / 2, 302, { align: 'center', maxWidth: W - 160 });
  doc.setFont('helvetica', 'normal'); doc.setTextColor(154, 160, 200); doc.setFontSize(14);
  doc.text('for successfully completing', W / 2, 340, { align: 'center' });
  doc.setFont('helvetica', 'bold'); doc.setTextColor(238, 240, 255); doc.setFontSize(18);
  doc.text(course, W / 2, 368, { align: 'center', maxWidth: W - 160 });

  const row = (label, val, x, mono) => {
    doc.setFont('helvetica', 'normal'); doc.setFontSize(8); doc.setTextColor(154, 160, 200); doc.text(label, x, 470, { charSpace: 2 });
    doc.setFont(mono ? 'courier' : 'helvetica', 'bold'); doc.setFontSize(11);
    mono ? doc.setTextColor(51, 214, 255) : doc.setTextColor(238, 240, 255); doc.text(val, x, 488);
  };
  row('ISSUED', issued, 66); row('CERTIFICATE ID', certId, 220, true); row('ISSUER', issuer, 390, true);

  const qrUrl = `http://localhost:5173/verify/${certId}`;
  const qrData = await QRCode.toDataURL(qrUrl, { margin: 1, width: 280, errorCorrectionLevel: 'M', color: { dark: '#050511', light: '#ffffff' } });
  doc.addImage(qrData, 'PNG', W - 160, H - 170, 90, 90);
  doc.setFont('helvetica', 'normal'); doc.setFontSize(7); doc.setTextColor(154, 160, 200);
  doc.text('SCAN TO VERIFY', W - 115, H - 68, { align: 'center', charSpace: 2 });

  const pdfBytes = Buffer.from(doc.output('arraybuffer'));
  const docHash = '0x' + crypto.createHash('sha256').update(pdfBytes).digest('hex');
  console.log('PDF bytes length:', pdfBytes.length);
  console.log('SHA-256 hash:', docHash);

  console.log('Submitting issue transaction to Sepolia...');
  const provider = new JsonRpcProvider(SEPOLIA_RPC);
  const wallet = new Wallet(PRIVATE_KEY, provider);
  const contract = new Contract(CONTRACT_ADDRESS, ABI, wallet);

  // Check if already issued
  const status = await contract.verify(certId, docHash);
  let txHash = '0x0';
  if (Number(status) === 1) {
    console.log('Already issued on Sepolia!');
  } else {
    const tx = await contract.issue(certId, docHash, { gasLimit: 650000 });
    console.log('Tx sent:', tx.hash);
    await tx.wait();
    txHash = tx.hash;
    console.log('Mined on Sepolia!');
  }

  // Update SQLite database
  const dataDir = path.resolve(__dirname, '../server/data');
  fs.mkdirSync(path.join(dataDir, 'pdfs'), { recursive: true });
  fs.writeFileSync(path.join(dataDir, 'pdfs', `${certId}.pdf`), pdfBytes);

  const db = new DatabaseSync(path.join(dataDir, 'certchain.db'));
  db.exec(`
  CREATE TABLE IF NOT EXISTS certificates(
    cert_id TEXT PRIMARY KEY, recipient_name TEXT NOT NULL, recipient_email TEXT, course TEXT NOT NULL,
    achievement TEXT, template TEXT, doc_hash TEXT NOT NULL, issuer TEXT NOT NULL, network TEXT,
    issue_tx TEXT, revoke_tx TEXT, revoked_by TEXT, status TEXT NOT NULL DEFAULT 'valid',
    issued_at TEXT NOT NULL, revoked_at TEXT, has_pdf INTEGER NOT NULL DEFAULT 0);
  CREATE TABLE IF NOT EXISTS counters(year INTEGER PRIMARY KEY, n INTEGER NOT NULL);`);

  db.prepare(`INSERT INTO certificates(cert_id,recipient_name,recipient_email,course,achievement,template,doc_hash,issuer,network,issue_tx,issued_at,has_pdf)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,1)
    ON CONFLICT(cert_id) DO UPDATE SET doc_hash=excluded.doc_hash, issue_tx=excluded.issue_tx, has_pdf=1`)
    .run(certId, name, 'keerthi@example.com', course, achievement, 'premium', docHash.toLowerCase(), wallet.address, 'sepolia', txHash, new Date().toISOString());

  db.prepare('INSERT INTO counters(year,n) VALUES(2026,1) ON CONFLICT(year) DO UPDATE SET n=MAX(n,1)').run();

  console.log('Seed certificate CERT-2026-0001 saved to Sepolia and SQLite successfully!');
}

seed().catch(console.error);
