"""
Merchant domain entity.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Merchant:
    id: UUID
    name: str
    is_active: bool

    def ensure_active(self):
        if not self.is_active:
            raise ValueError("Merchant is inactive")
