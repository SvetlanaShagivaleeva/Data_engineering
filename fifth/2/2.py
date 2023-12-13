import os
import json
from pymongo import MongoClient

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_2_item.text'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

def read_file():
    # Считаем файл
    items = []
    with open(my_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()
        for line in lines:
            if line == '=====\n':
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split("::")

                if splitted[0] in ['salary', 'id', 'year', 'age']:
                    item[splitted[0]] = int(splitted[1])
                else:
                    item[splitted[0]] = splitted[1]
    return items


# добавление объектов
def insert_many(collection, data):
    collection.insert_many(data)


# подключение
def connect():
    client = MongoClient()
    db = client["BD_1"]
    return db.person


# мин, сред, макс зарплата
def get_stat_by_salary(collection):
    charact = [{"$group": {
        "_id": "result",
        "max": {"$max": "$salary"},
        "avg": {"$avg": "$salary"},
        "min": {"$min": "$salary"}}}]
    for stat in collection.aggregate(charact):
        return [stat]


# количество по профессиям
def count_by_job(collection):
    charact = [{"$group": {
        "_id": "$job",
        "count": {"$sum": 1}}},
        {"$sort":{"count":-1}}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        res.append(stat)
    return res


# мин, сред, макс параметра_2 по параметру
def get_stat_salary_with_param(collection, column_name, column_name_2):
    charact = [{"$group": {
        "_id": f"${column_name}",
        "max": {"$max": f"${column_name_2}"},
        "avg": {"$avg": f"${column_name_2}"},
        "min": {"$min": f"${column_name_2}"}}}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        res.append(stat)
    return res   


# макс зарплата, мин возраст
def get_max_salary_min_age(collection):
    charact = [{"$sort":{'age': 1, "salary": -1}},
                {"$limit": 1}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        stat.pop('_id')
        res.append(stat)
    return res  


# макс возраст, мин зарплата
def get_max_age_min_salary(collection):
    charact = [{"$sort":{'age': -1, "salary": 1}},
                {"$limit": 1}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        stat.pop('_id')
        res.append(stat)
    return res  


# сортировка где зарплата(свыше 50), с выводом агрегации возраста по городу
def sort_filter_age_by_city(collection):
    charact = [{"$match":{'salary': {'$gt': 50000}}},
        {"$group": {
        "_id": "$city",
        "max": {"$max": "$age"},
        "avg": {"$avg": "$age"},
        "min": {"$min": "$age"}}},
        {"$sort": {"salary": -1}}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        res.append(stat)
    return res   


# зарплата в диапазонах
def sort_filter_age_by_city(collection):
    charact = [{"$match":{
        'city': {'$in': ['Рига', "Санкт-Петербург", "Эль-Пуэрто-де-Санта-Мария"]},
        'job':{'$in':["Водитель", "Учитель", "Инженер"]},
        '$or':[{'age': {"$gt": 18, "$lt": 25}},
               {'age': {"$gt": 50, "$lt": 65}}]}},
        {"$group": {
        "_id": "_result",
        "max": {"$max": "$salary"},
        "avg": {"$avg": "$salary"},
        "min": {"$min": "$salary"}}}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        res.append(stat)
    return res  


# сортировка где год(позже 2010), с выводом агрегации возраста по работе
def sort_filter_city_by_job(collection):
    charact = [{"$match":{'year': {'$gt': 2010}}},
        {"$group": {
        "_id": "$job",
        "max": {"$max": "$age"},
        "avg": {"$avg": "$age"},
        "min": {"$min": "$age"}}},
        {"$sort": {"max": -1}}]
    res = []
    for stat in collection.aggregate(charact):
        # print(stat)
        res.append(stat)
    return res  


# файл прочли, больше не надо
# data = read_file()
# заполнение
# insert_many(connect(), data)

# мин, сред, макс зарплата
# m_a_m = get_stat_by_salary(connect())
# with open(os.path.join(res_file, os.path.normpath("res_1.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(m_a_m, ensure_ascii=False))

# количество по профессиям
# count_job = count_by_job(connect())
# with open(os.path.join(res_file, os.path.normpath("res_2.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(count_job, ensure_ascii=False))

# мин, сред, макс зарплата по городу
# salary_city =  get_stat_salary_with_param(connect(), 'city', 'salary')
# with open(os.path.join(res_file, os.path.normpath("res_3.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(salary_city , ensure_ascii=False))

# мин, сред, макс зарплата по профессии
# salary_job =  get_stat_salary_with_param(connect(), 'job', 'salary')
# with open(os.path.join(res_file, os.path.normpath("res_4.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(salary_job , ensure_ascii=False))

# мин, сред, макс возраста по городу
# age_city =  get_stat_salary_with_param(connect(), 'city', 'age')
# with open(os.path.join(res_file, os.path.normpath("res_5.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(age_city , ensure_ascii=False))

# мин, сред, макс возраста по профессии
# age_job =  get_stat_salary_with_param(connect(), 'job', 'age')
# with open(os.path.join(res_file, os.path.normpath("res_6.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(age_job , ensure_ascii=False))

# макс зарплата, мин возраст
# salary_age = get_max_salary_min_age(connect())
# with open(os.path.join(res_file, os.path.normpath("res_7.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(salary_age , ensure_ascii=False))

# макс возраст, мин зарплата
# age_salary = get_max_age_min_salary(connect())
# with open(os.path.join(res_file, os.path.normpath("res_8.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(age_salary , ensure_ascii=False))

# сортировка где зарплата(свыше 50), с выводом агрегации возраста по городу
# salar_agreg = sort_filter_age_by_city(connect())
# with open(os.path.join(res_file, os.path.normpath("res_9.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(salar_agreg , ensure_ascii=False))

# зарплата в диапазонах
# salary_diap = sort_filter_age_by_city(connect())
# with open(os.path.join(res_file, os.path.normpath("res_10.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(salary_diap , ensure_ascii=False))

# сортировка где год(позже 2010), с выводом агрегации возраста по работе
# age_agreg = sort_filter_city_by_job(connect())
# with open(os.path.join(res_file, os.path.normpath("res_11.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(age_agreg , ensure_ascii=False))