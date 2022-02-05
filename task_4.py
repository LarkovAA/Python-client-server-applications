list_word_bytes = []
available_word = True

while True:
    word = input('Введите слова для преобразования слова из строкового в байтовом виде.(Если хотите выйти наберите /q или /Q: ')
    if word == '/q' or word == '/Q':
        break
    available_word = True
    for _ in word:
        try:
            number = int(_)
        except:
            continue
        if type(number) == int:
            print('Введите слова без цифр')
            available_word = False
            break
    if available_word:
        list_word_bytes.append(word)

for word in list_word_bytes:
    encod_word = word.encode('utf-8')
    decod_word = encod_word.decode('utf-8')
    print(f'Байтовый вид:{encod_word}, Строковый вид:{decod_word}')