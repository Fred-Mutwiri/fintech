"""
Money value object.

Represents monetary value in minor units (e.g., cents).
Prevents floating point errors.
"""

from dataclasses import dataclass


class InvalidMoneyError(Exception):
    pass


@dataclass(frozen=True)
class Money:
    amount: int  # minor units
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise InvalidMoneyError("Money amount cannot be negative")

        if not self.currency or len(self.currency) != 3:
            raise InvalidMoneyError("Currency must be ISO 4217 code")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise InvalidMoneyError("Currency mismatch")

        return Money(
            amount=self.amount + other.amount,
            currency=self.currency,
        )
