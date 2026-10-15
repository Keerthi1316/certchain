// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {Test} from "forge-std/Test.sol";
import {CertChain} from "../src/CertChain.sol";

contract CertChainTest is Test {
    CertChain c;
    address issuer = address(0xA11CE);
    address stranger = address(0xBAD);
    bytes32 constant H = keccak256("doc");

    function setUp() public { c = new CertChain(); c.addIssuer(issuer); }

    function test_issue_and_verify() public {
        vm.prank(issuer); c.issue("CERT-2026-0001", H);
        assertEq(uint(c.verify("CERT-2026-0001", H)), uint(CertChain.Status.Valid));
        assertEq(uint(c.verify("CERT-2026-0001", bytes32(0))), uint(CertChain.Status.Valid));
    }
    function test_not_found() public view {
        assertEq(uint(c.verify("nope", H)), uint(CertChain.Status.NotFound));
    }
    function test_hash_mismatch() public {
        vm.prank(issuer); c.issue("X", H);
        assertEq(uint(c.verify("X", keccak256("other"))), uint(CertChain.Status.HashMismatch));
    }
    function test_revoke() public {
        vm.prank(issuer); c.issue("X", H);
        vm.prank(issuer); c.revoke("X");
        assertEq(uint(c.verify("X", H)), uint(CertChain.Status.Revoked));
        CertChain.Certificate memory r = c.getCertificate("X");
        assertEq(r.revokedBy, issuer);
    }
    function test_owner_can_revoke() public {
        vm.prank(issuer); c.issue("X", H);
        c.revoke("X");
        assertEq(uint(c.verify("X", H)), uint(CertChain.Status.Revoked));
    }
    function test_only_issuer_can_issue() public {
        vm.prank(stranger); vm.expectRevert(CertChain.NotIssuer.selector);
        c.issue("X", H);
    }
    function test_duplicate_reverts() public {
        vm.startPrank(issuer);
        c.issue("X", H);
        vm.expectRevert(CertChain.AlreadyIssued.selector);
        c.issue("X", H);
    }
    function test_stranger_cannot_revoke() public {
        vm.prank(issuer); c.issue("X", H);
        vm.prank(stranger); vm.expectRevert(CertChain.NotAuthorizedToRevoke.selector);
        c.revoke("X");
    }
    function test_counters() public {
        assertEq(c.issuerCount(), 2);
        vm.prank(issuer); c.issue("A", H);
        vm.prank(issuer); c.issue("B", H);
        c.revoke("A");
        assertEq(c.totalIssued(), 2);
        assertEq(c.totalRevoked(), 1);
        c.removeIssuer(issuer);
        assertEq(c.issuerCount(), 1);
    }
    function test_get_unknown_returns_empty() public view {
        assertFalse(c.getCertificate("nope").exists);
    }
    function test_remove_issuer() public {
        c.removeIssuer(issuer);
        vm.prank(issuer); vm.expectRevert(CertChain.NotIssuer.selector);
        c.issue("X", H);
    }
    function test_only_owner_manages_issuers() public {
        vm.prank(stranger); vm.expectRevert(CertChain.NotOwner.selector);
        c.addIssuer(stranger);
    }
}
