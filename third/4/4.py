import os
import re
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('task4_var3'))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

# считываем файлы
def file_read(file_name):
    items = []
    with open(file_name, encoding='utf-8') as f:
        str_xml = ''
        lines = f.readlines()
        for line in lines:
            str_xml += line
    
        soup = BeautifulSoup(str_xml, 'xml')
        for cloth in soup.find_all('clothing'):
            item = {}  
            for el in cloth.contents:
                if el.name is None:
                    continue
                elif el.name == 'price' or  el.name == 'reviews':
                    item[el.name] = int(el.get_text().strip())
                elif el.name == 'rating':
                    item[el.name] = float(el.get_text().strip())
                elif el.name == 'new':
                    item[el.name] = el.get_text().strip() == '+'
                elif el.name == 'exclusive' or el.name == 'sporty':
                    item[el.name] = el.get_text().strip() == 'yes'
                else:
                    item[el.name] = el.get_text().strip()
            items.append(item)
    return items


max_file = 101
# проходимся по всем файлам
items = []
for i in range(1, max_file):
    temp = file_read(os.path.join(my_file, os.path.normpath(f'{i}.xml')))
    items += temp

# отсортируем значения в алфавитном порядке и запишем в файл
items = sorted(items, key=lambda x: x['name'])

with open(os.path.join(result, os.path.normpath("res_4_sort.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

# выполним фильтрацию, отобрав новые вещи, и запишем в файл
filter_views = []
for product in items:
    if product.get('new', False) != False:
        filter_views.append(product)

with open(os.path.join(result, os.path.normpath("res_4_filter.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

# print(len(items))
# print(len(filter_views))

# рассчитаем числовые характеристики для цены и узнаем частоту цвета
all_price = {}
color = {'no_color': 0}
all_price['sum_price'] = 0
all_price['min_price'] = 10 ** 9 + 1
all_price['max_price'] = 0
std_price = [0]
for product in items:
    temp = product['price']
    all_price['sum_price'] += temp
    if all_price['min_price'] > temp:
        all_price['min_price'] = temp
    if all_price['max_price'] < temp:
        all_price['max_price'] = temp
    std_price.append(temp)
    if product.get('color', False) != False:
        if product['color'] in color:
            color[product['color']] += 1
        else:
            color[product['color']] = 1
    else:
        color['no_camera'] += 1
all_price['avr_price'] = all_price['sum_price'] / len(items)
all_price['std_price'] = statistics.stdev(std_price)

all_res = [all_price, color]

with open(os.path.join(result, os.path.normpath("res_4_charact.json")), 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))
