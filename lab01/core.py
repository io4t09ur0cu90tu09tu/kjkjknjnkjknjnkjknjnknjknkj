from typing import Any, Callable, Dict, Iterable, List, TypedDict

class Usage(TypedDict, total=False):
    minutes: float
    sms: int
    data_gb: float

class MobileUser(TypedDict, total=False):
    id: int
    name: str
    plan: str
    usage: Usage
    bonus_points: int
    monthly_cost: float

TariffRuleFn = Callable[[Usage], float]
BonusRuleFn = Callable[[float, int], float]

def calculate_usage_cost(
    usage: Usage,
    minute_rate: float = 0.8,
    sms_rate: float = 0.3,
    data_rate_per_gb: float = 10.0,
) -> float:
    """Чиста функція: обчислює базову вартість послуг за спожиті хвилини, SMS та трафік."""
    minutes = float(usage.get("minutes", 0.0))
    sms = float(usage.get("sms", 0))
    data_gb = float(usage.get("data_gb", 0.0))
    return minutes * minute_rate + sms * sms_rate + data_gb * data_rate_per_gb

def apply_loyalty_discount(cost: float, bonus_points: int) -> float:
    """Чиста функція: розраховує підсумкову вартість з урахуванням бонусів."""
    max_discount = cost * 0.3
    discount = min(bonus_points * 0.5, max_discount)
    return max(0.0, float(cost - discount))

def calculate_user_monthly_cost(
    user: MobileUser, tariff_fn: TariffRuleFn, bonus_fn: BonusRuleFn
) -> MobileUser:
    """Створює та повертає НОВИЙ словник із розрахованим полем monthly_cost, не мутуючи оригінал."""
    usage = user.get("usage", {})
    bonus_points = user.get("bonus_points", 0)

    base_cost = tariff_fn(usage)
    final_cost = bonus_fn(base_cost, bonus_points)

    return {**user, "monthly_cost": round(final_cost, 2)}

def make_mobile_processor(
    tariff_fn: TariffRuleFn, bonus_fn: BonusRuleFn
) -> Callable[[Iterable[MobileUser]], Dict[str, Any]]:
    """Фабрика функцій вищого порядку: повертає налаштований обробник списку користувачів."""
    def process(users: Iterable[MobileUser]) -> Dict[str, Any]:
        processed_users: List[MobileUser] = [
            calculate_user_monthly_cost(u, tariff_fn, bonus_fn) for u in users
        ]
        total_revenue = sum(
            float(u.get("monthly_cost", 0.0)) for u in processed_users
        )
        return {
            "count": len(processed_users),
            "total_revenue": round(total_revenue, 2),
            "users": processed_users,
        }

    return process