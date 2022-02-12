import json

def write_order_to_json(item, quantity, price, buyer, date):
    dictionary_json = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    with open('orders.json', 'w', encoding='utf-8') as o_j:
        json.dump(dictionary_json, o_j, indent=4)

write_order_to_json('кросовки', 10, 10000.00, 'Иванов Иван Иванович', '12/02/2022')
