import os
import numpy as np
import json

text_var = 'Данные для практической работы 2/2/matrix_3_2.npy'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('points.npz'))
res_zip = os.path.join(os.path.dirname(__file__), os.path.normpath('points_zip.npz'))

var = 3 

# считываем файл
matrix = np.load(my_file)
matrix = matrix.astype('float')

x = []
y = []
z = []

filt = 500 + var

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i][j] > filt:
            x.append(i)
            y.append(j)
            z.append(matrix[i][j])

np.savez(result, x=x, y=y, z=z)
np.savez_compressed(res_zip, x=x, y=y, z=z)

print(f'points     = {os.path.getsize(result)}')
print(f'points_zip = {os.path.getsize(res_zip)}')
