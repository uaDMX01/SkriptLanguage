import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def analyze_news_page(url):
    """
    Аналізує сторінку за заданим URL та підраховує
    частоту слів, HTML-тегів, кількість посилань та зображень.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні сторінки: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    # 1. Підрахунок частоти появи слів у тексті
    # Видаляємо скрипти та стилі, щоб отримати чистий текст
    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()

    text_content = soup.get_text()
    # Розбиваємо текст на слова та фільтруємо порожні рядки
    words = re.findall(r'\b\w+\b', text_content.lower())
    word_frequency = Counter(words)

    # 2. Підрахунок частоти появи HTML-тегів
    all_tags = [tag.name for tag in soup.find_all()]
    tag_frequency = Counter(all_tags)

    # 3. Підрахунок кількості посилань
    links = soup.find_all('a')
    num_links = len(links)

    # 4. Підрахунок кількості зображень
    images = soup.find_all('img')
    num_images = len(images)

    print(f"Аналіз сторінки: {url}\n")

    print("--- Частота появи слів (ТОП-20) ---")
    # Фільтруємо слова, які можуть бути специфічними для HTML, але потрапили в текст
    # Наприклад, 'div', 'p', 'span' тощо, якщо вони не є частиною осмисленого тексту.

    filtered_word_frequency = {word: count for word, count in word_frequency.items() if word.isalpha() and len(word) > 1}

    for word, count in Counter(filtered_word_frequency).most_common(20):
        print(f"'{word}': {count}")
    print("-" * 30)

    print("\n--- Частота появи HTML-тегів (ТОП-20) ---")
    for tag, count in tag_frequency.most_common(20):
        print(f"'{tag}': {count}")
    print("-" * 30)

    print(f"\nКількість посилань: {num_links}")
    print(f"Кількість зображень: {num_images}")

# Приклад використання для https://qoopixie.com/
if __name__ == "__main__":
    news_url = "https://www.unian.ua/"
    analyze_news_page(news_url)