"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование
(используя методы encode и decode).
"""


def enc(str_value=None):
    try:
        encoded_value = str_value.encode('utf-8')
        print(encoded_value)
        return encoded_value
    except AttributeError as error:
        print(f'Error with value "{str_value}":\n{error}')
        return None


def dec(byte_value=None):
    try:
        decoded_value = byte_value.decode('utf-8')
        print(decoded_value)
        return decoded_value
    except AttributeError as error:
        print(f'Error with value "{byte_value}":\n{error}')
        return None


WORDS = ['разработка', 'разработка', 'protocol', 'standard']

for word in WORDS:
    enc_word = enc(word)
    if enc_word:
        dec_word = dec(enc_word)
