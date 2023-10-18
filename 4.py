import os
import csv

var = 3
text_var = 'задания/4/text_4_var_3'
# text_var = 'test.txt'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('r_text_4.csv'))


columns = []
average_salary = 0
# считываем файл
with open(my_file, encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        column = {
                    'id': int(row[0]),
                    'name': row[2] + " " + row[1],
                    'age': int(row[3]),
                    'salary': int(row[4][:-1])
        }
        average_salary += column['salary']
        columns.append(column)

average_salary /= len(columns)

for i in columns:
    if i['salary'] < average_salary or i['age'] <= (25 + var % 10):
        columns.remove(i)

columns_sort = sorted(columns, key=lambda x: x['id'])

# выводим в файл
with open(result, 'w', encoding='utf-8') as res:
    writer = csv.writer(res)
    writer.writerow(['id', 'name', 'age', 'salary'])
    for value in columns_sort:
        writer.writerow([value['id'], value['name'], value['age'], value["salary"]])