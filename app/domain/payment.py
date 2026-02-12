"""
Payment domain model and state transitions.
"""

from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from .money import Money


class PaymentStatus(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"


class InvalidPaymentTransition(Exception):
    pass


@dataclass(frozen=True)
class Payment:
    id: UUID
    merchant_id: UUID
    amount: Money
    status: PaymentStatus

    def authorize(self) -> "Payment":
        if self.status != PaymentStatus.PENDING:
            raise InvalidPaymentTransition("Only pending payments can be authorized")

        return Payment(
            id=self.id,
            merchant_id=self.merchant_id,
            amount=self.amount,
            status=PaymentStatus.AUTHORIZED,
        )

    def capture(self) -> "Payment":
        if self.status != PaymentStatus.AUTHORIZED:
            raise InvalidPaymentTransition("Only authorized payments can be captured")

        return Payment(
            id=self.id,
            merchant_id=self.merchant_id,
            amount=self.amount,
            status=PaymentStatus.CAPTURED,
        )

    def fail(self) -> "Payment":
        if self.status not in {PaymentStatus.PENDING, PaymentStatus.AUTHORIZED}:
            raise InvalidPaymentTransition("Invalid failure transition")

        return Payment(
            id=self.id,
            merchant_id=self.merchant_id,
            amount=self.amount,
            status=PaymentStatus.FAILED,
        )
