"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

WORDS = ['attribute', 'класс', 'функция', 'type']

for word in WORDS:
    try:
        bytes(word, 'ascii')
    except UnicodeEncodeError:
        print(f'The word {word} cannot be written in byte type')
