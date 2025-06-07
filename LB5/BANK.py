import datetime

class Transaction:
    """Клас для зберігання інформації про транзакцію."""
    def __init__(self, transaction_id, type, amount, date, description=""):
        self.transaction_id = transaction_id
        self.type = type # 'deposit', 'withdrawal'
        self.amount = amount
        self.date = date # datetime.datetime object
        self.description = description

    def __str__(self):
        return (f"ID: {self.transaction_id}, Тип: {self.type}, "
                f"Сума: {self.amount:.2f} грн, Дата: {self.date.strftime('%Y-%m-%d %H:%M')}, "
                f"Опис: {self.description}")

class BankAccount:
    """Клас, який представляє банківський рахунок."""
    _next_transaction_id = 1

    def __init__(self, account_number, initial_balance=0.0):
        if not isinstance(account_number, str) or not account_number.isdigit():
            raise ValueError("Номер рахунку має бути рядком, що містить тільки цифри.")
        if initial_balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")

        self.account_number = account_number
        self.balance = initial_balance
        self.transaction_history = [] # Список об'єктів Transaction

    def get_balance(self):
        """Повертає поточний баланс рахунку."""
        return self.balance

    def deposit(self, amount, description=""):
        """Нараховує кошти на рахунок."""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Сума поповнення має бути додатним числом.")
        self.balance += amount
        transaction = Transaction(
            BankAccount._next_transaction_id,
            'deposit',
            amount,
            datetime.datetime.now(),
            description
        )
        self.transaction_history.append(transaction)
        BankAccount._next_transaction_id += 1
        print(f"Рахунок {self.account_number}: Нараховано {amount:.2f} грн. Новий баланс: {self.balance:.2f} грн.")
        return True

    def withdraw(self, amount, description=""):
        """Списує кошти з рахунку."""
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Сума списання має бути додатним числом.")
        if self.balance < amount:
            print(f"Недостатньо коштів на рахунку {self.account_number} для списання {amount:.2f} грн. Поточний баланс: {self.balance:.2f} грн.")
            return False
        self.balance -= amount
        transaction = Transaction(
            BankAccount._next_transaction_id,
            'withdrawal',
            amount,
            datetime.datetime.now(),
            description
        )
        self.transaction_history.append(transaction)
        BankAccount._next_transaction_id += 1
        print(f"Рахунок {self.account_number}: Списано {amount:.2f} грн. Новий баланс: {self.balance:.2f} грн.")
        return True

    def get_transaction_history(self):
        """Повертає історію транзакцій."""
        return self.transaction_history

    def __str__(self):
        return f"Рахунок №{self.account_number}, Баланс: {self.balance:.2f} грн"

class Bank:
    """Клас для керування банківськими рахунками."""
    def __init__(self, name):
        self.name = name
        self.accounts = {} # dict: {account_number: BankAccount object}

    def add_account(self, account_number, initial_balance=0.0):
        """Додає новий банківський рахунок."""
        if account_number in self.accounts:
            print(f"Рахунок з номером {account_number} вже існує.")
            return None
        try:
            account = BankAccount(account_number, initial_balance)
            self.accounts[account_number] = account
            print(f"Рахунок {account_number} успішно додано з початковим балансом {initial_balance:.2f} грн.")
            return account
        except ValueError as e:
            print(f"Помилка при додаванні рахунку: {e}")
            return None

    def find_account(self, account_number):
        """Шукає рахунок за номером."""
        return self.accounts.get(account_number)

    def delete_account(self, account_number):
        """Видаляє рахунок за номером."""
        if account_number not in self.accounts:
            print(f"Рахунок з номером {account_number} не знайдений.")
            return False
        del self.accounts[account_number]
        print(f"Рахунок {account_number} успішно видалено.")
        return True

    def perform_transfer(self, from_account_number, to_account_number, amount):
        """Здійснює переказ коштів між рахунками."""
        from_account = self.find_account(from_account_number)
        to_account = self.find_account(to_account_number)

        if not from_account:
            print(f"Відправник: Рахунок {from_account_number} не знайдений.")
            return False
        if not to_account:
            print(f"Отримувач: Рахунок {to_account_number} не знайдений.")
            return False
        if from_account_number == to_account_number:
            print("Неможливо переказати кошти на той самий рахунок.")
            return False
        if not isinstance(amount, (int, float)) or amount <= 0:
            print("Сума переказу має бути додатним числом.")
            return False

        if from_account.withdraw(amount, f"Переказ на рахунок {to_account_number}"):
            to_account.deposit(amount, f"Переказ з рахунку {from_account_number}")
            print(f"Успішний переказ {amount:.2f} грн з {from_account_number} на {to_account_number}.")
            return True
        else:
            print(f"Не вдалося здійснити переказ з {from_account_number} на {to_account_number}.")
            return False


# --- Приклад використання класу "Банківський рахунок" ---
if __name__ == "__main__":
    my_bank = Bank("ПриватБанк")

    # Додавання рахунків
    account1 = my_bank.add_account("1234567890", 1000.0)
    account2 = my_bank.add_account("0987654321", 500.0)
    my_bank.add_account("1234567890", 200) # Спроба додати існуючий рахунок

    if account1 and account2:
        print("\n--- Операції з рахунками ---")
        print(account1)
        print(account2)

        account1.deposit(200.0, "Зарплата")
        account1.withdraw(150.0, "Покупки")
        account1.withdraw(1500.0, "Велика покупка") # Спроба списати більше, ніж є на рахунку

        account2.deposit(100.0, "Повернення боргу")

        print("\n--- Переказ коштів ---")
        my_bank.perform_transfer("1234567890", "0987654321", 300.0)
        my_bank.perform_transfer("1234567890", "0000000000", 50.0) # Неіснуючий рахунок
        my_bank.perform_transfer("1111111111", "0987654321", 50.0) # Неіснуючий рахунок
        my_bank.perform_transfer("1234567890", "1234567890", 50.0) # На той самий рахунок

        print("\n--- Перевірка балансу ---")
        print(f"Баланс рахунку {account1.account_number}: {account1.get_balance():.2f} грн")
        print(f"Баланс рахунку {account2.account_number}: {account2.get_balance():.2f} грн")

        print("\n--- Історія транзакцій для рахунку 1234567890 ---")
        for t in account1.get_transaction_history():
            print(t)

        print("\n--- Історія транзакцій для рахунку 0987654321 ---")
        for t in account2.get_transaction_history():
            print(t)

        print("\n--- Видалення рахунку ---")
        my_bank.delete_account("1234567890")
        my_bank.delete_account("9999999999") # Спроба видалити неіснуючий рахунок

        print(f"\nРахунок 1234567890 після видалення: {my_bank.find_account('1234567890')}")