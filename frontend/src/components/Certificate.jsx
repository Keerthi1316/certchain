import { useEffect, useState } from 'react';
import { qrDataUrl, verifyUrl } from '../lib/pdf.js';

export function QR({ text }) {
  const [src, setSrc] = useState('');
  useEffect(() => { qrDataUrl(text).then(setSrc).catch(() => {}); }, [text]);
  return <div className="qr">{src && <img src={src} alt={`QR code linking to ${text}`} style={{ width: '100%', height: '100%', display: 'block' }} />}</div>;
}

export default function Certificate({ tpl = 'premium', name, course, achievement, certId, issued, issuer }) {
  return (
    <div className="certwrap"><div className="cert2" data-tpl={tpl}>
      <div className="c2-pat" />
      <div className="c2-in">
        <div className="c2-top">
          <div className="c2-logo"><svg width="1.6em" height="1.6em" viewBox="0 0 32 32" fill="none"><rect x="3" y="3" width="11" height="11" rx="3" stroke="currentColor" strokeWidth="2" /><rect x="18" y="18" width="11" height="11" rx="3" stroke="currentColor" strokeWidth="2" /><path d="M14 8h6a3 3 0 013 3v7M9 14v6a3 3 0 003 3h6" stroke="currentColor" strokeWidth="2" /></svg><span>Institute of Technology</span></div>
          <span className="c2-seal">✓ Blockchain verified</span>
        </div>
        <div className="c2-mid">
          <small>Certificate of</small><h3>{achievement || '—'}</h3>
          <small>Proudly presented to</small><div className="c2-name">{name || '—'}</div>
          <p>for successfully completing <b>{course || '—'}</b></p>
        </div>
        <div className="c2-bot">
          <div><small>Issued</small><b>{issued}</b></div>
          <div><small>Certificate ID</small><b className="mono">{certId}</b></div>
          <div><small>Issuer</small><b className="mono">{issuer}</b></div>
          <div className="c2-qr"><QR text={verifyUrl(certId)} /><small>Scan to verify</small></div>
        </div>
      </div>
    </div></div>
  );
}
