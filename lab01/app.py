from core import (
    MobileUser,
    calculate_usage_cost,
    apply_loyalty_discount,
    make_mobile_processor
)

def render_report(result: dict) -> None:
    print("=" * 45)
    print("      РОЗРАХУНОК МОБІЛЬНИХ ТАРИФІВ")
    print("=" * 45)
    for u in result["users"]:
        print(f"Користувач: {u['name']} (ID: {u['id']})")
        print(f"  Тариф: {u['plan']}")
        print(f"  Місячна вартість (monthly_cost): {u['monthly_cost']} грн")
        print("-" * 45)
    print(f"Усього оброблено: {result['count']} абонентів")
    print(f"Загальна виручка: {result['total_revenue']} грн")

def main():
    sample_users: list[MobileUser] = [
        {"id": 1, "name": "Олексій", "plan": "Smart", "usage": {"minutes": 150, "sms": 20, "data_gb": 12.5}, "bonus_points": 50},
        {"id": 2, "name": "Марія", "plan": "Unlim", "usage": {"minutes": 400, "sms": 5, "data_gb": 35.0}, "bonus_points": 120},
    ]
    smart_tariff = lambda u: calculate_usage_cost(u, minute_rate=0.8, sms_rate=0.3, data_rate_per_gb=10.0)
    processor = make_mobile_processor(smart_tariff, apply_loyalty_discount)
    result = processor(sample_users)
    render_report(result)

if __name__ == "__main__":
    main()