from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class Fact(BaseModel):
    fact_id: str
    statement: str
    source_chunk_id: int
    source_passage: str
    confidence: float = 1.0

class Entity(BaseModel):
    name: str
    entity_type: str  # e.g., "CVE", "MALWARE", "IP_IOC", "ORGANIZATION", "LOCATION", "METRIC", "SYSTEM"
    context: Optional[str] = None

class ActionItem(BaseModel):
    action_id: str
    title: str
    description: str
    priority: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW
    timeframe: str = "Immediate"

class KeyMetric(BaseModel):
    label: str
    value: str
    context: Optional[str] = None

class ContentBrief(BaseModel):
    brief_id: str
    source_title: str
    source_digest: str  # SHA-256 of raw source
    intent_and_objective: str
    core_summary: str
    facts: List[Fact] = Field(default_factory=list)
    entities: List[Entity] = Field(default_factory=list)
    actions: List[ActionItem] = Field(default_factory=list)
    metrics: List[KeyMetric] = Field(default_factory=list)
    operator_settings: Dict[str, Any] = Field(default_factory=dict)
    created_at: str
