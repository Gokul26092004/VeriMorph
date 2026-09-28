import hashlib
import json
import os
from typing import List, Dict, Any, Tuple
from .block import Block, compute_merkle_root

class ProvenanceLedger:
    """
    Hash-chained tamper-proof ledger modeled after permissioned Hyperledger Fabric / C2PA specs.
    Tracks transformation provenance from source document to verified deliverables.
    """
    def __init__(self, persistence_path: str = None):
        self.persistence_path = persistence_path
        self.chain: List[Block] = []
        self._initialize_chain()

    def _initialize_chain(self):
        if self.persistence_path and os.path.exists(self.persistence_path):
            self.load()
        else:
            # Mint Genesis Block (Block 0)
            genesis = Block(
                index=0,
                timestamp="2026-09-28T00:00:00Z",
                previous_hash="0" * 64,
                source_hash=hashlib.sha256(b"VERIMORPH_GENESIS_SOURCE").hexdigest(),
                brief_hash=hashlib.sha256(b"VERIMORPH_GENESIS_BRIEF").hexdigest(),
                settings_hash=hashlib.sha256(b"VERIMORPH_GENESIS_SETTINGS").hexdigest(),
                outputs_hash=hashlib.sha256(b"VERIMORPH_GENESIS_OUTPUTS").hexdigest(),
                verifier_hash=hashlib.sha256(b"VERIMORPH_GENESIS_VERIFIER").hexdigest(),
                merkle_root=hashlib.sha256(b"VERIMORPH_GENESIS_MERKLE").hexdigest(),
                signer_identity="Genesis_System_TechStack_171612"
            )
            genesis.block_hash = genesis.calculate_hash()
            self.chain = [genesis]

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def record_transformation(
        self,
        source_content: str,
        brief_data: Dict[str, Any],
        settings_data: Dict[str, Any],
        outputs_data: Dict[str, Any],
        verifier_report: Dict[str, Any],
        signer: str = "TechStack_Operator_171612"
    ) -> Block:
        """
        Mints a new cryptographic provenance block on the ledger.
        """
        source_hash = hashlib.sha256(source_content.encode("utf-8")).hexdigest()
        brief_hash = hashlib.sha256(json.dumps(brief_data, sort_keys=True).encode("utf-8")).hexdigest()
        settings_hash = hashlib.sha256(json.dumps(settings_data, sort_keys=True).encode("utf-8")).hexdigest()
        outputs_hash = hashlib.sha256(json.dumps(outputs_data, sort_keys=True).encode("utf-8")).hexdigest()
        verifier_hash = hashlib.sha256(json.dumps(verifier_report, sort_keys=True).encode("utf-8")).hexdigest()

        new_block = Block.create_block(
            index=len(self.chain),
            previous_hash=self.latest_block.block_hash,
            source_hash=source_hash,
            brief_hash=brief_hash,
            settings_hash=settings_hash,
            outputs_hash=outputs_hash,
            verifier_hash=verifier_hash,
            signer_identity=signer
        )

        self.chain.append(new_block)
        if self.persistence_path:
            self.save()

        return new_block

    def verify_integrity(self) -> Tuple[bool, str]:
        """
        Validates cryptographic link across all blocks in the ledger.
        Returns (is_valid: bool, status_message: str).
        """
        if not self.chain:
            return (False, "Ledger chain is empty.")

        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # 1. Check recalculation of block hash
            expected_hash = curr.calculate_hash()
            if curr.block_hash != expected_hash:
                return (False, f"Block #{curr.index} hash mismatch. Computed: {expected_hash}, Stored: {curr.block_hash}")

            # 2. Check previous hash pointer
            if curr.previous_hash != prev.block_hash:
                return (False, f"Block #{curr.index} previous_hash link broken. Expected {prev.block_hash}, Found: {curr.previous_hash}")

            # 3. Check Merkle root integrity
            expected_merkle = compute_merkle_root([
                curr.source_hash,
                curr.brief_hash,
                curr.settings_hash,
                curr.outputs_hash,
                curr.verifier_hash
            ])
            if curr.merkle_root != expected_merkle:
                return (False, f"Block #{curr.index} Merkle root tampered.")

        return (True, f"Ledger integrity verified: All {len(self.chain)} blocks cryptographically validated.")

    def get_chain_dict(self) -> List[Dict[str, Any]]:
        return [b.model_dump() for b in self.chain]

    def save(self):
        if not self.persistence_path:
            return
        os.makedirs(os.path.dirname(os.path.abspath(self.persistence_path)), exist_ok=True)
        with open(self.persistence_path, "w", encoding="utf-8") as f:
            json.dump([b.model_dump() for b in self.chain], f, indent=2)

    def load(self):
        if not self.persistence_path or not os.path.exists(self.persistence_path):
            return
        with open(self.persistence_path, "r", encoding="utf-8") as f:
            raw_blocks = json.load(f)
            self.chain = [Block(**b) for b in raw_blocks]
