list_word_bytes = []
available_word = True

while True:
    word = input('Введите слова из латинских букв.(Если хотите выйти наберите /q или /Q: ')
    available_word = True
    if word == '/q' or word == '/Q':
        available_word = False
        break
    for _ in word:
        num = ord(_)
        if num >= 126:
            print('Введите символ латинского алфавита')
            available_word = False
            break
    if available_word:
        list_word_bytes.append(word)

for _ in list_word_bytes:
    word_bytes = bytes(_, encoding="utf-8")
    print(f'{word_bytes} {type(word_bytes)} Длинна:{len(_)}')