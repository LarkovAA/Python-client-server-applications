import chardet
import re
import csv

system_parameters_list = []
file_list = []
os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

while True:
    name_file = input('Введите путь к файлу в формате txt который хотите проверить по определенным параметрам (нажмите \q или \Q для выхода): ')
    if name_file == '\q' or name_file == '\Q':
        break
    if name_file[-4:] != '.txt':
        print('Введите правильное название файла формата txt')
    else:
        system_parameters_list.append(name_file)

# Не придумал что можно сделать что бы мы сами выбирали какие строки просмотреть поэтому закоментил
# while True:
#     name_parameter = input('Введите название параметров которые хотите определить в введенных ранее файлах (нажмите \q или \Q для выхода): ')
#     if name_parameter == '\q' or name_file == '\Q':
#         break
#     else:
#         file_list.append(name_parameter)

def write_to_csv(file_list):
    for file in file_list:
        with open(file, 'rb') as fil:
            coding = fil.read()
        encoding = chardet.detect(coding)['encoding']
        get_data(encoding, file)
    main_data.append(os_prod_list)
    main_data.append(os_name_list)
    main_data.append(os_code_list)
    main_data.append(os_type_list)

    # Создаем заголовок для CSV файла в него доб наименование мараметров столбец и наименование файлов какие данные мы из каждого вытащили
    name_columns = ['Название параметров']
    for i in range(len(system_parameters_list)):
        name_columns.append(system_parameters_list[i])
    # Данный заголовок доб 1 к файлу CSV
    trans_main_data = []
    trans_main_data.append(name_columns)
    # Транспонируем наш список таким образом что бы было коректное отображение данных
    for i in range(len(main_data[0])):
        add_list = [main_data[0][i]]
        for _ in main_data[i+1]:
            add_list.append(_)
        trans_main_data.append(add_list)

    with open('summary_table.csv', 'w', encoding='utf-8') as s_t:
        s_t_writer = csv.writer(s_t)
        s_t_writer.writerows(trans_main_data)

def get_data(encoding, file):
    stop = 0
    with open(file, 'r', encoding=encoding) as fil:
        for line in fil:
            if os_prod_line := re.findall(r"(\AИзготовитель системы:)(\s+)(.+)", line):
                os_prod_list.append(os_prod_line[0][2])
                stop += 1
            if os_name_line := re.findall(r"(\AНазвание ОС:)(\s+)(.+)", line):
                os_name_list.append(os_name_line[0][2])
                stop += 1
            if os_code_line := re.findall(r"(\AКод продукта:)(\s+)(.+)", line):
                os_code_list.append(os_code_line[0][2])
                stop += 1
            if os_type_line := re.findall(r"(\AТип системы:)(\s+)(.+)", line):
                os_type_list.append(os_type_line[0][2])
                stop += 1
            if stop == 4:
                break

write_to_csv(system_parameters_list)