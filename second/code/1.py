import os
import numpy as np
import json

text_var = 'Данные для практической работы 2/1/matrix_3.npy'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('r_task_1.txt'))
mat_norm = os.path.join(os.path.dirname(__file__), os.path.normpath('norm_matrix'))

# считываем файл
matrix = np.load(my_file)
matrix = matrix.astype('float')

matrix_inf = {}
matrix_inf['sum'] = np.sum(matrix)
matrix_inf['avr'] = matrix_inf.get('sum') / matrix.size
matrix_inf["sumMD"] = np.trace(matrix)
matrix_inf['avrMD'] = matrix_inf.get('sumMD') / matrix.shape[0]

sumSD = 0
k = matrix.shape[0] - 1
for i in range(matrix.shape[0]):
    sumSD += matrix[i][k]
    k -= 1
    
matrix_inf["sumSD"] = sumSD
matrix_inf['avrSD'] = matrix_inf.get('sumSD') / matrix.shape[0]
matrix_inf['max'] = matrix.max()
matrix_inf['min'] = matrix.min()

# print(matrix_inf)
with open(result, 'w') as res:
    res.write(json.dumps(matrix_inf))

matrix_norm = matrix / matrix_inf.get('max')

np.save(mat_norm, matrix_norm)