import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 800, "CERTCHAIN — Complete Project & Technical Documentation")
            self.drawRightString(540, 800, "Ethereum Sepolia • Web3")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 794, 540, 794)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 540, 42)
        self.drawString(54, 30, "Student: Katuri Keerthi (24R11A66N9) | GCET CSE-AI&ML | CUTM Internship")
        self.drawRightString(540, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf():
    pdf_filename = "CertChain_Complete_Project_Overview.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        alignment=0,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#0f766e'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0369a1')
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TC',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    table_cell_bold = ParagraphStyle(
        'TCB',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )

    story = []

    # ==========================================
    # HEADER BANNER & PROJECT TITLE
    # ==========================================
    story.append(Paragraph("CERTCHAIN", ParagraphStyle('Eyebrow', fontName='Helvetica-Bold', fontSize=10, leading=12, textColor=colors.HexColor('#2563eb'), spaceAfter=4)))
    story.append(Paragraph("Decentralized Academic Credential Verification Platform", title_style))
    story.append(Paragraph("Complete Technical Project Dossier: Purpose, System Architecture, Cryptographic Pipeline, Full-Stack Tech Stack, and Live Sepolia Deployment", subtitle_style))
    
    # Metadata Pill Box Table
    meta_data = [
        [
            Paragraph("<b>Author:</b> KATURI KEERTHI<br/><b>Roll No:</b> 24R11A66N9", table_cell_style),
            Paragraph("<b>College:</b> Geethanjali College of Engineering & Tech (GCET)<br/><b>Department:</b> CSE-AI&ML (2026-27)", table_cell_style),
            Paragraph("<b>Internship Org:</b> Centurion University (CUTM)<br/><b>Certificate ID:</b> CUTM/AP/26/907367077873", table_cell_style),
            Paragraph("<b>Smart Contract:</b> Ethereum Sepolia<br/><b>Live Status:</b> Verified & Deployed", table_cell_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[115, 135, 125, 115])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 1: EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # ==========================================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "Academic credential fraud has emerged as a multi-billion dollar crisis threatening the integrity of global higher education. Counterfeit degrees, fabricated graduation certificates, and fake diploma mills proliferate due to the weaknesses of traditional paper certificates and centralized verification repositories.",
        body_style
    ))
    
    # Callout Box: Traditional Verification Challenges
    prob_box = [
        [Paragraph("<b>Key Vulnerabilities of Legacy Centralized Systems:</b><br/>"
                   "• <b>Turnaround Delays:</b> Employers and background checkers must wait 3 to 6 weeks for university registrar offices to manually pull physical archives.<br/>"
                   "• <b>High Intermediary Fees:</b> Commercial screening agencies charge significant fees per certificate verification.<br/>"
                   "• <b>Centralized Single Points of Failure:</b> Traditional databases (SQL) can be silently altered by malicious database administrators or compromised through ransomware attacks.<br/>"
                   "• <b>Data Privacy Infringements:</b> Exposing student academic records to third parties violates modern privacy standards.", callout_style)]
    ]
    t_prob = Table(prob_box, colWidths=[490])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fef2f2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#fca5a5')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<b>The CertChain Solution:</b> CertChain replaces centralized trust with mathematical, cryptographic trust. By computing a deterministic SHA-256 binary hash of the certificate document and anchoring only this hash to a Solidity smart contract on the Ethereum Sepolia blockchain, credentials become permanently immutable, tamper-evident, and verifiable in under 500 milliseconds without exposing sensitive student information.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 2: SYSTEM ARCHITECTURE & CRYPTOGRAPHIC PIPELINE
    # ==========================================
    story.append(Paragraph("2. System Architecture & Cryptographic Pipeline", h1_style))
    story.append(Paragraph(
        "CertChain is architected as a modern, decoupled 4-tier Web3 platform designed for low latency, zero transaction fees for students, and high throughput:",
        body_style
    ))
    
    story.append(Paragraph("• <b>Tier 1: Smart Contract Layer (Ethereum Sepolia):</b> The authoritative source of truth. Contains the immutable registry mapping each Certificate ID to its SHA-256 document hash, issuer address, issuance timestamp, and revocation flag.", bullet_style))
    story.append(Paragraph("• <b>Tier 2: Institutional Relayer Layer (Node.js & Express):</b> A secure relayer service holding the institution's authorized Ethereum private key. Sponsors all blockchain gas fees on behalf of university staff, enabling one-click gasless certificate issuance.", bullet_style))
    story.append(Paragraph("• <b>Tier 3: Client-Side Cryptographic Engine (Web Crypto API & jsPDF):</b> Renders certificates as deterministic vector PDFs and calculates 256-bit binary SHA-256 hashes directly in the browser memory.", bullet_style))
    story.append(Paragraph("• <b>Tier 4: Public Verification Portal (React & html5-qrcode):</b> A zero-trust web portal that directly interrogates the Ethereum Sepolia blockchain via public JSON-RPC nodes to authenticate credentials instantly without requiring logins.", bullet_style))
    story.append(Spacer(1, 6))

    # Architecture Diagram Image
    if os.path.exists('presentation_assets/certchain_architecture_diagram.png'):
        story.append(Paragraph("<b>Figure 1: High-Level System Architecture of CertChain</b>", h2_style))
        story.append(Image('presentation_assets/certchain_architecture_diagram.png', width=490, height=270))
        story.append(Spacer(1, 8))

    # Data Flow Diagram Image
    if os.path.exists('presentation_assets/certchain_dataflow_diagram.png'):
        story.append(Paragraph("<b>Figure 2: End-to-End Cryptographic Issuance & Verification Data Flow</b>", h2_style))
        story.append(Image('presentation_assets/certchain_dataflow_diagram.png', width=490, height=270))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ==========================================
    # SECTION 3: EXHAUSTIVE TECHNOLOGY STACK
    # ==========================================
    story.append(Paragraph("3. Exhaustive Technology Stack", h1_style))
    story.append(Paragraph(
        "CertChain leverages cutting-edge open-source Web3, frontend, backend, and cryptographic technologies chosen for reliability, security, and developer ergonomics:",
        body_style
    ))

    tech_table_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technology / Library", table_header_style), Paragraph("Version", table_header_style), Paragraph("Role & Technical Rationale", table_header_style)],
        [Paragraph("Blockchain Layer", table_cell_bold), Paragraph("Solidity", table_cell_style), Paragraph("0.8.24", table_cell_style), Paragraph("Smart contract language executing on the EVM; implements state storage, access control, and revocation.", table_cell_style)],
        [Paragraph("Blockchain Network", table_cell_bold), Paragraph("Ethereum Sepolia", table_cell_style), Paragraph("Chain 11155111", table_cell_style), Paragraph("Proof-of-Stake Ethereum testnet mirroring mainnet EVM execution with block explorer auditability.", table_cell_style)],
        [Paragraph("Smart Contract Framework", table_cell_bold), Paragraph("Foundry (forge/cast)", table_cell_style), Paragraph("0.2.0", table_cell_style), Paragraph("High-speed Rust-based toolkit for automated smart contract testing, gas profiling, and deployment.", table_cell_style)],
        [Paragraph("Security Standards", table_cell_bold), Paragraph("OpenZeppelin Contracts", table_cell_style), Paragraph("v5.0.0", table_cell_style), Paragraph("Industry-standard audited Ownable pattern for multi-administrator role access control.", table_cell_style)],
        [Paragraph("Web3 Client Library", table_cell_bold), Paragraph("Ethers.js", table_cell_style), Paragraph("v6.13.2", table_cell_style), Paragraph("Handles contract instantiation, JSON-RPC Sepolia communication, event listening, and wallet signatures.", table_cell_style)],
        [Paragraph("Frontend Framework", table_cell_bold), Paragraph("React", table_cell_style), Paragraph("v18.3.1", table_cell_style), Paragraph("Component-based reactive UI managing issuance wizards, certificate previews, and verification states.", table_cell_style)],
        [Paragraph("Build & Bundling", table_cell_bold), Paragraph("Vite", table_cell_style), Paragraph("v5.4.21", table_cell_style), Paragraph("Lightning-fast ESM development server and optimized Rollup production bundler.", table_cell_style)],
        [Paragraph("Styling System", table_cell_bold), Paragraph("Vanilla CSS (Glassmorphism)", table_cell_style), Paragraph("CSS3", table_cell_style), Paragraph("Custom design system with HSL tokens, backdrop blurs, sleek dark modes, and zero third-party CSS bloat.", table_cell_style)],
        [Paragraph("Backend Server", table_cell_bold), Paragraph("Node.js & Express", table_cell_style), Paragraph("v20+ / 4.19", table_cell_style), Paragraph("Lightweight REST API service managing institutional relayer key signing and PDF file uploads.", table_cell_style)],
        [Paragraph("Database", table_cell_bold), Paragraph("SQLite (better-sqlite3)", table_cell_style), Paragraph("v11.8.1", table_cell_style), Paragraph("High-speed embedded relational database caching certificate metadata for institutional admin dashboards.", table_cell_style)],
        [Paragraph("Document Generation", table_cell_bold), Paragraph("jsPDF", table_cell_style), Paragraph("v2.5.2", table_cell_style), Paragraph("Deterministic vector PDF rendering engine generating consistent binary array buffers for hashing.", table_cell_style)],
        [Paragraph("Cryptographic Hashing", table_cell_bold), Paragraph("Web Cryptography API", table_cell_style), Paragraph("Native W3C", table_cell_style), Paragraph("Hardware-accelerated SHA-256 binary digesting directly in browser memory.", table_cell_style)],
        [Paragraph("Optical Scanner", table_cell_bold), Paragraph("html5-qrcode", table_cell_style), Paragraph("v2.3.8", table_cell_style), Paragraph("Real-time optical barcode scanner reading QR codes from webcams, mobile cameras, or screenshot files.", table_cell_style)],
        [Paragraph("DevOps & Hosting", table_cell_bold), Paragraph("Netlify Edge / Vercel", table_cell_style), Paragraph("Global CDN", table_cell_style), Paragraph("Serverless edge content delivery network with automated CI/CD and single-page routing.", table_cell_style)],
    ]
    t_tech = Table(tech_table_data, colWidths=[80, 110, 60, 240])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 4: KEY FEATURES & ARCHITECTURAL HIGHLIGHTS
    # ==========================================
    story.append(Paragraph("4. Key Innovations & Distinctive Features", h1_style))
    
    features = [
        ("Zero-Trust Mathematical Verification", 
         "Verifiers do not need to contact the university registrar or trust a third-party screening company. The presented certificate is hashed locally, and its existence is checked against the immutable Ethereum Sepolia ledger. Verification takes under 500 ms."),
        
        ("Dual-Mode Issuance Mechanism", 
         "Supports two issuance methods: <b>(1) Gasless Institutional Relayer</b>, where the university server signs and sponsors blockchain gas fees automatically, requiring zero crypto knowledge from administrators; and <b>(2) Web3 Wallet Signing</b>, where administrators can connect MetaMask to sign transactions directly on Sepolia."),
        
        ("Privacy-Preserving Off-Chain Architecture", 
         "In compliance with global data privacy regulations (GDPR / Indian DPDP Act), student names, grades, and identity details are NEVER published in plaintext on the public blockchain. Only the non-invertible SHA-256 cryptographic digest is anchored."),
        
        ("Avalanche Effect Tamper Detection", 
         "Because SHA-256 produces entirely different hashes if even a single comma, grade, or character is altered (avalanche effect), forged documents fail verification instantly, indicating unauthorized tampering."),
        
        ("Real-Time In-Browser Optical Camera QR Scanner", 
         "Verifiers can click 'Scan QR Code' to launch a high-speed viewfinder that decodes physical paper certificates via smartphone cameras or computer webcams, or allows dragging and dropping a screenshot image."),
        
        ("On-Chain Revocation with Audit Trail", 
         "If an academic credential is found to have been issued in error or compromised, the institution can execute an immutable on-chain revocation with a timestamped reason, which immediately invalidates all future verification attempts."),
        
        ("Resilient Static Client-Side Fallback Engine", 
         "The frontend architecture includes self-contained offline authentication and verification fallbacks. If hosted statically on Netlify Edge without a live backend, the portal continues to operate reliably.")
    ]
    
    for f_title, f_desc in features:
        story.append(Paragraph(f"• <b>{f_title}:</b> {f_desc}", bullet_style))
    story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ==========================================
    # SECTION 5: SMART CONTRACT SPECIFICATIONS
    # ==========================================
    story.append(Paragraph("5. Smart Contract Technical Specifications", h1_style))
    story.append(Paragraph(
        "The core logic of CertChain is encapsulated within the <b>CertChain.sol</b> smart contract, audited and deployed to the Ethereum Sepolia network:",
        body_style
    ))

    sc_meta = [
        [Paragraph("<b>Contract Parameter</b>", table_header_style), Paragraph("Value / Implementation", table_header_style)],
        [Paragraph("Smart Contract Name", table_cell_bold), Paragraph("CertChain.sol", table_cell_style)],
        [Paragraph("Compiler Version", table_cell_bold), Paragraph("Solidity 0.8.24 (Cancun EVM target)", table_cell_style)],
        [Paragraph("Sepolia Contract Address", table_cell_bold), Paragraph("<code>0xba0553a92F82F62E62d38496398637f9CB11B37C</code>", table_cell_style)],
        [Paragraph("Contract Deployer / Owner", table_cell_bold), Paragraph("<code>0xe23ce985284365B92fF6EE0F855a11811274ceF1</code>", table_cell_style)],
        [Paragraph("Sponsored Relayer Key", table_cell_bold), Paragraph("Dedicated institutional key with automated nonce and gas pricing management", table_cell_style)],
        [Paragraph("Seed Issuance Tx Hash", table_cell_bold), Paragraph("<code>0x243790c4e526836ef380d4f41bfec44ded681699a882061fc538be5587ce7f78</code>", table_cell_style)],
        [Paragraph("Security Standards", table_cell_bold), Paragraph("OpenZeppelin Ownable, Role-Based Access Control, Nonce Checks", table_cell_style)],
    ]
    t_sc_meta = Table(sc_meta, colWidths=[150, 340])
    t_sc_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sc_meta)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Primary Smart Contract Functions (ABI Summary):</b>", h2_style))
    fn_table = [
        [Paragraph("Function Signature", table_header_style), Paragraph("Type", table_header_style), Paragraph("Description", table_header_style)],
        [Paragraph("<code>issueCertificate(string certId, bytes32 docHash)</code>", table_cell_style), Paragraph("External<br/>State Change", table_cell_bold), Paragraph("Anchors a new certificate hash on-chain. Callable only by authorized institutional issuers.", table_cell_style)],
        [Paragraph("<code>revokeCertificate(string certId, string reason)</code>", table_cell_style), Paragraph("External<br/>State Change", table_cell_bold), Paragraph("Marks a certificate as revoked with an audit reason. Callable by admin or issuing authority.", table_cell_style)],
        [Paragraph("<code>verifyCertificate(string certId)</code>", table_cell_style), Paragraph("External View<br/>(Gasless)", table_cell_bold), Paragraph("Returns (bool exists, bytes32 docHash, address issuer, uint256 issuedAt, bool isRevoked, uint256 revokedAt, string reason).", table_cell_style)],
        [Paragraph("<code>authorizeIssuer(address issuer)</code>", table_cell_style), Paragraph("External<br/>OnlyOwner", table_cell_bold), Paragraph("Grants university staff or affiliated colleges the right to issue blockchain credentials.", table_cell_style)],
        [Paragraph("<code>deauthorizeIssuer(address issuer)</code>", table_cell_style), Paragraph("External<br/>OnlyOwner", table_cell_bold), Paragraph("Revokes issuing authority from a compromised or retired administrator address.", table_cell_style)],
    ]
    t_fn = Table(fn_table, colWidths=[180, 80, 230])
    t_fn.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_fn)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 6: VISUAL WALKTHROUGH & SCREENSHOTS
    # ==========================================
    story.append(Paragraph("6. Visual System Walkthrough (Screenshots)", h1_style))
    story.append(Paragraph(
        "The following screenshots illustrate the complete user and administrator experience across issuance, verification, and telemetry:",
        body_style
    ))

    screenshots = [
        ("presentation_assets/01_Landing_Hero.png", "1. Public Landing Page — Hero interface showcasing Sepolia network status, features, and sample query cards."),
        ("presentation_assets/02_Public_Verify_Interface.png", "2. Zero-Trust Verification Portal — Search bar for Certificate IDs, quick test chips, and camera QR scanner button."),
        ("presentation_assets/03_QR_Camera_Scanner.png", "3. Real-Time Camera QR Code Scanner — Fast viewfinder decoding QR barcodes directly through browser media devices."),
        ("presentation_assets/05_Verified_Certificate_Result.png", "4. Cryptographically Verified Result Card — Displays on-chain proof for Katuri Keerthi with Etherscan transaction link."),
        ("presentation_assets/07_Admin_Dashboard_Telemetry.png", "5. Institutional Admin Telemetry Dashboard — Real-time analytics of valid vs. revoked certificates and system health."),
        ("presentation_assets/08_Issue_Credential_Live_Preview.png", "6. Credential Issuance Engine — Input form with presets and real-time SVG vector preview."),
        ("presentation_assets/09_Certificates_Registry_Table.png", "7. Institutional Registry & Revocation Management — Full registry table with instant on-chain revocation actions."),
        ("presentation_assets/11_Netlify_Public_Deployment.png", "8. Live Production Deployment — Running on Netlify Edge CDN with resilient client-side authentication fallbacks.")
    ]

    for img_path, caption in screenshots:
        if os.path.exists(img_path):
            story.append(KeepTogether([
                Paragraph(f"<b>{caption}</b>", h2_style),
                Image(img_path, width=490, height=240),
                Spacer(1, 8)
            ]))

    story.append(PageBreak())

    # ==========================================
    # SECTION 7: LIVE DEPLOYMENT & VERIFICATION CREDENTIALS
    # ==========================================
    story.append(Paragraph("7. Live Deployment, Repositories & Credentials", h1_style))
    
    dep_data = [
        [Paragraph("Item", table_header_style), Paragraph("Details & Public Link", table_header_style)],
        [Paragraph("GitHub Source Code Repository", table_cell_bold), Paragraph("https://github.com/Keerthi1316/certchain (Branch: main)", table_cell_style)],
        [Paragraph("Smart Contract on Etherscan", table_cell_bold), Paragraph("https://sepolia.etherscan.io/address/0xba0553a92F82F62E62d38496398637f9CB11B37C", table_cell_style)],
        [Paragraph("Seed Issuance Transaction", table_cell_bold), Paragraph("https://sepolia.etherscan.io/tx/0x243790c4e526836ef380d4f41bfec44ded681699a882061fc538be5587ce7f78", table_cell_style)],
        [Paragraph("Sample Verified Certificate ID", table_cell_bold), Paragraph("<b>CERT-2026-0001</b> (Recipient: <b>Katuri Keerthi</b>)", table_cell_style)],
        [Paragraph("Admin Login Email", table_cell_bold), Paragraph("<code>admin@institute.edu</code>", table_cell_style)],
        [Paragraph("Admin Login Password", table_cell_bold), Paragraph("<code>admin123</code>", table_cell_style)],
        [Paragraph("Local Development Server", table_cell_bold), Paragraph("http://localhost:5173 (Frontend) | http://localhost:4000 (API Backend)", table_cell_style)],
    ]
    t_dep = Table(dep_data, colWidths=[160, 330])
    t_dep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_dep)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 8: FUTURE ROADMAP & CONCLUSION
    # ==========================================
    story.append(Paragraph("8. Future Roadmap & Academic Conclusion", h1_style))
    story.append(Paragraph(
        "CertChain successfully establishes a scalable, production-ready foundation for next-generation academic credentialing. The future engineering roadmap includes:",
        body_style
    ))
    story.append(Paragraph("• <b>Soulbound Tokens (ERC-5192):</b> Upgrading certificate anchors to non-transferable NFTs bound directly to student decentralized identity (DID) wallets.", bullet_style))
    story.append(Paragraph("• <b>Zero-Knowledge Proofs (zk-SNARKs):</b> Enabling selective attribute disclosure (e.g., proving graduation with GPA > 3.5 without revealing the full transcript).", bullet_style))
    story.append(Paragraph("• <b>Layer-2 Rollups:</b> Expanding contract deployments to Arbitrum or Polygon for sub-cent transaction costs at national accreditation scale.", bullet_style))
    story.append(Paragraph("• <b>Multi-University Consortium:</b> Federating identity verification across international university alliances.", bullet_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Conclusion:</b> Under the guidance of Geethanjali College of Engineering and Technology (GCET) and Centurion University of Technology and Management (CUTM), CertChain proves that Blockchain technology can eliminate diploma fraud, protect student privacy, and automate credential verification worldwide.",
        body_style
    ))

    # Build the document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {pdf_filename} (Size: {os.path.getsize(pdf_filename)} bytes)")

if __name__ == '__main__':
    build_pdf()
