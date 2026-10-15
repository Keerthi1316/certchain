import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

console.log('\x1b[36m%s\x1b[0m', '==========================================================');
console.log('\x1b[35m%s\x1b[0m', '   🌟 CERTCHAIN — Decentralized Certificate Verification  ');
console.log('\x1b[36m%s\x1b[0m', '==========================================================');
console.log('\x1b[32m%s\x1b[0m', '✓ Smart Contract: 0xba0553a92F82F62E62d38496398637f9CB11B37C (Sepolia)');
console.log('\x1b[33m%s\x1b[0m', '✓ Admin Login:    admin@institute.edu / admin123');
console.log('\x1b[34m%s\x1b[0m', '✓ Starting Backend API Server (Port 4000)...');
console.log('\x1b[35m%s\x1b[0m', '✓ Starting Frontend Dev Server (Port 5173)...');
console.log('\x1b[36m%s\x1b[0m', '==========================================================\n');

const isWindows = process.platform === 'win32';
const npmCmd = isWindows ? 'npm.cmd' : 'npm';

// Spawn server
const server = spawn('node', ['index.js'], {
  cwd: path.join(__dirname, 'server'),
  stdio: 'pipe',
  shell: isWindows
});

// Spawn frontend
const frontend = spawn(npmCmd, ['run', 'dev'], {
  cwd: path.join(__dirname, 'frontend'),
  stdio: 'pipe',
  shell: isWindows
});

const pipeOutput = (stream, prefix, color) => {
  stream.on('data', (data) => {
    const lines = data.toString().split('\n').filter(Boolean);
    for (const line of lines) {
      console.log(`${color}${prefix}\x1b[0m ${line}`);
    }
  });
};

pipeOutput(server.stdout, '[SERVER]', '\x1b[36m');
pipeOutput(server.stderr, '[SERVER ERR]', '\x1b[31m');
pipeOutput(frontend.stdout, '[FRONTEND]', '\x1b[35m');
pipeOutput(frontend.stderr, '[FRONTEND ERR]', '\x1b[33m');

const shutdown = () => {
  console.log('\n\x1b[33mShutting down CertChain services...\x1b[0m');
  try {
    if (isWindows) {
      if (server.pid) spawn('taskkill', ['/pid', server.pid, '/f', '/t']);
      if (frontend.pid) spawn('taskkill', ['/pid', frontend.pid, '/f', '/t']);
    } else {
      server.kill();
      frontend.kill();
    }
  } catch {}
  process.exit(0);
};

process.on('SIGINT', shutdown);
process.on('SIGTERM', shutdown);
