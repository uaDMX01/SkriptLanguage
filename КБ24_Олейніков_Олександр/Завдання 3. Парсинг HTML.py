import re

html = """
<html>
<head><title>Сторінка</title></head>
<body>
<h1>Головна новина</h1>
<p>Текст новини...</p>
<h1>Оголошення</h1>
</body>
</html>
"""

# Знаходимо всі заголовки <h1> за допомогою регулярного виразу
headers = re.findall(r'<h1>(.*?)</h1>', html, re.DOTALL)

# Виводимо кожен заголовок
for header in headers:
    print(header.strip())
