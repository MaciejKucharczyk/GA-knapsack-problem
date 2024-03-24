import random
import os

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
    
    return f"Generated test data in {folder_path}/ with random profits and weights."

# Parametry
item_count = 20  # ilość przedmiotów
knapsack_capacity = 200  # pojemność plecaka
profit_range = (20, 100)  # zakres wartości przedmiotów
weight_range = (10, 90)  # zakres wag przedmiotów

# Generowanie danych z losowymi zyskami i wagami
result = generate_random_test_data(item_count, knapsack_capacity, profit_range, weight_range)
result
