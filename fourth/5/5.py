import os
import sqlite3
import json
import csv
from bs4 import BeautifulSoup

file_json = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('cities.json'))
file_csv = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('states.csv'))
file_xml = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('countries.xml'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

# функции для чтения файлов
def read_json(file_name):
    with open (file_name, 'rb') as file:
        data = json.load(file)
    # print(data[:5])
    return data


def read_csv(file_name):
    items = []
    with open(file_name, 'r', encoding='utf-8') as file:
        data = csv.reader(file)
        data.__next__()
        for row in data:
            if len(row) == 0: continue
            item = dict()
            item['id'] = int(row[0])
            item['name'] = row[1]
            item['country_id'] = int(row[2])
            item['country_code'] = row[3]
            item['state_code'] = row[4]
            if len(row[5]) == 0:
                item['latitude'] = 0
                item['longitude'] = 0
            else:
                item['latitude'] = float(row[5])
                item['longitude'] = float(row[6])
            items.append(item)
    # print(items[:5])
    return items


def read_xml(file_name):
    items = []
    with open(file_name, encoding='utf-8') as f:
        str_xml = ''
        lines = f.readlines()
        for line in lines:
            str_xml += line
    
        soup = BeautifulSoup(str_xml, 'xml')
        for country in soup.find_all('country'):
            item = {}
            for el in country.contents:
                if el.name == 'id':
                    item[el.name] = int(el.get_text().strip())
                elif el.name == 'latitude' or el.name == 'longitude':
                    item[el.name] = float(el.get_text().strip())
                elif el.name in ['name', 'iso3', 'iso2', 'capital', 'currency', 'region', 'subregion', 'phone_code']:
                    item[el.name] = el.get_text().strip()
            items.append(item)
        # print(items[:5])
    return items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

# запись в бд
def insert_cities(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO cities (name, state_id, state_code, country_id, country_code, latitude, longitude) 
        VALUES(:name, :state_id, :state_code, :country_id, :country_code, :latitude, :longitude)""", data)
    db.commit()


def insert_states(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO states (name, country_id, country_code, state_code, latitude, longitude) 
        VALUES(:name, :country_id, :country_code, :state_code, :latitude, :longitude)""", data)
    db.commit()


def insert_contries(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO contries (name, iso3, iso2, phone_code, capital, currency, region, subregion, latitude, longitude) 
        VALUES(:name, :iso3, :iso2, :phone_code, :capital, :currency, :region, :subregion, :latitude, :longitude)""", data)
    db.commit()


# найдем все города России в алфавитном порядке
def rus_filter(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            *
        FROM cities
        WHERE country_code = "RU"
        ORDER BY name
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        # if item['name'] == "Yekaterinburg":
        #     print(item)
        # if item['name'] == "Kopeysk":
        #     print(item)
        items.append(item)
    cursor.close()
    return items


# посчитаем сколько регионов в каждой стране
# считаем по таблице states, а название страны берем по сооветсвию кода страны таблиц states и contries
def how_state(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT c.name, COUNT(s.name) as count_state
        FROM contries c
        INNER JOIN states s ON c.iso2 = s.country_code
        GROUP BY c.name
        """)    
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# добавить столбец в таблицу contry
def add_column(db):
    cursor = db.cursor()
    res = cursor.execute("""
        ALTER TABLE contries
        ADD column count_state INTEGER DEFAULT 0
                         """)
    cursor.close()
    return []


# заполняем колонку
def add_count(db, count_st):
    cursor = db.cursor()
    for temp in count_st:
        cursor.execute('UPDATE contries SET count_state = ? WHERE name = ?', [temp.get('count_state'), temp.get('name')])
    db.commit()
    return []

# Найдем числовые характеристики для количества регионов в странах
def charact_state(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(count_state) as sum,
            AVG(count_state) as avg,
            MIN(count_state) as min, 
            MAX(count_state) as max,
            COUNT(*) as total_count
        FROM contries
                    """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# найдем все города в европе
# для этого возьмем соответствие города по коду страны и из страны часть света
def cities_eu(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT t.name, c.name as country
        FROM cities t
        INNER JOIN contries c ON t.country_code = (SELECT c.iso2 WHERE c.region = 'Europe')
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# запишем столицы всех стран Азии
def cap_as(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT name, capital
        FROM contries
        WHERE region = 'Asia'
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# cities = read_json(file_json)
# states = read_csv(file_csv)
# contries = read_xml(file_xml)

db = connect_to_db(os.path.join(os.path.dirname(__file__), os.path.normpath('fifth')))
# заагрузили файл в БД
# insert_cities(db, cities)
# insert_states(db, states)
# insert_contries(db, contries)

# найдем все города России в алфавитном порядке
cities_rus = rus_filter(db)
with open(os.path.join(res_file, os.path.normpath("res_cities_rus.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(cities_rus, ensure_ascii=False))

# посчитаем сколько регионов в каждой стране
count_state_in_country = how_state(db)
with open(os.path.join(res_file, os.path.normpath("res_count_state_in_country.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(count_state_in_country, ensure_ascii=False))

# добавляем колонку
# add_column(db)
# заполняем ее
# add_count(db, count_state_in_country)

# Найдем числовые характеристики для количества регионов в странах
ch_state = charact_state(db)
with open(os.path.join(res_file, os.path.normpath("res_charact_state.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(ch_state, ensure_ascii=False))

# найдем все города в европе
city_eu = cities_eu(db)
with open(os.path.join(res_file, os.path.normpath("res_city_eu.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(city_eu, ensure_ascii=False))

# запишем столицы всех стран Азии
capital_as = cap_as(db)
with open(os.path.join(res_file, os.path.normpath("res_capital_as.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(capital_as, ensure_ascii=False))