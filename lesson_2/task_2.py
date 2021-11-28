"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:

    a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
    цена (price), покупатель (buyer), дата (date). Функция  должна предусматривать запись данных в виде словаря
    в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;

    b. Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений
    каждого параметра.
"""
import json
import datetime

FILE = './data/orders.json'


def write_order_to_json(item, qtty, price, buyer, date):
    """
    Write data to JSON file

    :param item: str product name
    :param qtty: int quantity
    :param price: product price
    :param buyer: customer
    :param date: date
    :return: None
    """
    data = {
        "item": item,
        "qtty": qtty,
        "price": price,
        "buyer": buyer,
        "date": date,
    }

    with open(FILE, 'r+', encoding='utf-8') as f_n:
        obj = json.load(f_n)
        print(obj)
        obj["orders"].append(data)
        f_n.seek(0)
        json.dump(obj, f_n, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    today = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")
    write_order_to_json('book', 29, 34.45, 'John Dow', today)

    with open(FILE, encoding='utf-8') as file:
        print(file.read())
