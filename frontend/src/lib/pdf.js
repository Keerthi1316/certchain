import { jsPDF } from 'jspdf';
import QRCode from 'qrcode';

export const verifyUrl = (id) => `${location.origin}/verify/${id}`;
export const qrDataUrl = (text, light = '#ffffff') =>
  QRCode.toDataURL(text, { margin: 1, width: 280, errorCorrectionLevel: 'M', color: { dark: '#050511', light } });

export async function sha256Hex(bytes) {
  const h = await crypto.subtle.digest('SHA-256', bytes);
  return '0x' + [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/** Builds the certificate PDF. The bytes returned are exactly what gets hashed and stored. */
export async function makeCertificatePdf({ certId, name, course, achievement, issued, issuer }) {
  const W = 842, H = 595;
  const safeCertId = String(certId || 'CERT-2026-0001');
  const safeName = String(name || 'Recipient');
  const safeCourse = String(course || 'Blockchain Technology');
  const safeAchievement = String(achievement || 'Certificate of Completion');
  const safeIssued = String(issued || new Date().toISOString().slice(0, 10));
  const safeIssuer = String(issuer || '0xe23ce9…ceF1 (Inst. Authority)');

  const doc = new jsPDF({ orientation: 'landscape', unit: 'pt', format: 'a4' });
  doc.setProperties({ title: `${safeCertId} — ${safeName}`, creator: 'CERTCHAIN' });
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
  const achSize = safeAchievement.length > 25 ? 24 : safeAchievement.length > 15 ? 30 : 36;
  doc.setTextColor(185, 180, 255); doc.setFontSize(achSize);
  doc.text(safeAchievement.toUpperCase(), W / 2, 195, { align: 'center', maxWidth: W - 160 });
  doc.setTextColor(154, 160, 200); doc.setFontSize(10);
  doc.text('PROUDLY PRESENTED TO', W / 2, 252, { align: 'center', charSpace: 4 });
  doc.setTextColor(238, 240, 255); doc.setFontSize(34);
  doc.text(safeName, W / 2, 302, { align: 'center', maxWidth: W - 160 });
  doc.setFont('helvetica', 'normal'); doc.setTextColor(154, 160, 200); doc.setFontSize(14);
  doc.text('for successfully completing', W / 2, 340, { align: 'center' });
  doc.setFont('helvetica', 'bold'); doc.setTextColor(238, 240, 255); doc.setFontSize(18);
  doc.text(safeCourse, W / 2, 368, { align: 'center', maxWidth: W - 160 });

  const row = (label, val, x, mono) => {
    const textVal = String(val ?? '');
    doc.setFont('helvetica', 'normal'); doc.setFontSize(8); doc.setTextColor(154, 160, 200); doc.text(String(label), x, 470, { charSpace: 2 });
    doc.setFont(mono ? 'courier' : 'helvetica', 'bold'); doc.setFontSize(11);
    mono ? doc.setTextColor(51, 214, 255) : doc.setTextColor(238, 240, 255);
    doc.text(textVal, x, 488);
  };
  row('ISSUED', safeIssued, 66);
  row('CERTIFICATE ID', safeCertId, 220, true);
  row('ISSUER', safeIssuer, 390, true);
  doc.addImage(await qrDataUrl(verifyUrl(safeCertId)), 'PNG', W - 160, H - 170, 90, 90);
  doc.setFont('helvetica', 'normal'); doc.setFontSize(7); doc.setTextColor(154, 160, 200);
  doc.text('SCAN TO VERIFY', W - 115, H - 68, { align: 'center', charSpace: 2 });
  return new Uint8Array(doc.output('arraybuffer'));
}

/** Obtains the PDF bytes either by fetching the stored file or generating on the fly */
export async function getPdfBlob(cert) {
  const certId = cert?.certId || cert?.cert_id || 'CERT-2026-0001';
  try {
    const res = await fetch(`/api/certificates/${encodeURIComponent(certId)}/pdf`);
    const cType = res.headers.get('content-type') || '';
    if (res.ok && cType.includes('application/pdf')) {
      return await res.blob();
    }
  } catch {}

  // Generate client-side vector PDF fallback
  const bytes = await makeCertificatePdf({
    certId,
    name: cert?.recipientName || cert?.recipient_name || 'Keerthi Katuri',
    course: cert?.course || 'Blockchain Technology',
    achievement: cert?.achievement || 'Excellence in Smart Contract Verification',
    issued: cert?.issuedAt || cert?.issued_at || '14 October 2026',
    issuer: cert?.issuer || '0xe23ce9…ceF1 (Inst. Authority)'
  });
  return new Blob([bytes], { type: 'application/pdf' });
}

export async function downloadCertificatePdf(cert) {
  const certId = cert?.certId || cert?.cert_id || 'CERT-2026-0001';
  const blob = await getPdfBlob(cert);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${certId}.pdf`;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 2000);
}

export async function openCertificatePdf(cert) {
  const blob = await getPdfBlob(cert);
  const url = URL.createObjectURL(blob);
  window.open(url, '_blank');
}

