"""
Balance computation logic.
"""

from typing import Iterable
from .ledger import LedgerEntry
from .money import Money


def compute_balance(entries: Iterable[LedgerEntry]) -> Money:
    entries = list(entries)

    if not entries:
        return Money(amount=0, currency="KES")

    currency = entries[0].amount.currency
    total = 0

    for entry in entries:
        if entry.amount.currency != currency:
            raise ValueError("Mixed currencies in ledger")

        total += entry.amount.amount

    return Money(amount=total, currency=currency)
