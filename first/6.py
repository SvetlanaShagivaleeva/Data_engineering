import os
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('text_6.txt'))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('r_text_6.html'))

str_json = ''
with open(my_file, encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)
soup = BeautifulSoup('', 'html.parser')

html = soup.new_tag('html')
soup.append(html)
head = soup.new_tag('head')
html.append(head)
title = soup.new_tag('title')
title.string = 'SUPERHEROES'
head.append(title)
body = soup.new_tag('body')
html.append(body)

# Создаем заголовок таблицы
table = soup.new_tag('table')
body.append(table)
thead = soup.new_tag('thead')
table.append(thead)
tr = soup.new_tag('tr')
thead.append(tr)
for key in data['members'][0]:
    th = soup.new_tag('th')
    th.string = key
    tr.append(th)

# строки
tbody = soup.new_tag('tbody')
table.append(tbody)
for member in data['members']:
    tr = soup.new_tag('tr')
    tbody.append(tr)
    for key, value in member.items():
        td = soup.new_tag('td')
        if '[' in str(value):
            k = 0
            value = ' + '.join(value)
        td.string = str(value)
        tr.append(td)

# print(soup.prettify())
# выводим в файл
with open(result, 'w', encoding='utf-8') as res:
    res.write(soup.prettify())