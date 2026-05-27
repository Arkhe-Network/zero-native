// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ERC8257ToolRegistry
 * @notice Registro permissionless de ferramentas de agentes de IA
 * @dev Implementação do EIP-8257 (Cody Sears, Ryan Ghods / OpenSea)
 * @custom:substrato 872-ERC-8257-TOOL-REGISTRY
 * @custom:cross-link 888-OWL-WEB3-BRIDGE
 * @custom:cross-link 885-REALITY-MANIFESTATION
 * @custom:cross-link 889-ERC-8257-SOLIDITY-IPFS-REALITY
 */
contract ERC8257ToolRegistry {

    struct Tool {
        string name;
        string metadataURI;      // IPFS/Arweave hash do JSON-LD SDX
        bytes32 checksum;        // SHA3-256 do conteúdo binário
        address owner;
        uint256 registeredAt;
        bool exists;
    }

    mapping(bytes32 => Tool) public tools;

    event ToolRegistered(
        bytes32 indexed toolHash,
        string name,
        string metadataURI,
        bytes32 checksum,
        address indexed owner,
        uint256 registeredAt
    );

    event ToolUpdated(
        bytes32 indexed toolHash,
        string metadataURI,
        bytes32 checksum,
        uint256 updatedAt
    );

    event ToolVerified(
        bytes32 indexed toolHash,
        address indexed verifier,
        bool valid
    );

    modifier onlyOwner(bytes32 _toolHash) {
        require(tools[_toolHash].owner == msg.sender, "ERC8257: not owner");
        _;
    }

    modifier toolExists(bytes32 _toolHash) {
        require(tools[_toolHash].exists, "ERC8257: tool not found");
        _;
    }

    function registerTool(
        string calldata _name,
        string calldata _metadataURI,
        bytes32 _checksum
    ) external returns (bytes32 toolHash) {
        toolHash = keccak256(bytes(_name));
        require(!tools[toolHash].exists, "ERC8257: tool already registered");

        tools[toolHash] = Tool({
            name: _name,
            metadataURI: _metadataURI,
            checksum: _checksum,
            owner: msg.sender,
            registeredAt: block.timestamp,
            exists: true
        });

        emit ToolRegistered(toolHash, _name, _metadataURI, _checksum, msg.sender, block.timestamp);
        return toolHash;
    }

    function updateTool(
        bytes32 _toolHash,
        string calldata _metadataURI,
        bytes32 _checksum
    ) external onlyOwner(_toolHash) toolExists(_toolHash) {
        tools[_toolHash].metadataURI = _metadataURI;
        tools[_toolHash].checksum = _checksum;
        emit ToolUpdated(_toolHash, _metadataURI, _checksum, block.timestamp);
    }

    function verifyChecksum(
        bytes32 _toolHash,
        bytes32 _expectedChecksum
    ) external view toolExists(_toolHash) returns (bool) {
        bool valid = tools[_toolHash].checksum == _expectedChecksum;
        emit ToolVerified(_toolHash, msg.sender, valid);
        return valid;
    }

    function getTool(bytes32 _toolHash) external view toolExists(_toolHash) returns (Tool memory) {
        return tools[_toolHash];
    }

    function isRegistered(bytes32 _toolHash) external view returns (bool) {
        return tools[_toolHash].exists;
    }
}