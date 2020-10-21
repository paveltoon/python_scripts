file = open("deadlines.txt", 'r+')
arr = file.read().split('\n')
res_file = open("new.txt", 'w+')
for i, elem in enumerate(arr):
    if "CCN: " in elem:
        res_file.write(f'{elem.split("CCN: ")[1].split("; created")[0]}\n')
res_file.close()
