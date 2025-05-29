# Зчитування тексту з файлу
file_path = "M:\Programing\Python\SkriptLanguage\LB4\ХорЕлементів.txt"  # Шлях до файлу
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
except FileNotFoundError:
    print(f"Помилка: Файл '{file_path}' не знайдено. Переконайтеся, що файл існує в правильній директорії.")
    exit(1)
except UnicodeDecodeError:
    print("Помилка: Проблема з кодуванням файлу. Переконайтеся, що файл збережено в UTF-8.")
    exit(1)

# Функція для підрахунку символів
def count_characters(text):
    # Загальна кількість символів (з пробілами, включаючи всі символи)
    total_chars = len(text)
    
    # Кількість символів без пробілів (видаляємо пробіли, табуляцію, переноси рядків)
    # Використовуємо replace для видалення пробільних символів
    no_spaces_text = text.replace(' ', '').replace('\n', '').replace('\t', '')
    chars_no_spaces = len(no_spaces_text)
    
    return total_chars, chars_no_spaces

# Функція для підрахунку слів
def count_words(text):
    # Видаляємо основні знаки пунктуації за допомогою replace
    # Список основних знаків пунктуації з лекційного матеріалу та тексту
    punctuation = '.,!?;:"\'—-()'
    clean_text = text.lower()  # Приводимо до нижнього регістру
    for char in punctuation:
        clean_text = clean_text.replace(char, '')
    
    # Розділяємо текст на слова
    words = clean_text.split()
    
    # Загальна кількість слів
    total_words = len(words)
    
    # Кількість різних слів (без повторів)
    # Створюємо словник для підрахунку частоти слів
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] = word_freq[word] + 1
        else:
            word_freq[word] = 1
    
    # Кількість різних слів — це кількість ключів у словнику
    unique_words = len(word_freq.keys())
    
    # Кількість унікальних слів, що зустрічаються лише один раз
    one_time_words = len([word for word, count in word_freq.items() if count == 1])
    
    return total_words, unique_words, one_time_words

# Виконання аналізу
total_chars, chars_no_spaces = count_characters(text)
total_words, unique_words, one_time_words = count_words(text)

# Виведення результатів
print(f"Загальна кількість символів (з пробілами): {total_chars}")
print(f"Загальна кількість символів (без пробілів): {chars_no_spaces}")
print(f"Загальна кількість слів: {total_words}")
print(f"Кількість різних слів (без повторів): {unique_words}")
print(f"Кількість унікальних слів (зустрічаються один раз): {one_time_words}")