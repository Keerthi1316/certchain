import { useEffect, useRef, useState } from 'react';
import { Html5Qrcode } from 'html5-qrcode';

export function parseQrResult(text) {
  if (!text) return '';
  const trimmed = text.trim();
  // Match /verify/<id> in URL or path
  const match = trimmed.match(/\/verify\/([A-Za-z0-9-_]+)/i);
  if (match) return match[1].toUpperCase();
  // Match standard CERT-XXXX-XXXX format anywhere in text
  const certMatch = trimmed.match(/(CERT-[A-Za-z0-9-]+)/i);
  if (certMatch) return certMatch[1].toUpperCase();
  return trimmed;
}

export default function QrScannerModal({ isOpen, onClose, onScanSuccess }) {
  const [tab, setTab] = useState('camera'); // 'camera' | 'file'
  const [cameraError, setCameraError] = useState('');
  const [scanning, setScanning] = useState(false);
  const [processingFile, setProcessingFile] = useState(false);
  const [fileError, setFileError] = useState('');
  const scannerRef = useRef(null);
  const containerId = 'interactive-qr-reader';
  const fileInputRef = useRef(null);

  // Close on Escape key
  useEffect(() => {
    if (!isOpen) return;
    const handleKey = (e) => e.key === 'Escape' && handleClose();
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [isOpen]);

  const stopScanner = async () => {
    if (scannerRef.current) {
      try {
        if (scannerRef.current.isScanning) {
          await scannerRef.current.stop();
        }
        scannerRef.current.clear();
      } catch (err) {
        console.warn('Error stopping scanner:', err);
      } finally {
        scannerRef.current = null;
        setScanning(false);
      }
    }
  };

  const handleClose = async () => {
    await stopScanner();
    onClose();
  };

  const handleSuccess = async (decodedText) => {
    const certId = parseQrResult(decodedText);
    await stopScanner();
    onScanSuccess(certId);
  };

  // Start Camera
  useEffect(() => {
    if (!isOpen || tab !== 'camera') {
      stopScanner();
      return;
    }

    let isMounted = true;
    setCameraError('');

    const startCamera = async () => {
      try {
        await stopScanner();
        if (!isMounted) return;

        const scanner = new Html5Qrcode(containerId);
        scannerRef.current = scanner;

        await scanner.start(
          { facingMode: 'environment' },
          {
            fps: 10,
            qrbox: { width: 260, height: 260 },
            aspectRatio: 1.0
          },
          (decodedText) => {
            if (isMounted) handleSuccess(decodedText);
          },
          () => {
            // Frame parse error ignored
          }
        );

        if (isMounted) setScanning(true);
      } catch (err) {
        console.error('Camera start error:', err);
        if (isMounted) {
          setScanning(false);
          setCameraError(
            err?.name === 'NotAllowedError'
              ? 'Camera permission denied. Please allow camera access in your browser settings or use the Upload Image tab.'
              : 'Unable to start camera. You can upload an image or certificate containing the QR code instead.'
          );
        }
      }
    };

    const timer = setTimeout(startCamera, 150);
    return () => {
      isMounted = false;
      clearTimeout(timer);
      stopScanner();
    };
  }, [isOpen, tab]);

  // Handle Image File
  const handleImageFile = async (file) => {
    if (!file) return;
    setProcessingFile(true);
    setFileError('');
    try {
      // Create temporary scanner instance for file analysis
      const fileScanner = new Html5Qrcode('qr-file-dummy');
      const decodedText = await fileScanner.scanFile(file, false);
      fileScanner.clear();
      handleSuccess(decodedText);
    } catch (err) {
      console.warn('Image decode error:', err);
      setFileError('No valid QR code could be detected in this image. Please ensure the QR code is clearly visible and unblurred.');
    } finally {
      setProcessingFile(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="overlay"
      onMouseDown={(e) => e.target === e.currentTarget && handleClose()}
      style={{ zIndex: 9999 }}
    >
      <div
        className="glass vcard"
        style={{
          maxWidth: 520,
          width: '100%',
          padding: '28px 24px',
          textAlign: 'center',
          position: 'relative'
        }}
        role="dialog"
        aria-modal="true"
        aria-labelledby="qr-modal-title"
      >
        <button
          onClick={handleClose}
          style={{
            position: 'absolute',
            top: 16,
            right: 18,
            background: 'none',
            border: 'none',
            color: 'var(--muted)',
            fontSize: '1.4rem',
            cursor: 'pointer',
            lineHeight: 1
          }}
          title="Close Scanner"
        >
          ✕
        </button>

        <div className="eyebrow" style={{ color: 'var(--cyan)' }}>Fast-Track Authentication</div>
        <h3 id="qr-modal-title" className="vt" style={{ marginTop: 6, marginBottom: 16, fontSize: '1.45rem' }}>
          Scan to Verify
        </h3>

        {/* Tab switcher */}
        <div
          style={{
            display: 'flex',
            gap: 6,
            background: 'rgba(5, 5, 17, 0.6)',
            padding: 4,
            borderRadius: 12,
            marginBottom: 20,
            border: '1px solid rgba(185, 180, 255, 0.15)'
          }}
        >
          <button
            type="button"
            className={`btn sm ${tab === 'camera' ? 'action' : 'ghost'}`}
            style={{ flex: 1, padding: '8px 12px', fontSize: '.84rem' }}
            onClick={() => setTab('camera')}
          >
            📷 Live Camera
          </button>
          <button
            type="button"
            className={`btn sm ${tab === 'file' ? 'action' : 'ghost'}`}
            style={{ flex: 1, padding: '8px 12px', fontSize: '.84rem' }}
            onClick={() => setTab('file')}
          >
            🖼 Upload QR Image
          </button>
        </div>

        {/* Hidden dummy node for file scanning */}
        <div id="qr-file-dummy" style={{ display: 'none' }} />

        {/* CAMERA MODE */}
        {tab === 'camera' && (
          <div>
            <div
              style={{
                position: 'relative',
                borderRadius: 16,
                overflow: 'hidden',
                background: '#04040d',
                border: '1px solid rgba(51, 214, 255, 0.25)',
                minHeight: 280,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            >
              <div id={containerId} style={{ width: '100%', minHeight: 280 }} />

              {cameraError && (
                <div style={{ padding: '24px 16px', color: 'var(--text)' }}>
                  <div style={{ fontSize: '2rem', marginBottom: 8 }}>📷⚠️</div>
                  <strong style={{ color: 'var(--bad)', display: 'block', marginBottom: 8 }}>
                    Camera Unavailable
                  </strong>
                  <p style={{ fontSize: '.84rem', color: 'var(--muted)', maxWidth: 360, margin: '0 auto 16px' }}>
                    {cameraError}
                  </p>
                  <button
                    className="btn ghost sm"
                    onClick={() => setTab('file')}
                    style={{ fontSize: '.82rem' }}
                  >
                    Switch to Upload Image Tab →
                  </button>
                </div>
              )}

              {scanning && !cameraError && (
                <div
                  style={{
                    position: 'absolute',
                    top: 12,
                    left: 12,
                    background: 'rgba(5, 5, 17, 0.75)',
                    padding: '4px 10px',
                    borderRadius: 20,
                    fontSize: '.72rem',
                    color: 'var(--cyan)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    border: '1px solid rgba(51, 214, 255, 0.3)',
                    pointerEvents: 'none'
                  }}
                >
                  <span className="dot" style={{ background: 'var(--cyan)' }} />
                  Align QR code within target frame
                </div>
              )}
            </div>

            <p style={{ fontSize: '.78rem', color: 'var(--muted)', marginTop: 14 }}>
              Point your camera at the QR code printed on any CertChain certificate or screen.
            </p>
          </div>
        )}

        {/* FILE / IMAGE DROP MODE */}
        {tab === 'file' && (
          <div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              style={{ display: 'none' }}
              onChange={(e) => handleImageFile(e.target.files[0])}
            />

            <div
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault();
                const dropped = e.dataTransfer.files[0];
                if (dropped) handleImageFile(dropped);
              }}
              style={{
                border: '2px dashed rgba(51, 214, 255, 0.4)',
                borderRadius: 16,
                padding: '36px 16px',
                textAlign: 'center',
                cursor: 'pointer',
                background: 'rgba(51, 214, 255, 0.04)',
                transition: '.2s'
              }}
            >
              <div style={{ fontSize: '2.5rem', marginBottom: 8 }}>🖼️</div>
              <strong style={{ display: 'block', fontSize: '.96rem', marginBottom: 4 }}>
                {processingFile ? 'Analyzing QR Image…' : 'Choose or Drag QR Code Image'}
              </strong>
              <small style={{ color: 'var(--muted)', fontSize: '.8rem' }}>
                Supports PNG, JPG, WEBP, or screenshot of a certificate QR code
              </small>
            </div>

            {fileError && (
              <div
                style={{
                  marginTop: 12,
                  padding: '10px 14px',
                  borderRadius: 10,
                  background: 'rgba(255, 107, 107, 0.1)',
                  border: '1px solid var(--bad)',
                  fontSize: '.82rem',
                  color: 'var(--bad)',
                  textAlign: 'left'
                }}
              >
                ✕ {fileError}
              </div>
            )}
          </div>
        )}

        {/* Informative Mobile scanning callout */}
        <div
          style={{
            marginTop: 18,
            padding: '12px 14px',
            borderRadius: 12,
            background: 'rgba(185, 180, 255, 0.05)',
            border: '1px solid rgba(185, 180, 255, 0.15)',
            fontSize: '.76rem',
            color: 'var(--muted)',
            textAlign: 'left',
            lineHeight: 1.5
          }}
        >
          <strong style={{ color: 'var(--cyan)' }}>💡 Scanning with a Phone Camera?</strong>
          <br />
          If you scan the certificate QR code with your smartphone camera, your phone must be on the same Wi-Fi network and access this site via your computer&apos;s local IP address (e.g. <code>http://192.168.x.x:5173</code>) rather than <code>localhost</code>.
        </div>
      </div>
    </div>
  );
}
