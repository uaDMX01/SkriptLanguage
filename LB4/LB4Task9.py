file_path = "ХорЕлементів.txt"
try:
    with open(file_path, 'r', encoding='utf=8') as file:
        text = file.read()
except FileNotFoundError:
    print (f"помилка: '{file_path}'не знайдено")
    exit(1)
except UnicodeDecodeError:
    print (f"Помилка з кодуванням файлу")
    exit(1)

def count_characters(text):
    total_chars = len(text)

    no_spaces_text = text.replace(' ', '').replace('\n', '').replace('\t', '')
    chars_no_spaces = len(no_spaces_text)

    return total_chars, chars_no_spaces
# підрахунок символів

def count_words(text):
    punctuation = '.,!?;:"\'—-()…–'
    clean_text = text.lower()
    for char in punctuation:
        clean_text = clean_text.replace(char, '')

    words = clean_text.split()

    total_words = len(words)

    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] = word_freq[word] + 1
        else:
            word_freq[word] = 1

    unique_words = len(word_freq.keys())

    one_time_words = 0
    for word, count in word_freq.items():
        if count == 1:
            one_time_words = one_time_words + 1

    return total_words, unique_words, one_time_words, words
# Функція для підрахунку слів і створення списку слів

#10 слів
def find_top_n_grams(words, n):
    n_gram_freq = {}

    if n <= 0 or n > len(words):
        return []

    for i in range(len(words) - n + 1):
        n_gram = ' '.join(words[i:i + n])
        if n_gram in n_gram_freq:
            n_gram_freq[n_gram] = n_gram_freq[n_gram] + 1
        else:
            n_gram_freq[n_gram] = 1

    n_gram_list =[]
    for n_gram, count in n_gram_freq.items():
        n_gram_list.append((count,n_gram))

    for i in range(len(n_gram_list)):
        for j in range (len(n_gram_list) - i - 1):
            if n_gram_list[j][0] < n_gram_list [j+1][0]:
                n_gram_list[j], n_gram_list[j+1] = n_gram_list [j+1], n_gram_list[j]
    # Повертаємо перші 10 (або менше, якщо послідовностей менше)
    return n_gram_list [:10]

# Парцюємо з користувачем

try:
    n=int(input("Введіть кількість слів у послідовності (N): "))
except ValueError:
    print("Помилка: Введіть ціле число.")
    exit(1)

# Виконання аналізу
total_chars, char_no_spaces = count_characters(text)
total_words, unique_words, one_time_words, words = count_words(text)

#пошук 10 слів (задача 9)
top_n_grams = find_top_n_grams(words, n)

#вивід результату
print(f"Загальна кількість символів (з пробілами): {total_chars}")
print(f"Загальна кількість символів (без пробілів): {char_no_spaces}")
print(f"Загальна кількість слів: {total_words}")
print(f"Кількість різних слів (без повторів): {unique_words}")
print(f"Кількість унікальних слів (зустрічаються один раз): {one_time_words}")
print("\n10 найчастіше вживаних послідовностей із", n, "слів:")
if top_n_grams:
    for count, n_gram in top_n_grams:
        print(f"'{n_gram}' - {count} разів")
    else:
        print(f"Неможливо знайти послідовності: N={n} є некоректним або текст надто короткий.")
