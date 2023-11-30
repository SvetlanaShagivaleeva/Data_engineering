import os
import msgpack
import sqlite3
import json

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('data_2'), os.path.normpath('task_2_var_03_subitem.msgpack'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result_2'))

def read_file():
    # Считаем файл
    with open(my_file, 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
    # print(data[:5])
    return data


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


# запись в бд
def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO comments (first_table, price, place, date) 
        VALUES(
            (SELECT id FROM my_first_table WHERE title = :title),
            :price, :place, :date)""", data)
    db.commit()


# все данные о стоимости, месте и дате по книге
def first_query(db, title):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM comments
        WHERE first_table = (SELECT id FROM my_first_table WHERE title = ?)                
         """, [title])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items    


# все данные о стоимости, месте и дате по книге
def second_query(db, title):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(price) as sum_price,
            AVG(price) as avg_price,
            MIN(price) as min_price, 
            MAX(price) as max_price
        FROM comments
        WHERE first_table = (SELECT id FROM my_first_table WHERE title = ?) 
                       
         """, [title])
    print(dict(res.fetchone()))

    cursor.close()
    return []


# книги, которые есть в наличии онлайн
def third_query(db, place):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            title,
            (SELECT "YES" FROM comments WHERE id = (SELECT id FROM comments WHERE place = ?)) as availability_offline
        FROM my_first_table              
         """, [place])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items    


# файл прочли, больше не надо
# data = read_file()
db = connect_to_db(os.path.join(os.path.dirname(__file__), os.path.normpath('first')))
# заагрузили файл в БД
# insert_data(db, data)


# все данные о стоимости, месте и дате по книге
first = first_query(db, 'Зеленая миля')
with open(os.path.join(res_file, os.path.normpath("res_2_first.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(first, ensure_ascii=False))

# узначем числовые характеристики для книги определенной
second_query(db, 'Зеленая миля')

# книги, которые есть в наличии онлайн
third = third_query(db, "offline")
with open(os.path.join(res_file, os.path.normpath("res_2_third.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(third, ensure_ascii=False))

# просмотр всей таблицы
# result = db.cursor().execute("SELECT * FROM comments")
# for row in result.fetchall():
#     print(dict(row))
