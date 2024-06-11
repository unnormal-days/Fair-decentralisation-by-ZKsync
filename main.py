import csv
from collections import defaultdict

# Шаг 1: Прочитать данные из файла
file_path = 'addresses.csv'  # Замените на путь к вашему файлу

addresses = []
with open(file_path, mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        address, reward = row[0], int(row[1])
        addresses.append((address, reward))

# Шаг 2: Сортировать по количеству наград
addresses.sort(key=lambda x: x[1])

# Шаг 3: Разделить на категории
categories = {
    "0-2000": [],
    "2000-5000": [],
    "5000-10000": [],
    "10000-20000": [],
    "20000-50000": [],
    "50000+": []
}

for address, reward in addresses:
    if reward < 2000:
        categories["0-2000"].append((address, reward))
    elif 2000 <= reward < 5000:
        categories["2000-5000"].append((address, reward))
    elif 5000 <= reward < 10000:
        categories["5000-10000"].append((address, reward))
    elif 10000 <= reward < 20000:
        categories["10000-20000"].append((address, reward))
    elif 20000 <= reward < 50000:
        categories["20000-50000"].append((address, reward))
    else:
        categories["50000+"].append((address, reward))

# Шаг 4: Подсчитать общее количество токенов
total_tokens = sum(reward for address, reward in addresses)

# Шаг 5: Рассчитать распределение токенов по категориям
distribution = defaultdict(lambda: {"count": 0, "tokens": 0})
for category, entries in categories.items():
    distribution[category]["count"] = len(entries)
    distribution[category]["tokens"] = sum(reward for address, reward in entries)

# Шаг 6: Вывести результаты
print(f"Общее количество распределенных токенов: {total_tokens}")
print("Распределение по категориям:")

for category, stats in distribution.items():
    count_percentage = (stats["count"] / len(addresses)) * 100
    token_percentage = (stats["tokens"] / total_tokens) * 100
    print(f"Категория {category}: {stats['count']} кошельков ({count_percentage:.2f}%), {stats['tokens']} токенов ({token_percentage:.2f}%)")
