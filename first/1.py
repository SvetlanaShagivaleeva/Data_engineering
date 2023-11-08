import os
text_var = 'задания/1/text_1_var_3'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('r_text_1.txt'))

# считываем файл
with open(my_file) as f:
    text = f.readlines()
text = ' '.join(text)

# функция для удаления знаков препинания
def str_change(line):
    mask = '!?,.'
    mask_2 = '\n'
    for i in mask:
        line = line.replace(i, ' ')
    line = line.replace(mask_2, ' ')
    while "  " in line:
        line = line.replace('  ', ' ')
    line = line.lower()
    return line.split()

lines = str_change(text)
# создаем словарь
words_dict = {}
for i in lines:
    if i in words_dict:
        words_dict[i] += 1
    else:
        words_dict[i] = 1

# сортируем
words_dict_sort = dict(sorted(words_dict.items(), reverse=True, key=lambda x: x[1]))
# print(words_dict_sort)

# выводим в файл
with open(result, 'w') as res:
    for key, value in words_dict_sort.items():
        res.write(key + ':' + str(value) + '\n')