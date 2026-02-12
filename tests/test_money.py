import pytest
from app.domain.money import Money, InvalidMoneyError


def test_money_creation():
    m = Money(amount=1000, currency="KES")
    assert m.amount == 1000


def test_negative_money():
    with pytest.raises(InvalidMoneyError):
        Money(amount=-1, currency="KES")
