import os
import json
import msgpack

text_var = 'Данные для практической работы 2/3/products_2.json'
my_file = os.path.join(os.path.dirname(__file__), os.path.normpath(text_var))
result = os.path.join(os.path.dirname(__file__), os.path.normpath('res_product.json'))
r_product = os.path.join(os.path.dirname(__file__), os.path.normpath('r_product.msgpack'))

# считываем файл
with open(my_file) as file:
    data = json.load(file)
# print(data)

products = {}
for items in data:
    if items['name'] in products:
        products[items['name']].append(items['price'])
    else:
        products[items['name']] = [items['price']]
# print(len(products))

products_price = []
for item in products:
    avr = sum(products.get(item)) / len(products.get(item))
    minp = min(products.get(item))
    maxp = max(products.get(item))
    products_price.append({'name': item, 
                           'max': maxp, 
                           'min': minp,
                           'avr': avr})
# print(products_price)
    
with open(result, 'w') as res:
    res.write(json.dumps(products_price))

with open(r_product, 'wb') as res:
    res.write(msgpack.dumps(products_price))

print(f'res_json    = {os.path.getsize(result)}')
print(f'res_msgpack = {os.path.getsize(r_product)}')