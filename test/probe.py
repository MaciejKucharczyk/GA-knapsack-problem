import os

# Wydrukuj bieżącą ścieżkę roboczą
print("Bieżąca ścieżka robocza:", os.getcwd())

# Wylistuj pliki i foldery w bieżącym katalogu
print("Zawartość katalogu:", os.listdir('.'))

# Spróbuj wylistować zawartość folderu 'data', jeśli istnieje
data_folder_path = './data'
if os.path.exists(data_folder_path):
    print(f"Zawartość folderu 'data':", os.listdir(data_folder_path))
else:
    print(f"Folder '{data_folder_path}' nie istnieje.")