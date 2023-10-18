import os
import csv
from bs4 import BeautifulSoup

var = 3
text_var = 'задания/5/text_5_var_3'
# text_var = 'test.txt'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('r_text_5.csv'))

with open(my_file, encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# print(soup)

# находим таблицу и строки по тегам
table = soup.find('table')
rows = table.find_all('tr')
rows = rows[1:]
items = []
for row in rows:
    columns = row.find_all('td')
    item = {
        'company': columns[0].text, 
        'contact': columns[1].text, 
        'country': columns[2].text, 
        'price': columns[3].text, 
        'item': columns[4].text
    }
    items.append(item)
# print(items)

# выводим в файл
with open(result, 'w', encoding='utf-8') as res:
    writer = csv.writer(res)
    for value in items:
        writer.writerow([value['company'], value['contact'], value['country'], value["price"], value["item"]])