file_path = "ХорЕлементів.txt"
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print (f"Помилка: Файл '{file_path}' не знайдено. Переконайтеся, що файл інсує в правельній дерикторії.")
    exit (1)

