import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    
    # Title Banner
    banner = patches.FancyBboxPatch((0.5, 9.0), 9.0, 0.8, boxstyle="round,pad=0.1", fc='#1e293b', ec='#3b82f6', lw=1.5)
    ax.add_patch(banner)
    ax.text(5.0, 9.45, "CertChain — Decentralized System Architecture", color='#f8fafc', fontsize=13, weight='bold', ha='center', va='center')
    ax.text(5.0, 9.15, "Decentralized Academic Credential Verification Platform on Ethereum Sepolia", color='#94a3b8', fontsize=8.5, ha='center', va='center')

    # Tier 1: Client Frontend
    box1 = patches.FancyBboxPatch((0.5, 4.8), 2.6, 3.8, boxstyle="round,pad=0.1", fc='#1e293b', ec='#06b6d4', lw=1.2)
    ax.add_patch(box1)
    ax.text(1.8, 8.2, "Client Layer", color='#38bdf8', fontsize=10.5, weight='bold', ha='center')
    ax.text(1.8, 7.8, "React 18 + Vite SPA", color='#94a3b8', fontsize=8, ha='center')
    
    fe_items = [
        "• Public Verification Portal",
        "• html5-qrcode Camera View",
        "• Institutional Admin UI",
        "• Real-Time Vector Preview",
        "• Ethers.js v6 Provider",
        "• MetaMask Signer"
    ]
    for idx, item in enumerate(fe_items):
        ax.text(0.7, 7.3 - idx*0.42, item, color='#e2e8f0', fontsize=7.8)

    # Tier 2: Relayer & Cryptographic Engine
    box2 = patches.FancyBboxPatch((3.7, 4.8), 2.6, 3.8, boxstyle="round,pad=0.1", fc='#1e293b', ec='#8b5cf6', lw=1.2)
    ax.add_patch(box2)
    ax.text(5.0, 8.2, "Relayer & Crypto", color='#a78bfa', fontsize=10.5, weight='bold', ha='center')
    ax.text(5.0, 7.8, "Node.js + Web Crypto", color='#94a3b8', fontsize=8, ha='center')
    
    be_items = [
        "• Deterministic jsPDF Engine",
        "• SHA-256 Digest Pipeline",
        "• Gasless Relayer Sponsor",
        "• ECDSA Key Custody",
        "• SQLite Local Cache",
        "• REST API (Express)"
    ]
    for idx, item in enumerate(be_items):
        ax.text(3.9, 7.3 - idx*0.42, item, color='#e2e8f0', fontsize=7.8)

    # Tier 3: Blockchain Settlement
    box3 = patches.FancyBboxPatch((6.9, 4.8), 2.6, 3.8, boxstyle="round,pad=0.1", fc='#1e293b', ec='#10b981', lw=1.2)
    ax.add_patch(box3)
    ax.text(8.2, 8.2, "Blockchain Layer", color='#34d399', fontsize=10.5, weight='bold', ha='center')
    ax.text(8.2, 7.8, "Ethereum Sepolia", color='#94a3b8', fontsize=8, ha='center')
    
    bc_items = [
        "• CertChain.sol Smart Contract",
        "• Immutable Hash Registry",
        "• Multi-Admin Access Control",
        "• On-Chain Revocation Map",
        "• Event Log Indexing",
        "• Etherscan Explorer Audits"
    ]
    for idx, item in enumerate(bc_items):
        ax.text(7.1, 7.3 - idx*0.42, item, color='#e2e8f0', fontsize=7.8)

    # Connecting Arrows
    arrow1 = patches.FancyArrowPatch((3.1, 6.7), (3.7, 6.7), color='#38bdf8', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    arrow2 = patches.FancyArrowPatch((3.7, 6.1), (3.1, 6.1), color='#a78bfa', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    arrow3 = patches.FancyArrowPatch((6.3, 6.7), (6.9, 6.7), color='#a78bfa', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    arrow4 = patches.FancyArrowPatch((6.9, 6.1), (6.3, 6.1), color='#34d399', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    ax.add_patch(arrow1); ax.add_patch(arrow2); ax.add_patch(arrow3); ax.add_patch(arrow4)
    ax.text(3.4, 6.9, "JSON-RPC", color='#38bdf8', fontsize=6.5, ha='center')
    ax.text(6.6, 6.9, "Tx Hash", color='#34d399', fontsize=6.5, ha='center')

    # Bottom Data & Security Banner
    banner2 = patches.FancyBboxPatch((0.5, 0.8), 9.0, 3.4, boxstyle="round,pad=0.1", fc='#1e293b', ec='#64748b', lw=1.0)
    ax.add_patch(banner2)
    ax.text(5.0, 3.8, "Zero-Trust Cryptographic Data Lifecycle", color='#f8fafc', fontsize=9.5, weight='bold', ha='center')

    steps = [
        ("1. Issue & Layout", "Vector PDF compiled with dynamic certificate metadata.", '#38bdf8'),
        ("2. SHA-256 Digest", "Exact byte-level mathematical hash generated client-side.", '#a78bfa'),
        ("3. On-Chain Anchor", "Contract stores digest; mints timestamped verifiable record.", '#34d399'),
        ("4. Optical Scanning", "Verifier scans QR via webcam / image to fetch on-chain proof.", '#f59e0b')
    ]
    for i, (title, desc, clr) in enumerate(steps):
        x = 0.8 + i * 2.2
        sb = patches.FancyBboxPatch((x, 1.2), 2.0, 2.2, boxstyle="round,pad=0.08", fc='#0f172a', ec=clr, lw=1.0)
        ax.add_patch(sb)
        ax.text(x + 1.0, 3.0, title, color=clr, fontsize=8, weight='bold', ha='center')
        ax.text(x + 1.0, 2.1, desc, color='#cbd5e1', fontsize=6.8, ha='center', wrap=True)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('presentation_assets/certchain_architecture_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("SUCCESS: certchain_architecture_diagram.png created.")

def create_dataflow_diagram():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_facecolor('#0f172a')
    fig.patch.set_facecolor('#0f172a')
    
    # Title Banner
    banner = patches.FancyBboxPatch((0.5, 9.0), 9.0, 0.8, boxstyle="round,pad=0.1", fc='#1e293b', ec='#10b981', lw=1.5)
    ax.add_patch(banner)
    ax.text(5.0, 9.45, "CertChain — End-to-End Cryptographic Data Flow", color='#f8fafc', fontsize=13, weight='bold', ha='center', va='center')
    ax.text(5.0, 9.15, "Step-by-Step Issuance, Fingerprinting, Ledger Verification, and Optical Retrieval", color='#94a3b8', fontsize=8.5, ha='center', va='center')

    # Grid of 6 functional flow cards
    cards = [
        ("Institutional Authority", "Admin logs in, defines course, recipient (Katuri Keerthi), and honors.", "#38bdf8", 0.6, 5.0),
        ("jsPDF Vector Compiler", "Generates deterministic A4 landscape certificate with security guilloche.", "#a78bfa", 3.7, 5.0),
        ("SHA-256 Binary Digest", "Transforms exact binary bytes into 64-char hexadecimal hash fingerprint.", "#f43f5e", 6.8, 5.0),
        ("Ethereum Sepolia Tx", "Calls issueCertificate() anchored immutably into Ethereum state.", "#10b981", 6.8, 1.2),
        ("QR Optical Encoding", "Encodes verification URI with Certificate ID directly onto document face.", "#f59e0b", 3.7, 1.2),
        ("Zero-Trust Verification", "Public verifier scans QR code; queries Sepolia node directly for validity.", "#06b6d4", 0.6, 1.2)
    ]

    for title, desc, clr, x, y in cards:
        card = patches.FancyBboxPatch((x, y), 2.6, 3.2, boxstyle="round,pad=0.1", fc='#1e293b', ec=clr, lw=1.2)
        ax.add_patch(card)
        ax.text(x + 1.3, y + 2.7, title, color=clr, fontsize=9.5, weight='bold', ha='center')
        ax.text(x + 1.3, y + 1.4, desc, color='#cbd5e1', fontsize=7.5, ha='center', wrap=True)

    # Arrows for flow
    a1 = patches.FancyArrowPatch((3.2, 6.6), (3.7, 6.6), color='#38bdf8', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    a2 = patches.FancyArrowPatch((6.3, 6.6), (6.8, 6.6), color='#a78bfa', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    a3 = patches.FancyArrowPatch((8.1, 5.0), (8.1, 4.4), color='#f43f5e', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    a4 = patches.FancyArrowPatch((6.8, 2.8), (6.3, 2.8), color='#10b981', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    a5 = patches.FancyArrowPatch((3.7, 2.8), (3.2, 2.8), color='#f59e0b', arrowstyle='->,head_width=4,head_length=5', lw=1.5)
    
    for a in [a1, a2, a3, a4, a5]:
        ax.add_patch(a)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('presentation_assets/certchain_dataflow_diagram.png', bbox_inches='tight', dpi=300)
    plt.close()
    print("SUCCESS: certchain_dataflow_diagram.png created.")

if __name__ == '__main__':
    create_architecture_diagram()
    create_dataflow_diagram()
