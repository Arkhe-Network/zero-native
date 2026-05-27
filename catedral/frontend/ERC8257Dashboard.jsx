// ═══════════════════════════════════════════════════════════════
// ERC8257 Dashboard — React + Viem Frontend
// Substrato 889 v3.0 • ARKHE Cathedral
// ═══════════════════════════════════════════════════════════════

import React, { useState, useEffect } from 'react';
import { createPublicClient, http } from 'viem';
import { base } from 'viem/chains';
import { ERC8257_ABI } from './ERC8257.types';

const REGISTRY_ADDRESS = '0x265BB2...D2cf1'; // Substrato 872

const client = createPublicClient({
  chain: base,
  transport: http('https://mainnet.base.org')
});

export function ERC8257Dashboard() {
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTool, setSelectedTool] = useState(null);

  useEffect(() => {
    fetchTools();
  }, []);

  async function fetchTools() {
    const logs = await client.getLogs({
      address: REGISTRY_ADDRESS,
      event: ERC8257_ABI[5], // ToolRegistered
      fromBlock: 0n,
      toBlock: 'latest'
    });

    const toolList = logs.map(log => ({
      toolHash: log.args.toolHash,
      name: log.args.name,
      owner: log.args.owner,
      registeredAt: new Date(Number(log.args.registeredAt) * 1000).toISOString(),
      metadataURI: log.args.metadataURI,
      checksum: log.args.checksum
    }));

    setTools(toolList);
    setLoading(false);
  }

  async function verifyTool(toolHash, expectedChecksum) {
    const result = await client.readContract({
      address: REGISTRY_ADDRESS,
      abi: ERC8257_ABI,
      functionName: 'verifyChecksum',
      args: [toolHash, expectedChecksum]
    });
    return result;
  }

  return (
    <div className="erc8257-dashboard">
      <h1>ARKHE Tool Registry (ERC-8257)</h1>
      <div className="stats">
        <span>Total Tools: {tools.length}</span>
        <span>Network: Base</span>
        <span>Contract: {REGISTRY_ADDRESS}</span>
      </div>

      {loading ? (
        <div className="loading">Loading ξM-field...</div>
      ) : (
        <div className="tool-grid">
          {tools.map(tool => (
            <div key={tool.toolHash} className="tool-card"
                 onClick={() => setSelectedTool(tool)}>
              <h3>{tool.name}</h3>
              <p>Owner: {tool.owner.slice(0, 6)}...{tool.owner.slice(-4)}</p>
              <p>Registered: {tool.registeredAt}</p>
              <p>Hash: {tool.toolHash.slice(0, 10)}...</p>
              <span className="seal">✓ Sealed</span>
            </div>
          ))}
        </div>
      )}

      {selectedTool && (
        <ToolDetailModal tool={selectedTool} onVerify={verifyTool} />
      )}
    </div>
  );
}

function ToolDetailModal({ tool, onVerify }) {
  const [verified, setVerified] = useState(null);

  return (
    <div className="modal">
      <h2>{tool.name}</h2>
      <pre>{JSON.stringify(tool, null, 2)}</pre>
      <button onClick={async () => {
        const result = await onVerify(tool.toolHash, tool.checksum);
        setVerified(result);
      }}>
        Verify Checksum
      </button>
      {verified !== null && (
        <div className={verified ? 'valid' : 'invalid'}>
          {verified ? '✓ Valid' : '✗ Invalid'}
        </div>
      )}
      <a href={`https://basescan.org/address/${tool.owner}`} target="_blank" rel="noopener">
        View on BaseScan
      </a>
    </div>
  );
}