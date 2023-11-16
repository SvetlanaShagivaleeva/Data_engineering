import os
import re
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('2'))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result'), os.path.normpath('2'))

# считываем файлы
def file_read(file_name):
    items = []
    with open(file_name, encoding='utf-8') as f:
        str_html = ''
        lines = f.readlines()
        for line in lines:
            str_html += line
    
        soup = BeautifulSoup(str_html, 'html.parser')
        # список телефонов
        prods = soup.find_all('div', attrs={'class': 'product-item'})
        # print(prod)
        # проходимя по каждому
        for prod in prods:
            item = {}   
            # достаем src изображения, название, ссылку
            imag = prod.find_all('div', attrs={'class': "product-item__img"})[0].img['src'].strip()
            item['img'] = imag
            item['name'] = prod.find_all('a')[0].get_text().strip()
            item['link'] = prod.find_all('a')[0]['href'].strip()

            # получаем параметры телефона
            parameters = prod.find_all("div", attrs={"class": "product-item__option-item"})
            for param in parameters:
                # название параметра и его значения
                name_val = param.get_text().strip().split(':')
                name = name_val[0] 
                val = name_val[1]

                # для веса, памяти и объектива значение "очищаем" от ед измерения и приводим к int
                if name == 'Вес' or name == 'Оперативная память' or name == 'Количество объективов':
                    vals = val.split()
                    val = int(vals[0])
                   
                item[name] = val
            items.append(item)
    return items

max_file = 11
# проходимся по всем файлам
items = []
for i in range(1, max_file):
    temp = file_read(os.path.join(my_file, os.path.normpath(f'{i}.html')))
    items += temp

# отсортируем значения в порядке увеличения памяти и запишем в файл
items = sorted(items, key=lambda x: x['Оперативная память'])

with open(os.path.join(result, os.path.normpath("res_2_sort.json")), 'w') as f:
    f.write(json.dumps(items, ensure_ascii=False))

# выполним фильтрацию, отбросив телефоны с объективом меньше 4, и запишем в файл
filter_views = []
for note in items:
    # проверка на наличие такого ключа (параметра телефона)
    if note.get('Количество объективов', False) != False:
        if note['Количество объективов'] > 3:
            filter_views.append(note)

with open(os.path.join(result, os.path.normpath("res_2_filter.json")), 'w') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

# print(len(items))
# print(len(filter_views))

# рассчитаем числовые характеристики по весу телефонов и частоту разных камер
all_weight = {}
count = 0
proc = {"no_camera": 0}
all_weight['sum_weight'] = 0
all_weight['min_weight'] = 10 ** 9 + 1
all_weight['max_weight'] = 0
std_weight = [0]
for product in items:
    # проверка на наличие такого ключа (параметра телефона)
    if product.get('Вес', False) != False:
        temp = product['Вес']
        count += 1

        all_weight['sum_weight'] += temp
        if all_weight['min_weight'] > temp:
            all_weight['min_weight'] = temp
        if all_weight['max_weight'] < temp:
            all_weight['max_weight'] = temp
        std_weight.append(temp)

    if product.get('Основная камера', False) != False:
        if product['Основная камера'] in proc:
            proc[product['Основная камера']] += 1
        else:
            proc[product['Основная камера']] = 1
    else:
        proc['no_camera'] += 1

all_weight['avr_weight'] = all_weight['sum_weight'] / count
all_weight['std_weight'] = statistics.stdev(std_weight)

with open(os.path.join(result, os.path.normpath("res_2_charact.json")), 'w') as f:
   f.write(json.dumps(all_weight, ensure_ascii=False))
   f.write(json.dumps(proc, ensure_ascii=False))
