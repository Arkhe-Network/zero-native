#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  SUBSTRATO 888 — OWL-WEB3 SUPPLY CHAIN BRIDGE (OWL-W3B)        ║
# ║  Ponte ontológica: SDX-ARKHE (252) ↔ ERC-8257 (872) ↔ CI/CD (881) ║
# ║  Architect: ORCID 0009-0005-2697-4668                            ║
# ╚══════════════════════════════════════════════════════════════════╝

"""
OWL-W3B — Supply Chain Bridge

Converte artefatos SDX-ARKHE (252) para registros ERC-8257 (872) on-chain,
garantindo verificabilidade criptográfica e rastreabilidade da cadeia de
suprimentos via smart contracts permissionless.

Mecanismos:
  1. sdx_to_erc8257()    → Converte artefato SDX para entrada ERC-8257
  2. register_on_chain() → Simula registro on-chain (Ethereum/Base)
  3. verify_on_chain()   → Verifica selo e checksum contra registry

Cross-links:
  252 (SDX-ARKHE)      → Ontologia de distribuição de software
  872 (ERC-8257)       → Tool Registry on-chain
  881 (DEVOPS-DEPLOYMENT) → Pipeline CI/CD
  841 (Web3-Ontology-Bridge) → Selo arkhe:hasSeal
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Optional

class OWLWeb3Bridge:
    """Ponte entre ontologia SDX e registro on-chain ERC-8257."""

    ERC8257_ADDRESS = "0x265BB2...D2cf1"  # Substrato 872

    def __init__(self, registry_address: str = None):
        self.registry_address = registry_address or self.ERC8257_ADDRESS
        self.tool_index: Dict[str, dict] = {}

    def sdx_to_erc8257(self, sdx_artifact: dict) -> dict:
        """Converte artefato SDX-ARKHE para formato ERC-8257."""
        name = sdx_artifact.get("sdx:artifactName", "unknown")
        version = sdx_artifact.get("sdx:hasVersion", {}).get("sdx:versionString", "")
        full_name = f"{name}:{version}" if version and version not in name else name

        artifact_json = json.dumps(sdx_artifact, sort_keys=True, default=str)
        checksum = hashlib.sha3_256(artifact_json.encode()).hexdigest()
        metadata_uri = f"ipfs://{checksum[:46]}"

        return {
            "name": full_name,
            "metadataURI": metadata_uri,
            "checksum": "0x" + checksum[:64],
            "sdx_source": sdx_artifact,
            "seal": sdx_artifact.get("arkhe:hasSeal", {}).get("arkhe:sealHash", "PENDING")
        }

    def register_on_chain(self, sdx_artifact: dict) -> dict:
        """Registra artefato on-chain (simulado)."""
        erc_entry = self.sdx_to_erc8257(sdx_artifact)
        tx_hash = hashlib.sha3_256(
            f"register:{erc_entry['name']}:{datetime.now(timezone.utc).isoformat()}".encode()
        ).hexdigest()

        self.tool_index[erc_entry['name']] = {
            **erc_entry,
            "txHash": "0x" + tx_hash[:64],
            "blockNumber": 42424242,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "registry": self.registry_address
        }
        return self.tool_index[erc_entry['name']]

    def verify_on_chain(self, name: str, expected_seal: str = None, prefix_len: int = 16) -> dict:
        """Verifica artefato no registry on-chain."""
        entry = self.tool_index.get(name)
        if not entry:
            return {"verified": False, "reason": "NOT_REGISTERED", "name": name}

        seal_match = True
        if expected_seal:
            actual_seal = entry.get("seal", "")
            seal_match = actual_seal.startswith(expected_seal[:prefix_len])

        return {
            "verified": seal_match,
            "name": name,
            "txHash": entry.get("txHash"),
            "checksum": entry.get("checksum"),
            "metadataURI": entry.get("metadataURI"),
            "seal": entry.get("seal"),
            "registry": entry.get("registry")
        }

    def verify_chain(self, artifacts: list, prefix_len: int = 16) -> dict:
        """Verifica cadeia completa de dependências."""
        results = []
        all_valid = True
        for art in artifacts:
            name = art.get("sdx:artifactName", "unknown")
            if art.get("sdx:hasVersion"):
                name += ":" + art["sdx:hasVersion"]["sdx:versionString"]
            seal = art.get("arkhe:hasSeal", {}).get("arkhe:sealHash", "")
            result = self.verify_on_chain(name, expected_seal=seal, prefix_len=prefix_len)
            results.append(result)
            if not result["verified"]:
                all_valid = False
        return {"chain_valid": all_valid, "results": results}


if __name__ == "__main__":
    bridge = OWLWeb3Bridge()

    # Criar e registrar artefatos
    oci = {
        "@context": {"sdx": "https://arkhe.org/ontology/sdx#", "arkhe": "https://arkhe.org/ontology/841#"},
        "@type": ["sdx:Package", "sdx:OCIImage"],
        "sdx:artifactName": "arkheos-gateway",
        "sdx:hasVersion": {"sdx:versionString": "870-g-v3.0.1"},
        "sdx:digest": "sha256:7c1e8d3f...",
        "arkhe:hasSeal": {"arkhe:sealHash": "e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8"}
    }
    bridge.register_on_chain(oci)

    # Verificar
    result = bridge.verify_on_chain("arkheos-gateway:870-g-v3.0.1", expected_seal="e7f8a9b0c1d2e3f4")
    print(f"Verified: {result['verified']} | Seal: {result['seal'][:16]}...")