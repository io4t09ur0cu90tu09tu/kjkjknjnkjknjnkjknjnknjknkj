from typing import Callable, List, Dict, Any, TypedDict

class Usage(TypedDict):
    minutes: float
    sms: int
    data_gb: float

class MobileUser(TypedDict):
    id: int
    name: str
    plan: str
    usage: Usage
    bonus_points: int

TariffRuleFn = Callable[[Usage], float]
BonusRuleFn = Callable[[float, int], float]

def calculate_usage_cost(usage: Usage, minute_rate: float, sms_rate: float, data_rate_per_gb: float) -> float:
    """Обчислює базову вартість спожитих послуг без мутації даних."""
    return (
        usage["minutes"] * minute_rate
        + usage["sms"] * sms_rate
        + usage["data_gb"] * data_rate_per_gb
    )

def apply_loyalty_discount(cost: float, bonus_points: int) -> float:
    """Застосовує знижку за бонуси (1 бонус = 0.5 грн знижки, але не більше 30% суми)."""
    max_discount = cost * 0.3
    discount = min(bonus_points * 0.5, max_discount)
    return max(0.0, cost - discount)

def calculate_user_monthly_cost(
    user: MobileUser,
    tariff_fn: TariffRuleFn,
    bonus_fn: BonusRuleFn
) -> MobileUser:
    """Створює НОВИЙ словник користувача із розрахованим полем monthly_cost."""
    base_cost = tariff_fn(user["usage"])
    final_cost = bonus_fn(base_cost, user["bonus_points"])
    
    # Створення нового об'єкта без мутації оригінального
    return {
        **user,
        "monthly_cost": round(final_cost, 2)
    }

def make_mobile_processor(
    tariff_fn: TariffRuleFn,
    bonus_fn: BonusRuleFn
) -> Callable[[List[MobileUser]], Dict[str, Any]]:
    """Фабрика функцій вищого порядку для обробки списку користувачів."""
    def process(users: List[MobileUser]) -> Dict[str, Any]:
        processed_users = [
            calculate_user_monthly_cost(u, tariff_fn, bonus_fn)
            for u in users
        ]
        total_revenue = sum(u["monthly_cost"] for u in processed_users)
        return {
            "count": len(processed_users),
            "total_revenue": round(total_revenue, 2),
            "users": processed_users
        }
    return process