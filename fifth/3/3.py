import os
import csv
import json
from pymongo import MongoClient

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_3_item.csv'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

# считываем первый файл
def read_file():
    items = []
    with open(my_file, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=';')
        data.__next__()

        for row in data:
            if len(row) == 0: continue
            item = dict()
            item['job'] = row[0]
            item['salary'] = int(row[1])
            item['id'] = int(row[2])
            item['city'] = row[3]
            item['year'] = int(row[4])
            item['age'] = int(row[5])
            items.append(item)
    return items


# добавление объектов
def insert_many(collection, data):
    collection.insert_many(data)


# подключение
def connect():
    client = MongoClient()
    db = client["BD_1"]
    return db.person


# удалить по зарплате
def delete_salary(collection):
    res = collection.delete_many({"$or":[
                {"salary": {"$lt": 25000}},
                {"salary": {'$gt': 175000}}
    ]})
    print(res)


# увеличить возраст
def update_age(collection):
    res = collection.update_many({}, {"$inc":{"age": 1}})
    print(res)

# поднять зарплату 
def update_salary(collection, number, name_v, where_name):
    res = collection.update_many({f'{name_v}': {"$in": where_name}},
                                 {"$mul": {"salary": number}})
    print(res)


# поднять зарплату со сложным предикатом
def update_salary_pred(collection):
    filter = {
        "city": {'$in': ['Минск', 'Москва', 'Прага']},
        "job": {'$in': ["Психолог", "Продавец", 'Повар']},
        "age": {"$lt": 45, "$gt": 25}
    }
    update = {"$mul": {"salary": 1.2}}
    res = collection.update_many(filter, update)
    print(res)


# удалить по возрасту
def delete_age(collection):
    res = collection.delete_many({"$or":[
                {"age": {"$lt": 20}},
                {"age": {'$gt': 60}}
    ]})
    print(res)



# файл прочли, больше не надо
# data = read_file()
# заполнение
# insert_many(connect(), data)

# удалить по зарплате
# delete_salary(connect())

# увеличить возраст
# update_age(connect())

# поднять зарплату
# update_salary(connect(), 1.05, 'job', ["Водитель", "Учитель", "Инженер"])
# update_salary(connect(), 1.07, 'city', ['Рига', "Санкт-Петербург", "Эль-Пуэрто-де-Санта-Мария"])

# поднять зарплату со сложным предикатом
# update_salary_pred(connect())

# удалить по возрасту
delete_age(connect())