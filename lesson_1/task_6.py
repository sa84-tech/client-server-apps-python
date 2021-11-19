"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
программирование», «сокет», «декоратор». Проверить кодировку файла по
умолчанию. Принудительно открыть файл в формате Unicode и вывести его
содержимое.
"""
from chardet import detect

WORDS = ['сетевое программирование\n', 'сокет\n', 'декоратор']

with open('test_file.txt', 'w') as file:
    file.writelines(WORDS)

with open('test_file.txt', 'rb') as file:
    code = detect(file.read())['encoding']
print('File encoding:', code)

with open('test_file.txt', encoding=code) as file:
    print('File content:')
    print(file.read())
