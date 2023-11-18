import os
import re
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task1_var3'))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

# считываем файлы
def file_read(file_name):
    with open(file_name, encoding='utf-8') as f:
        str_html = ''
        lines = f.readlines()
        for line in lines:
            str_html += line
    
        soup = BeautifulSoup(str_html, 'html.parser')

        item = {}
        item['type'] = soup.find_all('span', string=re.compile("Тип"))[0].get_text().split(':')[1].strip()
        item['tur'] = soup.find_all('h1')[0].get_text().split(':')[1].strip()
        address = soup.find_all('p')[0].get_text()
        ind = address.find('Начало')
        item["city"] = address[:ind].split(':')[1].strip()
        item["start"] = address[ind:].split(':')[1].strip()
        item['count_tur'] = int(soup.find_all('span', attrs={"class": 'count'})[0].get_text().split(':')[1].strip())
        item['limit_time'] = soup.find_all('span', attrs={"class": 'year'})[0].get_text().split(':')[1].strip()
        item['min_rating'] = int(soup.find_all('span', string=re.compile("Минимальный рейтинг для участия"))[0].get_text().split(':')[1].strip())
        item['img'] = soup.find_all('img')[0]['src']
        item['rating'] = float(soup.find_all('span', string=re.compile("Рейтинг"))[0].get_text().split(':')[1].strip())
        item['views'] = int(soup.find_all('span', string=re.compile("Просмотры"))[0].get_text().split(':')[1].strip())
        
        return item


max_file = 1000
# max_file = 200

# проходимся по всем файлам
items = []
for i in range(1, max_file):
    temp = file_read(os.path.join(my_file, os.path.normpath(f'{i}.html')))
    items.append(temp)
    # if i < 30:
    #     print(temp)

# отсортируем значения по уровню убывания рейтинга и запишем в файл
items = sorted(items, key=lambda x: x['rating'], reverse=True)

with open(os.path.join(result, os.path.normpath("res_1_sort.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

# выполним фильтрацию по просмотрам и запишем в файл
filter_views = []
for olimp in items:
    if olimp['views'] >= 50000:
        filter_views.append(olimp)

with open(os.path.join(result, os.path.normpath("res_1_filter.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

# print(len(items))
# print(len(filter_views))

# рассчитаем числовые характеристики для количества туров и узнаем частоту видов соревнований
all_tur = {}
sorev = {}
all_tur['sum_tur'] = 0
all_tur['min_tur'] = 10 ** 9 + 1
all_tur['max_tur'] = 0
std_tur = [0]
for olimp in items:
    temp = olimp['count_tur']
    all_tur['sum_tur'] += temp
    if all_tur['min_tur'] > temp:
        all_tur['min_tur'] = temp
    if all_tur['max_tur'] < temp:
        all_tur['max_tur'] = temp
    std_tur.append(temp)
    if olimp['type'] in sorev:
        sorev[olimp['type']] += 1
    else:
        sorev[olimp['type']] = 1
all_tur['avr_tur'] = all_tur['sum_tur'] / len(items)
all_tur['std_tur'] = statistics.stdev(std_tur)

all_res = [all_tur, sorev]

with open(os.path.join(result, os.path.normpath("res_1_charact.json")), 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))
