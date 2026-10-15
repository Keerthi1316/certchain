import { BrowserProvider, JsonRpcProvider, Contract, ZeroHash } from 'ethers';
import { ABI } from './abi.js';

export const SEPOLIA_ID = 11155111;
export const ETHERSCAN = 'https://sepolia.etherscan.io';
export const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS || '0xba0553a92F82F62E62d38496398637f9CB11B37C';
const RPC = import.meta.env.VITE_RPC_URL || 'https://ethereum-sepolia-rpc.publicnode.com';
export const STATUS = ['notfound', 'valid', 'revoked', 'mismatch'];

export const hasWallet = () => typeof window !== 'undefined' && !!window.ethereum;
export const short = (s, a = 6, b = 4) => (s ? `${s.slice(0, a)}…${s.slice(-b)}` : '');

const reader = () => {
  return new Contract(CONTRACT_ADDRESS, ABI, new JsonRpcProvider(RPC, SEPOLIA_ID, { staticNetwork: true }));
};
const writer = async () => {
  const signer = await new BrowserProvider(window.ethereum).getSigner();
  return new Contract(CONTRACT_ADDRESS, ABI, signer);
};

export async function connectWallet() {
  if (!hasWallet()) throw new Error('MetaMask is not installed');
  const p = new BrowserProvider(window.ethereum);
  const [addr] = await p.send('eth_requestAccounts', []);
  const { chainId } = await p.getNetwork();
  return { addr, chainId: Number(chainId) };
}

export async function switchToSepolia() {
  try {
    await window.ethereum.request({ method: 'wallet_switchEthereumChain', params: [{ chainId: '0xaa36a7' }] });
  } catch (e) {
    if (e.code !== 4902) throw e;
    await window.ethereum.request({ method: 'wallet_addEthereumChain', params: [{
      chainId: '0xaa36a7', chainName: 'Sepolia', rpcUrls: [RPC], blockExplorerUrls: [ETHERSCAN],
      nativeCurrency: { name: 'Sepolia ETH', symbol: 'ETH', decimals: 18 } }] });
  }
}

/** Public, read-only. Pass docHash to also check the document; omit to skip. */
export async function verifyOnChain(certId, docHash) {
  const c = reader();
  const status = STATUS[Number(await c.verify(certId, docHash || ZeroHash))];
  if (status === 'notfound') return { status };
  const x = await c.getCertificate(certId);
  return { status, docHash: x.docHash, issuer: x.issuer, issuedAt: Number(x.issuedAt) * 1000,
    revokedAt: Number(x.revokedAt) * 1000, revokedBy: x.revokedBy };
}

export async function issueOnChain(certId, docHash, onSent) {
  const tx = await (await writer()).issue(certId, docHash);
  onSent?.(tx.hash);
  const r = await tx.wait();
  return { txHash: tx.hash, block: r.blockNumber };
}

export async function revokeOnChain(certId, onSent) {
  const tx = await (await writer()).revoke(certId);
  onSent?.(tx.hash);
  const r = await tx.wait();
  return { txHash: tx.hash, block: r.blockNumber };
}

export async function manageIssuer(add, address) {
  const tx = await (await writer())[add ? 'addIssuer' : 'removeIssuer'](address);
  await tx.wait();
  return tx.hash;
}

export async function chainStats(addr) {
  const c = reader();
  const [issued, revoked, issuers, owner, issuer] = await Promise.all([
    c.totalIssued(), c.totalRevoked(), c.issuerCount(), c.owner(), addr ? c.isIssuer(addr) : false]);
  return { issued: Number(issued), revoked: Number(revoked), issuers: Number(issuers),
    isOwner: !!addr && owner.toLowerCase() === addr.toLowerCase(), isIssuer: issuer };
}

export const friendlyError = (e) =>
  e?.code === 'ACTION_REJECTED' || e?.code === 4001 ? 'Transaction rejected'
  : e?.reason || e?.shortMessage || e?.message || 'Something went wrong';
