from abc import ABC, abstractmethod
from typing import Dict, Any
from verimorph.brief.models import ContentBrief

class BaseGenerator(ABC):
    """
    Abstract base class for all VeriMorph format generators.
    Every format is generated from the single ContentBrief, guaranteeing fact consistency.
    """
    def __init__(self, format_name: str):
        self.format_name = format_name

    @abstractmethod
    def generate(self, brief: ContentBrief) -> Dict[str, Any]:
        """
        Takes the ContentBrief and generates the specific output format.
        Returns a dictionary containing the output content, structured payload, and claims for verification.
        """
        pass
