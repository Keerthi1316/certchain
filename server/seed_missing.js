import { JsonRpcProvider, Wallet, Contract } from 'ethers';
import { jsPDF } from 'jspdf';
import QRCode from 'qrcode';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';

const RPC_URL = 'https://ethereum-sepolia-rpc.publicnode.com';
const CONTRACT_ADDRESS = '0xba0553a92F82F62E62d38496398637f9CB11B37C';
const RELAYER_PRIVATE_KEY = '483ea0095c8df6fd81f5031b85323096efda2316c61d0082ffddff2d3d3c8869';

const provider = new JsonRpcProvider(RPC_URL);
const wallet = new Wallet(RELAYER_PRIVATE_KEY, provider);

const ABI = [
  'function issue(string certId, bytes32 docHash) external',
  'function getCertificate(string certId) view returns (tuple(bytes32 docHash, address issuer, uint64 issuedAt, uint64 revokedAt, address revokedBy, bool exists))'
];

const contract = new Contract(CONTRACT_ADDRESS, ABI, wallet);

const DATA = path.resolve('data');
fs.mkdirSync(path.join(DATA, 'pdfs'), { recursive: true });
const db = new DatabaseSync(path.join(DATA, 'certchain.db'));

async function makePdf({ certId, name, course, achievement, issued, issuer }) {
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
  const achSize = achievement.length > 25 ? 24 : achievement.length > 15 ? 30 : 36;
  doc.setTextColor(185, 180, 255); doc.setFontSize(achSize);
  doc.text(achievement.toUpperCase(), W / 2, 195, { align: 'center', maxWidth: W - 160 });
  doc.setTextColor(154, 160, 200); doc.setFontSize(10);
  doc.text('PROUDLY PRESENTED TO', W / 2, 252, { align: 'center', charSpace: 4 });
  doc.setTextColor(238, 240, 255); doc.setFontSize(34);
  doc.text(name, W / 2, 302, { align: 'center', maxWidth: W - 160 });
  doc.setFont('helvetica', 'normal'); doc.setTextColor(154, 160, 200); doc.setFontSize(14);
  doc.text('for successfully completing', W / 2, 340, { align: 'center' });
  doc.setFont('helvetica', 'bold'); doc.setTextColor(238, 240, 255); doc.setFontSize(18);
  doc.text(course, W / 2, 368, { align: 'center', maxWidth: W - 160 });

  const row = (label, val, x, mono) => {
    doc.setFont('helvetica', 'normal'); doc.setFontSize(8); doc.setTextColor(154, 160, 200); doc.text(String(label), x, 470, { charSpace: 2 });
    doc.setFont(mono ? 'courier' : 'helvetica', 'bold'); doc.setFontSize(11);
    mono ? doc.setTextColor(51, 214, 255) : doc.setTextColor(238, 240, 255);
    doc.text(String(val), x, 488);
  };
  row('ISSUED', issued, 66);
  row('CERTIFICATE ID', certId, 220, true);
  row('ISSUER', issuer, 390, true);

  const qr = await QRCode.toDataURL(`http://localhost:5173/verify/${certId}`, { margin: 1, width: 280 });
  doc.addImage(qr, 'PNG', W - 160, H - 170, 90, 90);
  doc.setFont('helvetica', 'normal'); doc.setFontSize(7); doc.setTextColor(154, 160, 200);
  doc.text('SCAN TO VERIFY', W - 115, H - 68, { align: 'center', charSpace: 2 });

  return Buffer.from(doc.output('arraybuffer'));
}

async function issueCert({ certId, name, email, course, achievement }) {
  console.log(`Checking ${certId}...`);
  const existing = await contract.getCertificate(certId);
  if (existing.exists) {
    console.log(`${certId} already exists on chain!`);
    return;
  }

  const issued = '14 October 2026';
  const issuerDisplay = '0xe23ce9…ceF1 (Inst. Authority)';
  const buf = await makePdf({ certId, name, course, achievement, issued, issuer: issuerDisplay });
  const hash = '0x' + crypto.createHash('sha256').update(buf).digest('hex');

  console.log(`Issuing ${certId} with hash ${hash} to Sepolia...`);
  const tx = await contract.issue(certId, hash);
  console.log(`Tx submitted: ${tx.hash}, waiting for confirmation...`);
  const rc = await tx.wait();
  console.log(`Confirmed in block ${rc.blockNumber}!`);

  // Save PDF
  fs.writeFileSync(path.join(DATA, 'pdfs', `${certId}.pdf`), buf);

  // Insert to DB
  try {
    db.prepare(`INSERT INTO certificates(cert_id, recipient_name, recipient_email, course, achievement, template, doc_hash, issuer, network, issue_tx, status, issued_at, has_pdf)
      VALUES(?, ?, ?, ?, ?, 'premium', ?, ?, 'sepolia', ?, 'valid', ?, 1)
      ON CONFLICT(cert_id) DO UPDATE SET recipient_name=excluded.recipient_name, course=excluded.course, achievement=excluded.achievement, doc_hash=excluded.doc_hash, issue_tx=excluded.issue_tx, has_pdf=1`)
      .run(certId, name, email, course, achievement, hash, wallet.address, tx.hash, new Date().toISOString());
    console.log(`Inserted ${certId} into SQLite!`);
  } catch (e) {
    console.error(`DB error for ${certId}:`, e.message);
  }
}

async function main() {
  await issueCert({
    certId: 'CERT-2026-0002',
    name: 'Keerthi Katuri',
    email: 'keerthi@example.com',
    course: 'Artificial Intelligence & Machine Learning',
    achievement: 'Excellence in Deep Learning & Neural Models'
  });

  await issueCert({
    certId: 'CERT-2026-0003',
    name: 'Keerthi Katuri',
    email: 'keerthi@example.com',
    course: 'Cybersecurity & Cryptography',
    achievement: 'Mastery in Applied Cryptographic Protocols'
  });

  console.log('Finished issuing missing certificates on chain!');
}

main().catch(console.error);
