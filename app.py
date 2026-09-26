from core import make_bill, tariff, discount


bill = make_bill(
    1250,
    1380,
    "student",
    tariff,
    discount
)

print("Квитанція за електроенергію")
print("Споживання:", bill["consumption"], "кВт·год")
print("Сума:", bill["sum"], "грн")
print("До оплати:", bill["final_sum"], "грн")