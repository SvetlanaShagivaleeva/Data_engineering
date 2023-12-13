import os
import json
import msgpack
from pymongo import MongoClient

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_1_item.msgpack'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

def read_file():
    # Считаем файл
    with open(my_file, 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
    # print(data[:5])
    return data


# добавление объектов
def insert_many(collection, data):
    collection.insert_many(data)


# подключение
def connect():
    client = MongoClient()
    db = client["BD_1"]
    return db.person


# сортировка по зарплате
def sort_by_salary(collection):
    sort_bd = []
    for person in collection.find({}, limit=10).sort({'salary': -1}):
        person.pop('_id')
        sort_bd.append(person)
        # print(person)
    return sort_bd


# люди моложе 30 по убыванию зарплаты
def filter_30(collection):
    filter_db = []
    for person in collection.find({'age': {'$lt': 30}}, limit=15).sort({'salary': -1}):
        person.pop('_id')
        filter_db.append(person)
        # print(person)
    return filter_db


# фильтр по городу и профессиям
def filter_city_job(collection):
    filter_db = []
    for person in collection.find({'city': "Махадаонда",
                                   'job': {'$in': ["Психолог", "Продавец", 'Повар']}}, limit=10).sort({'age': 1}):
        person.pop('_id')
        filter_db.append(person)
        print(person)
    return filter_db


# количество записей по фильтру
def count_filter(collection):
    filter_db = []
    res = collection.count_documents({'age': {"$gt": 30, "$lt": 50},
                                      'year': {"$in": [2019, 2020, 2021, 2022]},
                                      '$or': [{'salary': {"$gt": 50000, "$lte": 75000}},
                                              {'salary': {"$gt": 125000, "$lt": 150000}}]})
    filter_db.append({'count': res})
    return filter_db


# файл прочли, больше не надо
# data = read_file()
# заполнение
# insert_many(connect(), data)

# запишем первые 10 строк отсортированных по зарплате в порядке убывания
# bd_sort_salary = sort_by_salary(connect())
# with open(os.path.join(res_file, os.path.normpath("res_1_sort.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(bd_sort_salary, ensure_ascii=False))

# люди моложе 30 по убыванию зарплаты
# bd_filter_age = filter_30(connect())
# with open(os.path.join(res_file, os.path.normpath("res_1_filter.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(bd_filter_age, ensure_ascii=False))

# фильтр по городу и профессиям
# bd_filter_city_job = filter_city_job(connect())
# with open(os.path.join(res_file, os.path.normpath("res_1_filter_city_job.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(bd_filter_city_job, ensure_ascii=False))

# количество записей по фильтру
# count = count_filter(connect())
# with open(os.path.join(res_file, os.path.normpath("res_1_count_filter.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(count, ensure_ascii=False))