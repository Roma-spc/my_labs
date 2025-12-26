import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tools import survived, died, calculate_surv_rate

data = pd.read_csv("data.csv", index_col=False)

s = survived(data)
d = died(data)

print(f"Осіб вижило: {len(s)};\nОсіб померло: {len(d)};\n\n")

translator = {1: "Перший", 2: "Другий", 3: "Третій"}
for pclass in range(1,4):
    some_class = data[data["Pclass"] == pclass]
    info_about_class = calculate_surv_rate(some_class)

    print( f"{translator[pclass]} клас:\n- {info_about_class[0]} вижило.\n- {info_about_class[1]} померло.")
    print(f"- Процент виживання: {info_about_class[2] * 100:.3f} %.")

print("\n")


translator = {30: "молодих", 60: "людей середнього віку"}
for group_age in range(30, 91, 30):
    group = data[(data["Age"] >= group_age - 30) & (data["Age"] < group_age)]

    info_about_group = calculate_surv_rate(group)

    print(f"Для {translator.get(group_age, "людей старшого віку ()")}:")
    print(f"- {info_about_group[0]} вижило.\n- {info_about_group[1]} померло.")
    print(f"- Процент виживання: {info_about_group[2] * 100:.3f} %.")

without_age = data[data["Age"].isna()]
info_about_group = calculate_surv_rate(without_age)

print(f"Люди невідомого віку")
print(f"- {info_about_group[0]} вижило.\n- {info_about_group[1]} померло.")
print(f"- Процент виживання: {info_about_group[2] * 100:.3f} %.", end="\n\n\n")

for port, count in data["Embarked"].value_counts().items():
    print(f"{port}: {count}")

data.boxplot(column="Fare", by="Pclass", vert=False)


plt.xlabel("Ціна за човен")
plt.ylabel("Клас пасажира")
plt.suptitle("")
plt.title("Розподіл ціни квитка для кожного класу")

plt.show()


print(f"\nСередня вартість квитка {data["Fare"].mean():.3f} фунтів.")