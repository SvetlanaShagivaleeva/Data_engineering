import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('result'), os.path.normpath('df_3.csv'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_types():
    with open(os.path.join(res_file, os.path.normpath('dtypes_3.json')), mode='r') as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype()
        elif dtypes[key] == 'string':
            dtypes[key] = pd.StringDtype()
        else:
            dtypes[key] = np.dtype(dtypes[key])
    return dtypes


need_dtypes = read_types()

dataset = pd.read_csv(first, usecols=lambda x: x in need_dtypes.keys(),
            dtype=need_dtypes)

dataset.info(memory_usage='deep')

# распределение по дням недели, столбчатый тип
# plot = sns.histplot(data=dataset, x="DAY_OF_WEEK", hue="DAY_OF_WEEK", bins=100)
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('DAY_OF_WEEK.png')))

# AIRLINE, круговая
# d2 = dataset.groupby(['AIRLINE'])['AIRLINE'].count()
# circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
# circ.get_figure().savefig(os.path.join(res_file, os.path.normpath('AIRLINE.png')))

# линейный график, количество такси в аэропортах
# plt.figure(figsize=(15,10))
# plt.plot(dataset.groupby(["AIRLINE"])['TAXI_IN'].sum().values, marker='*', color='green')
# plt.savefig(os.path.join(res_file, os.path.normpath('AIRLINE_TAXI_IN.png')))

# ящик с усами, дистанции в год
# plot = sns.boxplot(data=dataset, x='YEAR', y='DISTANCE')
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('DISTANCE_in_YEAR.png')))

# корреляция
# data = dataset.copy()
# plt.figure(figsize=(16,16))
# plot = sns.heatmap(data.corr())
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('corr.png')))