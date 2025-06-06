file_path = "ХорЕлементів.txt"
try:
        text = file.read()
except FileNotFoundError:
    exit (1)

