list_word_bytes = []
available_word = True

while True:
    word = input('Введите слова для определения, что из них можно записать в байтовом виде.(Если хотите выйти наберите /q или /Q: ')
    if word == '/q' or word == '/Q':
        break
    list_word_bytes.append(word)

for word in list_word_bytes:
    available_word = True
    for letter in word:
        num = ord(letter)
        if num >= 126:
            print(f'{word} данное слово нельзя записать в байтовом виде')
            available_word = False
            break
    if available_word:
        print(f'{word} данное слово можно записать в байтовом виде')