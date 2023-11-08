import os

var = 3
text_var = 'задания/3/text_3_var_3'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('r_text_3.txt'))

# считываем файл
with open(my_file) as f:
    text = f.readlines()

# найдем неизвестные и отфильтруем строки
filter_str = []
for line in text:
    n = line.split(',')
    numbers = []
    for i in range(len(n)):
        if n[i] == 'NA':
            temp = (int(n[i - 1]) + int(n[i + 1])) / 2
            if temp ** 2 >= (50 + var) ** 2:
                numbers.append(str(temp))
        else:
            temp = int(n[i])
            if temp ** 2 >= (50 + var) ** 2:
                numbers.append(str(temp))
    filter_str.append(numbers)

# выводим в файл
with open(result, 'w') as res:
    for value in filter_str:
        s = ', '.join(value)
        res.write(s + '\n')
