import pandas as pd
import numpy as np
import os
import json

my_file = os.path.join(os.path.dirname(__file__), os.path.normpath('[2]automotive.csv.zip'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

pd.set_option("display.max_rows", 20, "display.max_columns", 60)


# считываем файл
def read_file(file_name):
    return pd.read_csv(file_name)
    # return next(pd.read_csv(file_name, chunksize=100))


# занимаемая память
def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2
    return "{:03.2f} MB".format(usage_mb)


# статистика начальная по колонкам
def get_memory_stat_by_column(file_chunk_name):
    # сколько в оперативке
    file_size = os.path.getsize(file_chunk_name)
    print(f'file size             = {file_size // 1024:10} КБ')

    total_size = 0
    start_data = next(pd.read_csv(file_chunk_name, chunksize=100_000))
    columns_stats = {
        column: {
            'memory_abs': 0,
            'memory_per': 0,
            'dtype': str(start_data.dtypes[column])
        }
        for column in start_data}
    for chunk in pd.read_csv(file_chunk_name, chunksize=100_000):
        chunk_memory = chunk.memory_usage(deep=True)
        total_size += float(chunk_memory.sum())
        for column in chunk:
            columns_stats[column]['memory_abs'] += float(chunk_memory[column])

    for col in columns_stats.keys():
        columns_stats[col]['memory_per'] = round(columns_stats[col]['memory_abs'] / total_size * 100, 4)
        columns_stats[col]['memory_abs'] = columns_stats[col]['memory_abs'] // 1024 
    with open(os.path.join(res_file, os.path.normpath('colums_memory_no_optim.json')), 'w', encoding='utf-8') as f:
        f.write(json.dumps(columns_stats, ensure_ascii=False))


# статистика оптимизированная по колонкам
def get_memory_with_optim(df):
    # сколько в оперативке
    file_size = os.path.getsize(my_file)
    print(f'file size             = {file_size // 1024:10} КБ')
    # память для каждой колонки
    memory_update_stat = df.memory_usage(deep=True)
    # общая память
    total_memory_usage = memory_update_stat.sum()
    print(f'file in memory size   = {total_memory_usage // 1024:10} КБ')

    column_stat = []
    for key in df.dtypes.keys():
        column_stat.append({'column_name': key,
                            'memory_abs': int(memory_update_stat[key] // 1024),
                            "memory_per": float(round(memory_update_stat[key] / total_memory_usage * 100, 4)),
                            'dtype': str(df.dtypes[key])})
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    with open(os.path.join(res_file, os.path.normpath("colums_memory_with_optim.json")), 'w', encoding='utf-8') as f:
        f.write(json.dumps(column_stat, ensure_ascii=False))


# перевод в категориальный тип
def opt_obj(df):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    print(mem_usage(dataset_obj))
    print(mem_usage(converted_obj))
    return converted_obj


# понижаем int
def opt_int(df):
    data_int = df.select_dtypes(include=['int'])

    converted_int = data_int.apply(pd.to_numeric, downcast='unsigned')
    print(mem_usage(data_int))
    print(mem_usage(converted_int))

    compare_ints = pd.concat([data_int.dtypes, converted_int.dtypes], axis=1)
    compare_ints.columns = ['before', 'after']
    compare_ints.apply(pd.Series.value_counts)
    print(compare_ints)

    return converted_int

    
# понижаем float
def opt_float(df):
    data_float = df.select_dtypes(include=['float'])

    converted_float = data_float.apply(pd.to_numeric, downcast='float')
    print(mem_usage(data_float))
    print(mem_usage(converted_float))

    compare_floats = pd.concat([data_float.dtypes, converted_float.dtypes], axis=1)
    compare_floats.columns = ['before', 'after']
    compare_floats.apply(pd.Series.value_counts)
    print(compare_floats)

    return converted_float

# ______________________________________________________________________________
# память по колонкам до оптимизации
# get_memory_stat_by_column(my_file)

# оптимизируем
dataset = read_file(os.path.join(res_file, os.path.normpath('df_2.csv')))
converted_obj = opt_obj(dataset)
converted_int = opt_int(dataset)
converted_float =  opt_float(dataset)

optimized_dataset = dataset.copy()

optimized_dataset[converted_obj.columns] = converted_obj
optimized_dataset[converted_int.columns] = converted_int
optimized_dataset[converted_float.columns] = converted_float

print(mem_usage(dataset))
print(mem_usage(optimized_dataset))
# get_memory_with_optim(optimized_dataset)

need_column = {}
opt_dtypes = optimized_dataset.dtypes
for key in dataset.columns:
    need_column[key] = opt_dtypes[key]
    print(f'{key}:{opt_dtypes[key]}')

# сохраняем типы данных
with open(os.path.join(res_file, os.path.normpath("dtypes_2.json")), mode='w') as file:
    dtypes_json = need_column.copy()
    for key in dtypes_json.keys():
        dtypes_json[key] = str(dtypes_json[key])
    
    json.dump(dtypes_json, file)


# нужные колонки
# column_dtype = {
#     'firstSeen': pd.StringDtype(),
#     'brandName': pd.CategoricalDtype(),
#     'modelName': pd.CategoricalDtype(),
#     'askPrice': pd.StringDtype(), #np.dtype('int64'),
#     'isNew': pd.CategoricalDtype(),
#     'color': pd.CategoricalDtype(),
#     'vf_Wheels': pd.StringDtype(), #np.dtype('uint8'),
#     'vf_Seats': pd.StringDtype(), #np.dtype('uint8'),
#     'vf_Windows': pd.StringDtype(), #np.dtype('int64'),
#     'vf_WheelBaseShort': pd.StringDtype() #np.dtype('int64')
# }

# считываем нужные данные 
# has_header = True
# total_size = 0
# for part in pd.read_csv(my_file, usecols = lambda x: x in column_dtype.keys(), 
#                              dtype=column_dtype, chunksize=500_000, compression='zip'):
#     total_size += part.memory_usage(deep=True).sum()
#     print(part.shape)
#     part.dropna().to_csv(os.path.join(res_file, os.path.normpath('df_2.csv')), mode='a', header=has_header)
#     print(part.shape)
#     has_header = False
# print(total_size)

# преобразуем в данные 