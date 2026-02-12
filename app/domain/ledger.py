"""
Ledger entry domain model.

Ledger entries are immutable records of value movement.
"""

from dataclasses import dataclass
from uuid import UUID

from .money import Money


@dataclass(frozen=True)
class LedgerEntry:
    id: UUID
    merchant_id: UUID
    payment_id: UUID
    amount: Money
