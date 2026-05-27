// ═══════════════════════════════════════════════════════════════
// ERC8257 Mapping — AssemblyScript
// Substrato 889.2 • ARKHE Cathedral
// ═══════════════════════════════════════════════════════════════

import { BigInt } from '@graphprotocol/graph-ts';
import {
  ToolRegistered,
  ToolUpdated,
  ToolVerified
} from '../generated/ERC8257ToolRegistry/ERC8257ToolRegistry';
import { Tool, Verification, RegistryStats } from '../generated/schema';

export function handleToolRegistered(event: ToolRegistered): void {
  let tool = new Tool(event.params.toolHash.toHex());
  tool.name = event.params.name;
  tool.metadataURI = event.params.metadataURI;
  tool.checksum = event.params.checksum;
  tool.owner = event.params.owner;
  tool.registeredAt = event.params.registeredAt;
  tool.updatedAt = event.params.registeredAt;
  tool.exists = true;
  tool.save();

  let stats = RegistryStats.load('singleton');
  if (!stats) {
    stats = new RegistryStats('singleton');
    stats.totalTools = BigInt.zero();
    stats.totalVerifications = BigInt.zero();
  }
  stats.totalTools = stats.totalTools.plus(BigInt.fromI32(1));
  stats.lastUpdate = event.block.timestamp;
  stats.save();
}

export function handleToolUpdated(event: ToolUpdated): void {
  let tool = Tool.load(event.params.toolHash.toHex());
  if (tool) {
    tool.metadataURI = event.params.metadataURI;
    tool.checksum = event.params.checksum;
    tool.updatedAt = event.params.updatedAt;
    tool.save();
  }
}

export function handleToolVerified(event: ToolVerified): void {
  let verification = new Verification(
    event.transaction.hash.toHex() + '-' + event.logIndex.toString()
  );
  verification.tool = event.params.toolHash.toHex();
  verification.verifier = event.params.verifier;
  verification.valid = event.params.valid;
  verification.timestamp = event.block.timestamp;
  verification.save();

  let stats = RegistryStats.load('singleton');
  if (stats) {
    stats.totalVerifications = stats.totalVerifications.plus(BigInt.fromI32(1));
    stats.lastUpdate = event.block.timestamp;
    stats.save();
  }
}