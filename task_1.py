list_word = ['разработка', 'сокет']
unicode_list_word = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', '\u0441\u043e\u043a\u0435\u0442']

for num in range(len(list_word)):
    print(f'Слово:{list_word[num]}. Кодовая точка:{unicode_list_word[num]}')