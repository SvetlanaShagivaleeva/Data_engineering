import os
import csv
import json
import statistics
import msgpack
import pickle

text_var = 'data_5.csv'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
r_file_json = os.path.join(os.path.dirname(__file__), os.path.normpath('res_task5.json'))
r_file_pickle = os.path.join(os.path.dirname(__file__), os.path.normpath('data_task5.pkl'))
r_file_msgpack = os.path.join(os.path.dirname(__file__), os.path.normpath('data_task5.msgpack'))

data = []
with open(my_file) as f:
    reader = csv.reader(f)
    i = 0
    for row in reader:
        if row[2] != '' and i != 0:
            column = {
                        'name': row[0],
                        'Data_value': float(row[2]),
                        'Status': row[4],
                        'UNITS': row[5], 
                        'Group': row[8],
                        'Series_title_1': row[9]  
            }
            data.append(column)
        i = 1

result = {}
for it in data:    
    itDV = it['Data_value']
    if it['name'] in result:
        temp = result[it['name']]

        temp['count'] += 1
        if temp['max'] < itDV:
            temp['max'] = itDV
        if temp['min'] > itDV:
            temp['min'] = itDV
        temp['sum'] += itDV
        temp['avr'] = temp['sum'] / temp['count']
        temp['std'].append(itDV)

        if it['Status'] in temp['Status']:
            temp['Status'][it['Status']] += 1
        else:
            temp['Status'][it['Status']] = 1
        
        if it['UNITS'] in temp['UNITS']:
            temp['UNITS'][it['UNITS']] += 1
        else:
            temp['UNITS'][it['UNITS']] = 1

        if it['Group'] in temp['Group']:
            temp['Group'][it['Group']] += 1
        else:
            temp['Group'][it['Group']] = 1

        if it['Series_title_1'] in temp['Series_title_1']:
            temp['Series_title_1'][it['Series_title_1']] += 1
        else:
            temp['Series_title_1'][it['Series_title_1']] = 1
    else:
        result[it['name']] = {'count': 1, 
                'min': itDV, 
                'max': itDV,
                'sum': itDV,
                'avr': itDV,
                'std': [itDV],
                'Status': {it['Status']: 1},
                'UNITS': {it['UNITS']: 1},
                'Group': {it['Group']: 1},
                'Series_title_1': {it['Series_title_1']: 1}                         
                }
    
keys_list = list(result.keys())
for i in keys_list:
    part = result[i]
    if len(part['std']) > 1:
        part['std'] = statistics.stdev(part['std'])
    else:
        part['std'] = part['std'][0]

with open(r_file_json, 'w') as res:
    res.write(json.dumps(result))    

with open(r_file_pickle, "wb") as res:
    res.write(pickle.dumps(data))

with open(r_file_msgpack, 'wb') as res:
    res.write(msgpack.dumps(data))

# print(f'res_json    = {os.path.getsize(r_file_json)}')
print(f'data_msgpack = {os.path.getsize(r_file_msgpack)}')
print(f'data_pickle  = {os.path.getsize(r_file_pickle)}')