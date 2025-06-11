try:
    num1 = float(input("Введіть перше число: "))
    num2 = float(input("Введіть друге число: "))

    if num2 == 0:
        print("Помилка: ділення на нуль")
    else:
        result = num1 / num2
        print(f"Результат: {result:.2f}")

except ValueError:
    print("Помилка: введіть число")