import pytest
from copy import deepcopy
from core import (
    MobileUser,
    calculate_usage_cost,
    apply_loyalty_discount,
    calculate_user_monthly_cost,
    make_mobile_processor
)

@pytest.fixture
def sample_user() -> MobileUser:
    return {
        "id": 101,
        "name": "Тестовий Користувач",
        "plan": "Basic",
        "usage": {"minutes": 100, "sms": 10, "data_gb": 5.0},
        "bonus_points": 20
    }

def test_referential_transparency(sample_user):
    tariff = lambda u: calculate_usage_cost(u, 1.0, 0.5, 5.0)
    res1 = calculate_user_monthly_cost(sample_user, tariff, apply_loyalty_discount)
    res2 = calculate_user_monthly_cost(sample_user, tariff, apply_loyalty_discount)
    assert res1 == res2

def test_no_mutation(sample_user):
    original = deepcopy(sample_user)
    tariff = lambda u: calculate_usage_cost(u, 1.0, 0.5, 5.0)
    calculate_user_monthly_cost(sample_user, tariff, apply_loyalty_discount)
    assert sample_user == original
    assert "monthly_cost" not in sample_user

def test_callable_policies(sample_user):
    tariff = lambda u: 100.0
    discount = lambda cost, bonus: cost - bonus
    processor = make_mobile_processor(tariff, discount)
    res = processor([sample_user])
    assert res["users"][0]["monthly_cost"] == 80.0