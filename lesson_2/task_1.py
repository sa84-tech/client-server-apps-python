"""
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый "отчетный" файл в формате CSV. Для этого:

    a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
    данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
    "Изготовитель системы", "Название ОС", "Код продукта", "Тип системы". Значения каждого параметра поместить
    в соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
    os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data —
    и поместить в него названия столбцов отчета в виде списка: "Изготовитель системы", "Название ОС", "Код продукта",
    "Тип системы". Значения для этих столбцов также оформить в виде списка и поместить в файл main_data
    (также для каждого файла);

    b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
    функции реализовать получение данных через вызов функции get_data(), а также
    сохранение подготовленных данных в соответствующий CSV-файл;

    c. Проверить работу программы через вызов функции write_to_csv().
"""
import csv
import re

FILES = ['./data/info_1.txt', './data/info_2.txt', './data/info_3.txt']


def get_data(files=[]):
    main_data = [["Изготовитель системы", "Название ОС", "Код продукта", "Тип системы"]]
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for file in files:

        with open(file) as f:
            text = f.readlines()

        for line in text:
            if re.match('Изготовитель системы', line):
                os_prod_list.append(line.split(':')[1].strip())
            elif re.match('Название ОС', line):
                os_name_list.append(line.split(':')[1].strip())
            elif re.match('Код продукта', line):
                os_code_list.append(line.split(':')[1].strip())
            elif re.match('Тип системы', line):
                os_type_list.append(line.split(':')[1].strip())

    new_list = list(zip(os_prod_list, os_name_list, os_code_list, os_type_list))
    main_data.extend(new_list)
    return main_data


def write_to_csv(files):
    print(get_data(files))


write_to_csv(FILES)
