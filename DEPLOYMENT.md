# CertChain — Cloud Deployment Guide (Render + Vercel)

This guide provides step-by-step instructions to deploy **CertChain** to production using **Render** for the backend API and **Vercel** for the frontend application.

The smart contract is already deployed and live on **Ethereum Sepolia Testnet** at:
`0xba0553a92F82F62E62d38496398637f9CB11B37C`

---

## Why did the previous Netlify link show "This site is suspended"?
The previous deployment was created using Netlify CLI's temporary **anonymous drop mode** (`--allow-anonymous`). 
Netlify treats anonymous drops as temporary 60-minute to 24-hour trials. If not claimed into a registered Netlify account, Netlify's automated abuse-prevention system suspends or purges the temporary link.

To make the site **100% permanent** so that you can open it anytime, from any phone, laptop, or examiner's computer without needing Antigravity or your computer running, follow the **Permanent Netlify Deployment** below.

---

## Permanent Netlify Deployment (Free & Never Suspended)

Your code is already pushed to GitHub at: **`https://github.com/Keerthi1316/certchain`**

1. Go to [app.netlify.com](https://app.netlify.com) and click **Log in with GitHub**.
2. In your Netlify dashboard, click **"Add new site"** → **"Import an existing project"**.
3. Choose **GitHub** as your Git provider and authorize Netlify.
4. Select your repository: **`Keerthi1316/certchain`**.
5. Netlify will detect your repository settings. Configure the fields as follows:
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend/dist`
6. Click **Deploy certchain**.
7. Within 60 seconds, your site will be permanently live on Netlify's global Edge CDN.
8. *(Optional)* To get a clean URL:
   - Go to **Site configuration** → **Change site name**.
   - Change it to something custom like `certchain-keerthi.netlify.app`.

Because this is connected directly to your GitHub account:
- It is **100% free** and **will never be suspended**.
- It runs 24/7/365 independently on Netlify servers (no Antigravity needed).
- Whenever you push new code to GitHub, Netlify automatically redeploys your site in seconds.

---

## Step 1: Push Code to GitHub

Your local git repository has already been initialized and committed on the `main` branch.

1. Go to [github.com/new](https://github.com/new) and create a new repository (e.g. `certchain`).
2. Link your local repository and push:

```bash
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/certchain.git
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (Free Tier)

Render hosts the Node.js Express API, the institutional relayer, and the SQLite metadata store.

1. Go to [render.com](https://render.com) and sign in with GitHub.
2. Click **New +** → **Web Service**.
3. Select your `certchain` repository.
4. Configure the service:
   - **Name**: `certchain-backend`
   - **Region**: Choose the closest region to you (e.g., Singapore, Frankfurt, Oregon)
   - **Root Directory**: `server`
   - **Environment**: `Node`
   - **Build Command**: `npm install`
   - **Start Command**: `node index.js`
   - **Instance Type**: `Free`
5. Under **Environment Variables**, add:

| Key | Value | Notes |
| :--- | :--- | :--- |
| `PORT` | `4000` | Internal server port |
| `JWT_SECRET` | *(Generate any long random string)* | Used for session tokens |
| `ADMIN_EMAIL` | `admin@institute.edu` | Issuer admin login email |
| `ADMIN_PASSWORD` | `admin123` | *(Or your custom password)* |
| `CONTRACT_ADDRESS` | `0xba0553a92F82F62E62d38496398637f9CB11B37C` | Deployed Sepolia contract |
| `RPC_URL` | `https://ethereum-sepolia-rpc.publicnode.com` | Public Sepolia RPC |
| `NETWORK` | `sepolia` | Network identifier |
| `CORS_ORIGIN` | `*` | Or your Vercel URL |
| `RELAYER_PRIVATE_KEY` | `483ea0095c8df6fd81f5031b85323096efda2316c61d0082ffddff2d3d3c8869` | Sponsored gas relayer wallet |

6. Click **Create Web Service**.
7. Once deployed, Render will provide your public backend URL (e.g. `https://certchain-backend.onrender.com`).
8. Verify it by visiting `https://certchain-backend.onrender.com/api/health` — it should return `{"ok":true}`.

---

## Step 3: Deploy Frontend to Vercel (Free Tier)

Vercel provides edge CDN delivery, fast builds, and automatic SSL for the React application.

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **Add New…** → **Project**.
3. Import your `certchain` repository.
4. In the **Configure Project** screen:
   - **Framework Preset**: `Vite`
   - **Root Directory**: Click *Edit* and select `frontend` *(or leave root since `vercel.json` handles monorepos)*
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Expand **Environment Variables** and add:

| Key | Value | Notes |
| :--- | :--- | :--- |
| `VITE_API_URL` | `https://certchain-backend.onrender.com` | Your Render backend URL from Step 2 |
| `VITE_CONTRACT_ADDRESS` | `0xba0553a92F82F62E62d38496398637f9CB11B37C` | Sepolia contract address |
| `VITE_RPC_URL` | `https://ethereum-sepolia-rpc.publicnode.com` | Sepolia RPC endpoint |

6. Click **Deploy**.
7. Within 1 minute, Vercel will generate your live production URL (e.g. `https://certchain.vercel.app`).

---

## Step 4: End-to-End Verification

1. Open your live Vercel URL in any browser or on your smartphone.
2. Navigate to `/verify/CERT-2026-0001` — it will immediately query Ethereum Sepolia and display the verified credential.
3. Test the **"Scan to Verify"** feature:
   - Test with your device's webcam.
   - Or upload an image/screenshot of the certificate QR code.
4. Log into the Admin Console at `/login` using:
   - **Email**: `admin@institute.edu`
   - **Password**: `admin123`
5. Issue a new credential: the gasless relayer on Render will sign and anchor the transaction onto Ethereum Sepolia without requiring gas from the user!
