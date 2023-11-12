import os
import json
import pickle

text_var = 'Данные для практической работы 2/4/products_3.pkl'
file_products = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
text_var = 'Данные для практической работы 2/4/price_info_3.json'
file_change = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))

result = os.path.join(os.path.dirname(__file__), os.path.normpath('price_change.pkl'))

def changes(prod, change):
    # print(prod['price'], 'start')
    if change['method'] == 'sum':
        prod['price'] += change['param']
    elif change['method'] == 'sub':
        prod['price'] -= change['param']
    elif change['method'] == 'percent+':
        prod['price'] *= (change['param'] + 1)
    elif change['method'] == 'percent-':
        prod['price'] *= (1 - change['param'])
    # print(prod['price'])
    


with open(file_products, "rb") as file:
    products = pickle.load(file)

with open(file_change) as file:
    info = json.load(file)

info_dict = {}
for item in info:
    info_dict[item["name"]] = item


for prod in products:
    changes(prod, info_dict[prod['name']])

# print(products)

with open(result, "wb") as file:
    file.write(pickle.dumps(products))