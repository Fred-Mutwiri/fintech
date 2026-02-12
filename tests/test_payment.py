import uuid
import pytest

from app.domain.payment import Payment, PaymentStatus, InvalidPaymentTransition
from app.domain.money import Money


def test_authorize_transition():
    p = Payment(
        id=uuid.uuid4(),
        merchant_id=uuid.uuid4(),
        amount=Money(1000, "KES"),
        status=PaymentStatus.PENDING,
    )

    authorized = p.authorize()
    assert authorized.status == PaymentStatus.AUTHORIZED


def test_invalid_capture():
    p = Payment(
        id=uuid.uuid4(),
        merchant_id=uuid.uuid4(),
        amount=Money(1000, "KES"),
        status=PaymentStatus.PENDING,
    )

    with pytest.raises(InvalidPaymentTransition):
        p.capture()
