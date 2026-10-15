// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title CertChain — on-chain certificate registry with issuer roles
/// @notice Stores a SHA-256 document hash per certificate ID. Personal data stays off-chain.
contract CertChain {
    enum Status { NotFound, Valid, Revoked, HashMismatch }

    struct Certificate {
        bytes32 docHash;
        address issuer;
        uint64 issuedAt;
        uint64 revokedAt;
        address revokedBy;
        bool exists;
    }

    address public owner;
    mapping(address => bool) public isIssuer;
    uint256 public issuerCount;
    uint256 public totalIssued;
    uint256 public totalRevoked;
    mapping(bytes32 => Certificate) private certs; // key = keccak256(bytes(certId))

    event IssuerAdded(address indexed issuer);
    event IssuerRemoved(address indexed issuer);
    event CertificateIssued(string certId, bytes32 indexed key, bytes32 docHash, address indexed issuer);
    event CertificateRevoked(string certId, bytes32 indexed key, address indexed revokedBy);
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    error NotOwner();
    error NotIssuer();
    error AlreadyIssued();
    error NotFound();
    error AlreadyRevoked();
    error EmptyInput();
    error NotAuthorizedToRevoke();

    modifier onlyOwner() { if (msg.sender != owner) revert NotOwner(); _; }
    modifier onlyIssuer() { if (!isIssuer[msg.sender]) revert NotIssuer(); _; }

    constructor() {
        owner = msg.sender;
        isIssuer[msg.sender] = true;
        issuerCount = 1;
        emit OwnershipTransferred(address(0), msg.sender);
        emit IssuerAdded(msg.sender);
    }

    // ---------- admin ----------
    function addIssuer(address a) external onlyOwner {
        if (!isIssuer[a]) { isIssuer[a] = true; issuerCount++; }
        emit IssuerAdded(a);
    }
    function removeIssuer(address a) external onlyOwner {
        if (isIssuer[a]) { isIssuer[a] = false; issuerCount--; }
        emit IssuerRemoved(a);
    }
    function transferOwnership(address n) external onlyOwner {
        emit OwnershipTransferred(owner, n);
        owner = n;
        if (!isIssuer[n]) { isIssuer[n] = true; issuerCount++; }
    }

    // ---------- issuing ----------
    function issue(string calldata certId, bytes32 docHash) external onlyIssuer {
        if (bytes(certId).length == 0 || docHash == bytes32(0)) revert EmptyInput();
        bytes32 key = keccak256(bytes(certId));
        if (certs[key].exists) revert AlreadyIssued();
        certs[key] = Certificate(docHash, msg.sender, uint64(block.timestamp), 0, address(0), true);
        totalIssued++;
        emit CertificateIssued(certId, key, docHash, msg.sender);
    }

    /// @notice Original issuer or the owner may revoke.
    function revoke(string calldata certId) external {
        bytes32 key = keccak256(bytes(certId));
        Certificate storage c = certs[key];
        if (!c.exists) revert NotFound();
        if (c.revokedAt != 0) revert AlreadyRevoked();
        if (msg.sender != c.issuer && msg.sender != owner) revert NotAuthorizedToRevoke();
        c.revokedBy = msg.sender;
        c.revokedAt = uint64(block.timestamp);
        totalRevoked++;
        emit CertificateRevoked(certId, key, msg.sender);
    }

    // ---------- verification ----------
    /// @param docHash pass bytes32(0) to skip the document-integrity comparison
    function verify(string calldata certId, bytes32 docHash) external view returns (Status) {
        Certificate storage c = certs[keccak256(bytes(certId))];
        if (!c.exists) return Status.NotFound;
        if (c.revokedAt != 0) return Status.Revoked;
        if (docHash != bytes32(0) && docHash != c.docHash) return Status.HashMismatch;
        return Status.Valid;
    }

    function getCertificate(string calldata certId) external view returns (Certificate memory) {
        return certs[keccak256(bytes(certId))];
    }
}
