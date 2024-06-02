import random
import os

def knapsack(profits, weights, capacity):
    n = len(profits)
    dp = [[0 for x in range(capacity + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif weights[i - 1] <= w:
                dp[i][w] = max(profits[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]

    # Finding the items included in the optimal solution
    w = capacity
    included = [0] * n
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            included[i - 1] = 1
            w -= weights[i - 1]
    
    return included

def generate_random_test_data(item_count, knapsack_capacity, profit_range, weight_range):
    # Generowanie losowych zysków i wag
    profits = [random.randint(*profit_range) for _ in range(item_count)]
    weights = [random.randint(*weight_range) for _ in range(item_count)]
    
    # Tworzenie nazwy folderu
    folder_name = f"w{item_count}c{knapsack_capacity}"
    folder_path = f"./data/{folder_name}"
    
    # Tworzenie folderu, jeśli nie istnieje
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Tworzenie i zapisywanie plików
    with open(os.path.join(folder_path, "profits.txt"), "w") as f:
        f.writelines(f"{profit}\n" for profit in profits)
    
    with open(os.path.join(folder_path, "size.txt"), "w") as f:
        f.write(f"{knapsack_capacity}\n")
    
    with open(os.path.join(folder_path, "weights.txt"), "w") as f:
        f.writelines(f"{weight}\n" for weight in weights)
    
    # Znalezienie optymalnego rozwiązania
    included_items = knapsack(profits, weights, knapsack_capacity)
    
    # Zapisywanie optymalnego rozwiązania do pliku
    with open(os.path.join(folder_path, "optimal.txt"), "w") as f:
        f.writelines(f"{item}\n" for item in included_items)
    
    return f"Generated test data in {folder_path}/ with random profits, weights, and optimal solution."

# Parametry
item_count = 20  # ilość przedmiotów
knapsack_capacity = 200  # pojemność plecaka
profit_range = (20, 100)  # zakres wartości przedmiotów
weight_range = (10, 90)  # zakres wag przedmiotów

# Generowanie danych z losowymi zyskami i wagami oraz optymalnym rozwiązaniem
result = generate_random_test_data(item_count, knapsack_capacity, profit_range, weight_range)
print(result)
