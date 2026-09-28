import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from pydantic import BaseModel, Field

def compute_merkle_root(hashes: List[str]) -> str:
    """Computes binary Merkle tree root hash from a list of SHA-256 hashes."""
    if not hashes:
        return hashlib.sha256(b"EMPTY_MERKLE").hexdigest()
    
    current_level = sorted(hashes)
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256((left + right).encode("utf-8")).hexdigest()
            next_level.append(combined)
        current_level = next_level
    
    return current_level[0]

class Block(BaseModel):
    index: int
    timestamp: str
    previous_hash: str
    source_hash: str
    brief_hash: str
    settings_hash: str
    outputs_hash: str
    verifier_hash: str
    merkle_root: str
    signer_identity: str
    block_hash: str = ""

    def calculate_hash(self) -> str:
        """Computes the SHA-256 block header hash."""
        header = (
            f"{self.index}|"
            f"{self.timestamp}|"
            f"{self.previous_hash}|"
            f"{self.merkle_root}|"
            f"{self.signer_identity}"
        )
        return hashlib.sha256(header.encode("utf-8")).hexdigest()

    @classmethod
    def create_block(
        cls,
        index: int,
        previous_hash: str,
        source_hash: str,
        brief_hash: str,
        settings_hash: str,
        outputs_hash: str,
        verifier_hash: str,
        signer_identity: str = "TechStack_Node_171612"
    ) -> "Block":
        merkle = compute_merkle_root([
            source_hash,
            brief_hash,
            settings_hash,
            outputs_hash,
            verifier_hash
        ])
        
        block = cls(
            index=index,
            timestamp=datetime.now(timezone.utc).isoformat(),
            previous_hash=previous_hash,
            source_hash=source_hash,
            brief_hash=brief_hash,
            settings_hash=settings_hash,
            outputs_hash=outputs_hash,
            verifier_hash=verifier_hash,
            merkle_root=merkle,
            signer_identity=signer_identity
        )
        block.block_hash = block.calculate_hash()
        return block
