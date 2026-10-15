// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;
import {Script, console} from "forge-std/Script.sol";
import {CertChain} from "../src/CertChain.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();
        CertChain c = new CertChain();
        vm.stopBroadcast();
        console.log("CertChain deployed at:", address(c));
    }
}
