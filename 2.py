import os
text_var = 'задания/2/text_2_var_3'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('r_text_2.txt'))

# считываем файл
with open(my_file) as f:
    text = f.readlines()

#подсчитываем среднее ариф в каждой строке
average = []
for line in text:
    n = line.split(',')
    count_n = 0
    sum_n = 0
    for i in n:
        count_n += 1
        sum_n += int(i)
    average.append(sum_n/count_n)

# print(average)
# выводим в файл
with open(result, 'w') as res:
    for value in average:
        res.write(str(value) + '\n')