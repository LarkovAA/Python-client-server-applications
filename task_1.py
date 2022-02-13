import chardet
import re
import csv

system_parameters_list = ['task_1/info_1.txt', 'task_1/info_2.txt', 'task_1/info_3.txt']
os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]

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

    trans_main_data = []
    trans_main_data.append(main_data[0])
    for i in range(len(system_parameters_list)):
        trans_main_data.append([main_data[1][i], main_data[2][i], main_data[3][i], main_data[4][i]])

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