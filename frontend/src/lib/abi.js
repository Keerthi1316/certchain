export const ABI = [
  'function owner() view returns (address)',
  'function isIssuer(address) view returns (bool)',
  'function issuerCount() view returns (uint256)',
  'function totalIssued() view returns (uint256)',
  'function totalRevoked() view returns (uint256)',
  'function addIssuer(address a)',
  'function removeIssuer(address a)',
  'function issue(string certId, bytes32 docHash)',
  'function revoke(string certId)',
  'function verify(string certId, bytes32 docHash) view returns (uint8)',
  'function getCertificate(string certId) view returns (tuple(bytes32 docHash, address issuer, uint64 issuedAt, uint64 revokedAt, address revokedBy, bool exists))',
];
