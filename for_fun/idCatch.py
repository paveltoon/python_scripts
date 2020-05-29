import pandas as pd

path = input('Введите путь до файла ')
read_file = pd.read_excel('выгрузка 21.04-22.04.xlsx' or path)
file_num = 1
result_path = ''  # Записать сюда адрес файла для сохранения
result_file = open(result_path + 'Результат' + str(file_num) + '.txt', 'w+')
sep_file = 500  # Количество строк в файле для сохранения
iteration_now = 1
for index, row in read_file.iterrows():
    iteration_now += 1
    _id = row["_id"]
    if iteration_now % sep_file == 0:
        file_num += 1
        result_file.write(f'"{_id}"')
        result_file = open(result_path + 'Результат' + str(file_num) + '.txt', 'w+')
        continue
    result_file.write(f'"{_id}", ')
result_file.close()
