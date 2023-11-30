import os
import msgpack
import sqlite3
import json

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('data'), os.path.normpath('task_1_var_03_item.msgpack'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

def read_file():
    # Считаем файл
    with open(my_file, 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
    # print(data[:2])
    return data


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection


# запись в бд
def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO my_first_table (title, author, genre, pages, published_year, isbn, rating, views) 
        VALUES(:title, :author, :genre, :pages, :published_year, :isbn, :rating, :views)""", data)
    db.commit()


# Сортируем по просмотрам 
def top_views(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM my_first_table ORDER BY views DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


# смотрим числовые характеристики для количства страниц
def charact_page(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(pages) as sum,
            AVG(pages) as avg,
            MIN(pages) as min, 
            MAX(pages) as max
        FROM my_first_table
                        """)
    print(dict(res.fetchone()))
    cursor.close()
    return []


# Узнаем частоту встречаемости различных жанров
# подзапрос нужен для вычисления частоты, а cast для преобразования в real
def genre_popul(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM my_first_table) as count,
            genre
        FROM my_first_table
        GROUP BY genre
                        """)
    for row in res.fetchall():
        print(dict(row))
    return []


# отфильтруем те книги, у которых рейтинг выше минимального, и отсортируем в порядке убывания популярности
def filter_rating(db, min_rating, limit):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM my_first_table
        WHERE rating >= ?
        ORDER BY views DESC
        LIMIT ?
        """, [min_rating, limit])
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

# Сортируем по просмотрам
sort_views = top_views(db, 13)
with open(os.path.join(res_file, os.path.normpath("res_1_sorted.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(sort_views, ensure_ascii=False))

# считаем характеристики числовые для страниц
charact_page(db)

# Узнаем частоту встречаемости различных жанров
genre_popul(db)


# отфильтруем те книги, у которых рейтинг выше минимального, и отсортируем в порядке убывания популярности
fil_rat = filter_rating(db, 4.0, 13)
with open(os.path.join(res_file, os.path.normpath("res_1_filtrer.json")), 'w', encoding='utf-8') as f:
    f.write(json.dumps(fil_rat, ensure_ascii=False))

# просмотр всей таблицы
# result = db.cursor().execute("SELECT * FROM my_first_table")
# for row in result.fetchall():
#     print(dict(row))
