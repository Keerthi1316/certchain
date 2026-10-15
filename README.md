# CERTCHAIN — Blockchain Certificate Verification System

CertChain is a decentralized academic credential platform that issues certificates as high-resolution vector PDFs, anchors their SHA-256 cryptographic fingerprints on the **Ethereum Sepolia** testnet, and enables instant, tamper-proof public verification.

---

## 🌟 Live Smart Contract & Deployment Status

- **Smart Contract Address**: [`0xba0553a92F82F62E62d38496398637f9CB11B37C`](https://sepolia.etherscan.io/address/0xba0553a92F82F62E62d38496398637f9CB11B37C)
- **Network**: Ethereum Sepolia Testnet (Chain ID: `11155111`)
- **Sample Verified Certificate**: `CERT-2026-0001` (Keerthi Varma — Excellence in Smart Contract Verification)
- **Seed Issuance Tx**: [`0x243790c4e526836ef380d4f41bfec44ded681699a882061fc538be5587ce7f78`](https://sepolia.etherscan.io/tx/0x243790c4e526836ef380d4f41bfec44ded681699a882061fc538be5587ce7f78)

---

## 🚀 Quick Start (Run with One Command)

Prerequisites: **Node.js v20+** (tested & verified on Node v24).

### Step 1: Start the Entire System
From the project root (`certchain/`):

```bash
npm run dev
```
*(Or on Windows, simply double-click `start.bat`)*

This concurrently starts:
1. **Backend API Server**: [http://localhost:4000](http://localhost:4000) (built with Express & Node SQLite)
2. **Frontend Web App**: [http://localhost:5173](http://localhost:5173) (built with React, Vite & Ethers v6)

---

## 🔐 Credentials & Quick Testing

| Portal | URL | Credentials / Notes |
| :--- | :--- | :--- |
| **Public Landing** | `http://localhost:5173/` | Hero showcase, interactive preview, QR code scanner |
| **Public Verification** | `http://localhost:5173/verify` | Type `CERT-2026-0001` or drag-and-drop a certificate PDF |
| **Sample Live Record** | `http://localhost:5173/verify/CERT-2026-0001` | Direct verification link with Sepolia Etherscan proof |
| **Admin Login** | `http://localhost:5173/login` | Email: `admin@institute.edu`<br>Password: `admin123`<br>*(Has a 1-click **⚡ Auto-Fill** button)* |
| **Admin Dashboard** | `http://localhost:5173/admin` | Real-time on-chain stats, registry overview, issuer management |
| **Issue Wizard** | `http://localhost:5173/admin/issue` | Multi-step certificate issuing engine with live PDF preview |
| **Certificate Registry**| `http://localhost:5173/certificates` | Search, verify, download official PDF, or revoke records |

---

## 🛠️ Architecture & Features

### 1. Dual Issuing Engine (Zero Gas Friction)
- **⚡ Institution Relayer (Gasless / Instant Demo)**:
  Uses the institution's pre-authorized deployer key on Sepolia to broadcast and pay for the transaction. Evaluators and professors can issue real on-chain certificates immediately without needing personal Sepolia ETH!
- **🦊 MetaMask Wallet (Self-Signed Web3 Flow)**:
  Connect any personal Web3 wallet. If the wallet is not yet registered, use the 1-click **"⚡ Authorize Current Wallet"** button on the dashboard to register it on-chain in seconds.

### 2. Cryptographic Document Integrity Check
- When issuing, a deterministic PDF is rendered using `jsPDF`.
- The exact raw bytes are fingerprinted using **SHA-256** via the Web Crypto API.
- The 32-byte hash is permanently anchored in the smart contract mapping `certs[keccak256(certId)]`.
- On verification, uploading the PDF recalculates the SHA-256 hash in the browser and compares it against the smart contract. If even 1 pixel or byte is altered, it triggers a **Document Tampering Mismatch Alert** (`Status: 3 / HashMismatch`).

### 3. Privacy-Preserving
- **Zero Personally Identifiable Information (PII)** is stored on the Ethereum blockchain.
- Recipient email and private administrative fields remain strictly in the institution's SQLite database and are excluded from public API responses.

---

## 📁 Project Structure

```
certchain/
├── start.js               # Concurrently runs frontend and backend with colored logs
├── start.bat              # 1-click Windows launcher
├── package.json           # Root package script definitions
├── contracts/             # Solidity smart contracts
│   ├── src/CertChain.sol  # Core registry smart contract
│   └── out/CertChain.sol/ # Compiled ABI & EVM bytecode artifacts
├── server/                # Node.js backend
│   ├── .env               # Server environment configuration
│   ├── index.js           # Express REST API, SQLite database & Sepolia relayer
│   └── data/              # SQLite database (certchain.db) & stored PDFs
└── frontend/              # Modern React + Vite application
    ├── .env               # Contract address & Sepolia RPC URL
    ├── deploy.js          # Ethers v6 contract deployment script
    ├── seed-sample.js     # Seeds initial verified certificate on Sepolia
    └── src/
        ├── App.jsx        # Routing & layout orchestration
        ├── pages/         # Landing, Verify, Login, Dashboard, Issue, Certificates
        ├── components/    # Navigation, Certificate preview, Wallet Modal, Toasts
        └── lib/           # Ethers contract interface, PDF generator, REST API client
```

---

## 🧪 Manual Verification & CLI Scripts

If you want to run services individually:

### Backend:
```bash
cd server
npm start        # Runs on http://localhost:4000
```

### Frontend:
```bash
cd frontend
npm run dev      # Runs on http://localhost:5173
```

### Re-seed a Sample Certificate on Sepolia:
```bash
npm run seed
```

### Deploy a Fresh Contract Instance to Sepolia:
```bash
npm run deploy-contract
```
