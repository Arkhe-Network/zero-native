// scripts/deploy-erc8257.ts
// ═══════════════════════════════════════════════════════════════
// Deploy ERC8257ToolRegistry para Ethereum/Base
// Substrato 889 v2.0 • ARKHE Cathedral
// ═══════════════════════════════════════════════════════════════

import { ethers } from "hardhat";
import { writeFileSync } from "fs";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const ERC8257 = await ethers.getContractFactory("ERC8257ToolRegistry");
  const registry = await ERC8257.deploy();
  await registry.waitForDeployment();

  const address = await registry.getAddress();
  console.log("ERC8257 deployed to:", address);

  // Salvar artefato de deploy
  const deploymentInfo = {
    contract: "ERC8257ToolRegistry",
    address,
    network: network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    abi: ERC8257.interface.formatJson(),
    verification: {
      etherscan: `https://${network.name}.etherscan.io/address/${address}`,
      basescan: `https://basescan.org/address/${address}`
    }
  };

  writeFileSync(
    `deployments/erc8257-${network.name}.json`,
    JSON.stringify(deploymentInfo, null, 2)
  );

  // Registrar artefato ARKHE no SDX
  const sdxArtifact = {
    "@context": { "sdx": "https://arkhe.org/ontology/sdx#", "arkhe": "https://arkhe.org/ontology/841#" },
    "@type": ["sdx:Package"],
    "sdx:artifactName": "ERC8257ToolRegistry",
    "sdx:hasVersion": { "sdx:versionString": "1.0.0" },
    "sdx:publishedAt": { "sdx:repositoryURL": `https://${network.name}.etherscan.io/address/${address}` },
    "arkhe:hasSeal": { "arkhe:hashAlgorithm": "SHA3-256", "arkhe:sealHash": await registry.deploymentTransaction().hash }
  };

  writeFileSync(
    `deployments/sdx-erc8257-${network.name}.json`,
    JSON.stringify(sdxArtifact, null, 2)
  );
}

main().catch(console.error);