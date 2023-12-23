import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('result'), os.path.normpath('df_4.csv'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_types():
    with open(os.path.join(res_file, os.path.normpath('dtypes_4.json')), mode='r') as file:
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

# опыт работы, столбчатый тип
# plot = sns.histplot(data=dataset, x="experience_name", hue="experience_name", bins=100)
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('experience_name.png')))

# # Занятость, круговая
# d2 = dataset.groupby(['schedule_name'])['schedule_name'].count()
# circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
# circ.get_figure().savefig(os.path.join(res_file, os.path.normpath('schedule_name.png')))

# линейный график, суммарная минимальная зарплата по формам работы
# plt.figure(figsize=(15,10))
# plt.plot(dataset.groupby(["schedule_name"])['salary_to'].sum().values, marker='*', color='green')
# plt.savefig(os.path.join(res_file, os.path.normpath('schedule_name_salary_to.png')))

# # ящик с усами, минимальная зарплата по формам работы
# plot = sns.boxplot(data=dataset, x='salary_to', y='schedule_name')
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('salary.png')))

# корреляция
# data = dataset.copy()
# plt.figure(figsize=(16,16))
# plot = sns.heatmap(data.corr())
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('corr.png')))