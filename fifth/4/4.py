import os
import csv
import json
from pymongo import MongoClient
import random

# файлы содержат разные данные. Предварительно разделены на 2 файла с разнами форматами
file_json = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('data.json'))
file_csv = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('data.csv'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

# считаем первый файл
def read_json():
    with open(file_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # print(len(data))
    return data


# считываем второй файл
def read_csv():
    items = []
    with open(file_csv, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=';')
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
    # print(len(items))
    return items


# добавление объектов
def insert_many(collection, data):
    collection.insert_many(data)


# подключение
def connect():
    client = MongoClient()
    db = client["task_5"]
    return db.person


# ВЫБОРКА
# 1) сортировка по долготе
def sort_by_longitude(collection):
    sort_bd = []
    for person in collection.find({}, limit=10).sort({'longitude': -1}):
        person.pop('_id')
        sort_bd.append(person)
        # print(person)
    return sort_bd


# 2) области с широтой ниже 100 и отсортированные по id страны
def filter_100(collection):
    filter_db = []
    for person in collection.find({'latitude': {'$lt': 100}}, limit=20).sort({'country_id': -1}):
        person.pop('_id')
        filter_db.append(person)
        # print(person)
    return filter_db


# 3) фильтр по стране и долготе
def filter_country_long(collection):
    filter_db = []
    for person in collection.find({'country_code': "RU",
                                   'longitude': {'$lt': 100}}, limit=10):
        person.pop('_id')
        filter_db.append(person)
    return filter_db


# 4) количество записей по России
def count_RU(collection):
    filter_db = []
    res = collection.count_documents({'country_code': "RU"})
    filter_db.append({'count': res})
    return filter_db


# 5) количество записей с широтой выше 70 и долготой ниже 130
def count_filter(collection):
    filter_db = []
    res = collection.count_documents({'longitude': {'$lt': 130},
                                      'latitude': {'$gt': 70},})
    filter_db.append({'count': res})
    return filter_db


# АГРЕГАЦИЯ
# 1) мин, сред, макс широты
def get_stat_by_latitude(collection):
    charact = [{"$group": {
        "_id": "result",
        "max": {"$max": "$latitude"},
        "avg": {"$avg": "$latitude"},
        "min": {"$min": "$latitude"}}}]
    for stat in collection.aggregate(charact):
        return [stat]
    

# 2) вывод количества данных по кодам стран
def count_by_country(collection):
    charact = [{"$group": {
        "_id": "$country_code",
        "count": {"$sum": 1}}},
        {"$sort":{"count":-1}}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        res.append(stat)
    return res


# 3) 4) вывод мин, сред, макс долготы/широты по странам
def get_stat_country_with_param(collection, column_name):
    charact = [{"$group": {
        "_id": "$country_code",
        "max": {"$max": f"${column_name}"},
        "avg": {"$avg": f"${column_name}"},
        "min": {"$min": f"${column_name}"}}}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        res.append(stat)
    return res   


# 5) вывод минимальной долготы при максимальной широте
def get_max_lat_min_long(collection):
    charact = [{"$sort":{'latitude': -1, "longitude": 1}},
                {"$limit": 1}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        stat.pop('_id')
        res.append(stat)
    return res  


# Обновление/удаление ДАННЫХ
# 1) удаляем области с отрицательной долготой и широтой
def delete_negativ(collection):
    res = collection.delete_many({"$or":[
                {"latitude": {"$lt": 0}},
                {"longitude": {"$lt": 0}}
    ]})
    print(res)

# 2) добавим дополнительную колонку
def new_column(collection):
    res = collection.update_many({}, {'$set': {'new_column': 0}})
    print(res)

# 3) обновить значение в колонке
def update_new_column(collection):
    for doc in collection.find():
        random_number = random.randint(1, 10)
        res = collection.update_one({'_id': doc['_id']},
                              {'$set': {'new_column': random_number}})
    print(res)
        

# 4) добавим в новой колонке 2 для областей России
def update_RU(collection):
    res = collection.update_many({'country_code': "RU"},
                                 {'$inc': {'new_column': 2}})
    print(res)


# 5) удаляем те, у кого меньше 5
def delete_5(collection):
    res = collection.delete_many({"new_column": {"$lt": 5}})
    print(res)

# файл прочли, больше не надо
# data_1 = read_json()
# data_2 = read_csv()
# заполнение
# insert_many(connect(), data_1)
# insert_many(connect(), data_2)

# ВЫБОРКА
# 1) сортировка по долготе
# bd_sort_longitude = sort_by_longitude(connect())
# with open(os.path.join(res_file, os.path.normpath("res_1_select.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(bd_sort_longitude, ensure_ascii=False))

# 2) области с широтой ниже 100 и отсортированные по id страны
# filter_bd_100 = filter_100(connect())
# with open(os.path.join(res_file, os.path.normpath("res_2_select.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(filter_bd_100, ensure_ascii=False))

# 3) фильтр по стране и долготе
# country_long = filter_country_long(connect())
# with open(os.path.join(res_file, os.path.normpath("res_3_select.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(country_long, ensure_ascii=False))

# 4) количество записей по России
# c_RU = count_RU(connect())
# with open(os.path.join(res_file, os.path.normpath("res_4_select.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(c_RU, ensure_ascii=False))

# 5) количество записей с широтой выше 70 и долготой ниже 130
# count = count_filter(connect())
# with open(os.path.join(res_file, os.path.normpath("res_5_select.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(count, ensure_ascii=False))

# АГРЕГАЦИЯ
# 1) мин, сред, макс широты
# agr_1 = get_stat_by_latitude(connect())
# with open(os.path.join(res_file, os.path.normpath("res_1_aggregate.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(agr_1, ensure_ascii=False))

# 2) вывод количества данных по кодам стран
# agr_2 = count_by_country(connect())
# with open(os.path.join(res_file, os.path.normpath("res_2_aggregate.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(agr_2, ensure_ascii=False))

# 3) 4) вывод мин, сред, макс долготы/широты по странам
# agr_3 = get_stat_country_with_param(connect(), "latitude")
# with open(os.path.join(res_file, os.path.normpath("res_3_aggregate.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(agr_3, ensure_ascii=False))

# agr_4 = get_stat_country_with_param(connect(), "longitude")
# with open(os.path.join(res_file, os.path.normpath("res_4_aggregate.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(agr_4, ensure_ascii=False))

# 5) вывод минимальной долготы при максимальной широте
# agr_5 = get_max_lat_min_long(connect())
# with open(os.path.join(res_file, os.path.normpath("res_5_aggregate.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(agr_5, ensure_ascii=False))

# Обновление/удаление ДАННЫХ
# 1) удаляем области с отрицательной долготой и широтой
# delete_negativ(connect())

# 2) добавим дополнительную колонку
# new_column(connect())

# 3) обновить значение в колонке
# update_new_column(connect())

# 4) добавим в новой колонке 2 для областей России
# update_RU(connect())

# 5) удаляем те, у кого меньше 5
# delete_5(connect())