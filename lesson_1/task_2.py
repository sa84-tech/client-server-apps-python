"""
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""
from task_1 import display_format


WORDS = ['class', 'function', 'method']

for word in WORDS:
    word_b = eval(f"b'{word}'")
    display_format(word_b)
