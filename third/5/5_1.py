import os
import re
import statistics
import json
from bs4 import BeautifulSoup

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('1'))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('result'), os.path.normpath('1'))

# считываем файлы
def file_read(file_name):
    with open(file_name, encoding='utf-8') as f:
        str_html = ''
        lines = f.readlines()
        for line in lines:
            str_html += line
    
        soup = BeautifulSoup(str_html, 'html.parser')

        item = {}
        item['name'] = soup.find_all('span')[0].get_text().strip()
        # вытаскиваем список параметров и их значения
        name_parameters = soup.find_all('span', attrs={"class": 'j2w'})
        val_parameters = soup.find_all('dd', attrs={'class': "jw2"})
        
        # обрабатываем 
        for i in range(len(name_parameters)):
            name_parameter = name_parameters[i].get_text().strip()
            val_parameter = val_parameters[i].get_text().strip()
            # вес, диагональ, время и объем переводим в численный тип
            if name_parameter == 'Вес, кг' or name_parameter == 'Диагональ экрана, дюймы':
                val_parameter = float(val_parameter)
            elif name_parameter == 'Общий объем SSD, ГБ' or name_parameter == 'Время автономной работы, ч':
                val_parameter = int(val_parameter)
            item[name_parameter] = val_parameter
        return item


max_file = 11
# проходимся по всем файлам
items = []
for i in range(1, max_file):
    temp = file_read(os.path.join(my_file, os.path.normpath(f'{i}.html')))
    items.append(temp)

# отсортируем значения по убыванию Общего объема SSD и запишем в файл
items = sorted(items, key=lambda x: x['Общий объем SSD, ГБ'], reverse=True)

with open(os.path.join(result, os.path.normpath("res_1_sort.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))

# выполним фильтрацию, отсеяв ноутбуки, работающие автономно меньше 5 часов, и запишем в файл
filter_views = []
for time in items:
    if time.get('Время автономной работы, ч', False) != False:
        if time['Время автономной работы, ч'] >= 5:
            filter_views.append(time)

with open(os.path.join(result, os.path.normpath("res_1_filter.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(filter_views, ensure_ascii=False))

# print(len(items))
# print(len(filter_views))

# рассчитаем числовые характеристики по весу ноутбуков и частоту разных видеокарт
all_weight = {}
sorev = {}
count = 0
all_weight['sum_weight'] = 0
all_weight['min_weight'] = 10 ** 9 + 1
all_weight['max_weight'] = 0
std_weight = [0]
for note in items:
    # проверка на наличие такого ключа (параметра ноутбука)
    if note.get('Вес, кг', False) != False:
        temp = note['Вес, кг']
        count += 1

        all_weight['sum_weight'] += temp
        if all_weight['min_weight'] > temp:
            all_weight['min_weight'] = temp
        if all_weight['max_weight'] < temp:
            all_weight['max_weight'] = temp
        std_weight.append(temp)
    if note.get('Операционная система', False) != False:
        if note['Операционная система'] in sorev:
            sorev[note['Операционная система']] += 1
        else:
            sorev[note['Операционная система']] = 1
all_weight['avr_weight'] = all_weight['sum_weight'] / count
all_weight['std_weight'] = statistics.stdev(std_weight)

all_res = [all_weight, sorev]

with open(os.path.join(result, os.path.normpath("res_1_charact.json")), 'w', encoding='utf-8') as f:
   f.write(json.dumps(all_res, ensure_ascii=False))
