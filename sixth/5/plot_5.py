import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

first = os.path.join(os.path.dirname(__file__), os.path.normpath('result'), os.path.normpath('df_5.csv'))
res_file = os.path.join(os.path.dirname(__file__), os.path.normpath('result'))

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_types():
    with open(os.path.join(res_file, os.path.normpath('dtypes_5.json')), mode='r') as file:
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


# линейный тип
# dataset['H_group'] = (dataset['H'] // 10) * 10
# grouped_df = dataset.groupby('H_group')['H'].mean().reset_index()
# plt.plot(grouped_df['H_group'], grouped_df['H'])
# plt.savefig(os.path.join(res_file, os.path.normpath('H.png')))

# гистограмма
# plot = sns.histplot(data=grouped_df, x="H", hue="H", bins=100)
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('H_mean.png')))

# круговая, без наиболее распространенного класса и наименее распространенных
data = dataset[dataset['class'] != 'MBA']
d2 = data.groupby(['class'])['class'].count()
d2 = d2[d2 > len(data) * 0.05]
circ = d2.plot(kind='pie', y=d2.keys(), autopct='%1.0f%%', title='')
plt.tight_layout()
circ.get_figure().savefig(os.path.join(res_file, os.path.normpath('class.png')))

# ящик с усами
# plot = sns.boxplot(data=dataset, x='diameter', y='class')
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('diameter.png')))

# корреляция
# data = dataset.copy()
# plt.figure(figsize=(16,16))
# plot = sns.heatmap(data.corr())
# plot.get_figure().savefig(os.path.join(res_file, os.path.normpath('corr.png')))