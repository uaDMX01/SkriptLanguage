class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def get_info(self):
        return f"Книга: {self.title}, Автор: {self.author}, Рік: {self.year}"


# Створення двох книг
book1 = Book("Гаррі Поттер", "Джоан Роулінг", 1997)
book2 = Book("Місто", "Валер'ян Підмогильний", 1927)

# Виведення інформації
print(book1.get_info())
print(book2.get_info())