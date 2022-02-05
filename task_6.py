import chardet

with open('test_file.txt', 'w') as test_file:
    while True:
        text = input('Введите текст который хотите записать в файл test_file.txt. (Если хотите выйти наберите /q или /Q): ')
        if text == '/q' or text == '/Q':
            break
        print(f'{text}', file=test_file)

with open('test_file.txt', 'rb') as test_file:
    text = test_file.read()
encod_text = chardet.detect(text)['encoding']

with open('test_file.txt', encoding=encod_text) as test_file:
    for text in test_file:
        print(text, end='')
