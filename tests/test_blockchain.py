import pytest
from verimorph.ledger import ProvenanceLedger, Block

def test_ledger_genesis_and_minting():
    ledger = ProvenanceLedger()
    assert len(ledger.chain) >= 1
    assert ledger.chain[0].index == 0
    assert ledger.chain[0].previous_hash == "0" * 64

    # Mint a block
    block = ledger.record_transformation(
        source_content="Source raw content",
        brief_data={"title": "Brief 1"},
        settings_data={"tone": "Urgent"},
        outputs_data={"advisory": "Output content"},
        verifier_report={"score": 95.0},
        signer="TestSigner_001"
    )

    assert block.index == 1
    assert len(block.block_hash) == 64
    assert block.previous_hash == ledger.chain[0].block_hash

    is_valid, msg = ledger.verify_integrity()
    assert is_valid is True

def test_ledger_tamper_detection():
    ledger = ProvenanceLedger()
    ledger.record_transformation(
        source_content="Doc 1",
        brief_data={},
        settings_data={},
        outputs_data={},
        verifier_report={}
    )

    # Tamper with block 1 payload
    ledger.chain[1].source_hash = "tampered_hash_0000000000000000000000000000000000000000000000000"
    is_valid, msg = ledger.verify_integrity()
    assert is_valid is False
    assert "tampered" in msg.lower() or "mismatch" in msg.lower()
