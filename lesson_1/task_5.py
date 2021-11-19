"""
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице.
"""
import subprocess
from chardet import detect


def ping(url, count=4):
    subproc_ping = subprocess.Popen(['ping', url], stdout=subprocess.PIPE)
    n = 0
    for reply in subproc_ping.stdout:
        code = detect(reply)['encoding']
        reply = reply.decode(code).encode('utf-8').decode('utf-8')
        print(reply, end='')
        if n == count:
            print()
            break
        n += 1


URLS = ['yandex.ru', 'google.com']

for url in URLS:
    ping(url)
