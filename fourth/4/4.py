import os
import msgpack
import sqlite3
import json

my_file_part_1 = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_4_var_03_product_data.msgpack'))
my_file_part_2 = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_4_var_03_update_data.text'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

def read_file_1():
    # Считаем файл
    with open(my_file_part_1, 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
    name_set = set()
    items = []
    for i in range(len(data)): 
        if data[i]['name'] not in name_set:
            items.append(data[i])
            name_set.add(data[i]['name'])
    for i in range(len(items)):
        if 'category' in items[i]:
            continue
        else:
            items[i]['category'] = "no"
    return items


def update_data():
    # Считаем файл
    items = []
    with open(my_file_part_2, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()
        for line in lines:
            if line == '=====\n':
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split("::")

                if splitted[0] != 'param':
                    item[splitted[0]] = splitted[1]
                else:
                    if item['method'] == 'available':
                        item[splitted[0]] = splitted[1] == 'True'
                    elif item['method'] != 'remove':
                        item[splitted[0]] = float(splitted[1]) 
                    items.append(item)
    return items


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


# запись в бд
def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views) 
        VALUES(:name, :price, :quantity, :category, :fromCity, :isAvailable, :views)""", data)
    db.commit()


# удаляем имя
def delet_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM product WHERE name = ?", [name])
    db.commit()


# изменение цены в процентах
def update_price_perc(db, name, perc):
    cursor = db.cursor()
    cursor.execute('UPDATE product SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?', [perc, name])
    cursor.execute('UPDATE product SET version = version + 1 WHERE name = ?', [name])
    db.commit()


# изменение цены
def update_price(db, name, value):
    cursor = db.cursor()
    res = cursor.execute('UPDATE product SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0)', [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()


# 
def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET isAvailable = ? WHERE (name = ?)", [param, name])
    cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
    db.commit()


# 
def update_quantity(db, name, val):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)", 
                         [val, name, val])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()


# обработка изменений
def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                print(f'deleting {item["name"]}')
                delet_name(db, item['name'])
            case 'price_percent':
                print(f'update_price {item["name"]} {item["param"]} %')
                update_price_perc(db, item['name'], item['param'])
            case "price_abs":
                print(f"update price {item['name']} {item['param']}")
                update_price(db, item['name'], item['param'])
            case "available":
                print(f"update available {item['name']} {item['param']}")
                update_available(db, item['name'], item['param'])
            case "quantity_add":
                print(f"update quantity {item['name']} {item['param']}")
                update_quantity(db, item['name'], item['param'])
            case "quantity_sub":
                print(f"update quantity {item['name']} {item['param']}")
                update_quantity(db, item['name'], item['param'])
            case _:
                print(f'unknow method {item["method"]}')


# самые обновляемые 
def top_update(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM product ORDER BY version DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# смотрим числовые характеристики по цене для товаров в каждой группе
def charact_price(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category,
            SUM(price) as sum,
            AVG(price) as avg,
            MIN(price) as min, 
            MAX(price) as max,
            COUNT(*) as total_count
        FROM product
        GROUP BY category
                        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# смотрим числовые характеристики по количеству для товаров в каждой группе
def charact_quantity(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            category,
            SUM(quantity) as sum,
            AVG(quantity) as avg,
            MIN(quantity) as min, 
            MAX(quantity) as max,
            COUNT(*) as total_count
        FROM product
        GROUP BY category
                        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# отфильтруем те товары, у которые в наличии, и отсортируем в порядке убывания популярности
def filter_rating(db):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM product
        WHERE isAvailable = 1
        ORDER BY views DESC
        """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# data_1 = read_file_1()
# with open(os.path.join(res_file, os.path.normpath("res_1.json")), 'w', encoding='utf-8') as f:
#     f.write(json.dumps(data_1, ensure_ascii=False))


db = connect_to_db(os.path.join(os.path.dirname(__file__), os.path.normpath('forth')))
# заагрузили файл в БД
# insert_data(db, data_1)

# загрузка обновлений в бд
# update = update_data()
# handle_update(db, update)

# Самые обновляемые
sort_version = top_update(db, 10)
with open(os.path.join(res_file, os.path.normpath("res_most_update.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(sort_version, ensure_ascii=False))

# Числовые характеристики для каждой группы товара по цене
ch_price = charact_price(db)
with open(os.path.join(res_file, os.path.normpath("res_charact_price.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(ch_price, ensure_ascii=False))

# Числовые характеристики для каждой группы товара по количеству
ch_quantity = charact_quantity(db)
with open(os.path.join(res_file, os.path.normpath("res_charact_quantity.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(ch_quantity, ensure_ascii=False))

# отфильтруем те товары, у которые в наличии, и отсортируем в порядке убывания популярности
fil_rat = filter_rating(db)
with open(os.path.join(res_file, os.path.normpath("res_filtrer.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(fil_rat, ensure_ascii=False))