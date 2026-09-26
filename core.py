from typing import Callable


TariffFn = Callable[[str], float]


DiscountFn = Callable[[float], float]


def consumption(old: float, new: float) -> float:

    return new - old




def calculate_sum(consumption_value: float, tariff: float) -> float:


    return consumption_value * tariff


def tariff(group: str) -> float:

    if group == "student":
        return 3.5
    return 4.32




def discount(sum_value: float) -> float:
    return sum_value * 0.9


def make_bill(
        old: float,
        new: float,
        group: str,
        tariff_fn: TariffFn,
        discount_fn: DiscountFn
) -> dict[str, float]:

    used = consumption(old, new)
    price = tariff_fn(group)
    total = calculate_sum(used, price)
    final_sum = discount_fn(total)

    return {
        "consumption": used,
        "sum": total,
        "final_sum": final_sum
    }