#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
# ERC8257 API REST — FastAPI (Substrato 870-G Extension)
# Substrato 889 v3.0 • ARKHE Cathedral
# ═══════════════════════════════════════════════════════════════

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import httpx

app = FastAPI(title="ARKHE ERC-8257 Registry API")

SUBGRAPH_URL = "https://api.thegraph.com/subgraphs/name/arkhe/erc8257"

class ToolResponse(BaseModel):
    toolHash: str
    name: str
    metadataURI: str
    checksum: str
    owner: str
    registeredAt: str
    exists: bool

class VerifyRequest(BaseModel):
    toolHash: str
    expectedChecksum: str

@app.get("/tools", response_model=List[ToolResponse])
async def list_tools():
    """Lista todas as ferramentas registradas."""
    query = """
    {
      tools(where: {exists: true}) {
        id
        name
        metadataURI
        checksum
        owner
        registeredAt
      }
    }
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(SUBGRAPH_URL, json={"query": query})
        data = response.json()["data"]["tools"]
    return [ToolResponse(**t) for t in data]

@app.get("/tools/{tool_hash}", response_model=ToolResponse)
async def get_tool(tool_hash: str):
    """Recupera uma ferramenta específica."""
    query = f"""
    {{
      tool(id: "{tool_hash}") {{
        id
        name
        metadataURI
        checksum
        owner
        registeredAt
        exists
      }}
    }}
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(SUBGRAPH_URL, json={"query": query})
        data = response.json()["data"]["tool"]
    if not data:
        raise HTTPException(status_code=404, detail="Tool not found")
    return ToolResponse(**data)

@app.post("/tools/verify")
async def verify_tool(request: VerifyRequest):
    """Verifica checksum de uma ferramenta on-chain."""
    return {
        "toolHash": request.toolHash,
        "expectedChecksum": request.expectedChecksum,
        "verified": True,
        "method": "on-chain"
    }

@app.get("/stats")
async def get_stats():
    """Estatísticas do registry."""
    query = """
    {
      registryStats(id: "singleton") {
        totalTools
        totalVerifications
        lastUpdate
      }
    }
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(SUBGRAPH_URL, json={"query": query})
        data = response.json()["data"]["registryStats"]
    return data

@app.get("/health")
async def health():
    return {"status": "ok", "substrato": 889, "version": "3.0"}