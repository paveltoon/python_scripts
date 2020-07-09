num = 0
wpa_py = open("wpa_py.txt", "w+")
while num < 99999999:
    t = ""
    num += 1
    if len(t) + len(str(num)) < 8:
        t += "0"*(8 - len(str(num))) + str(num)
    else:
        t = str(num)
    print(t)
    wpa_py.write(f"{t}\n")
wpa_py.close()