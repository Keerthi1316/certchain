import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JsonRpcProvider, Wallet, ContractFactory } from 'ethers';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function deploy() {
  console.log('Connecting to Sepolia RPC...');
  const provider = new JsonRpcProvider('https://ethereum-sepolia-rpc.publicnode.com');
  const privateKey = '483ea0095c8df6fd81f5031b85323096efda2316c61d0082ffddff2d3d3c8869';
  const wallet = new Wallet(privateKey, provider);
  console.log('Deployer address:', wallet.address);

  const balance = await provider.getBalance(wallet.address);
  console.log('Balance:', (Number(balance) / 1e18).toFixed(5), 'Sepolia ETH');

  const artifactPath = path.resolve(__dirname, '../contracts/out/CertChain.sol/CertChain.json');
  if (!fs.existsSync(artifactPath)) {
    throw new Error('Artifact not found at ' + artifactPath);
  }
  const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));

  const factory = new ContractFactory(artifact.abi, artifact.bytecode.object, wallet);
  console.log('Deploying CertChain contract to Ethereum Sepolia...');
  const contract = await factory.deploy({ gasLimit: 5200000 });

  const tx = contract.deploymentTransaction();
  console.log('Transaction broadcast! Tx hash:', tx.hash);
  console.log('Waiting for block confirmation on Sepolia...');
  await contract.waitForDeployment();

  const deployedAddress = await contract.getAddress();
  console.log('=============================================');
  console.log('SUCCESS! CertChain deployed at:', deployedAddress);
  console.log('Etherscan: https://sepolia.etherscan.io/address/' + deployedAddress);
  console.log('=============================================');

  const owner = await contract.owner();
  const issuerCount = await contract.issuerCount();
  console.log('Verified on-chain: owner =', owner, '| issuerCount =', issuerCount.toString());

  return deployedAddress;
}

deploy().catch((err) => {
  console.error('Deployment error:', err);
  process.exit(1);
});
