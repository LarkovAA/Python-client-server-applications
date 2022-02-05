import chardet
import subprocess
import platform

param = '-n' if platform.system().lower() == 'windows' else '-c'
list_websites = []
while True:
    web = input('Введите сайты которые хотите пинговать.(Если хотите выйти наберите /q или /Q): ')
    if web == '/q' or web == '/Q':
        break
    available_web = True
    if not web.index('.') or web[-3:] != 'com' or web[-2:] != 'ru':
        print('Введите коректное название сайт необходимо что бы было доменное имя ')
        available_web = False
    if available_web:
        list_websites.append(web)

for website in list_websites:
    number = input(f'Введите колличество пакетов которые хотите отправить на вебсайт {website}: ')
    args = ['ping', param, number, website]
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in result.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))