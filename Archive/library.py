from winreg import HKEY_USERS
import numpy as np
import outcome

def namecheck(archive, nmin, fullname):

    splits = fullname.split()
    N = np.size(archive)
    flag = 0
    k_save = 0

    for i in splits:
        flag = 0
        if len(i) > nmin:
            for k in range(N):
                if flag == 0:
                    for j in archive[k]:
                        if j.lower() == i.lower():
                            flag = 1
                            k_save = k
                            break
                if flag == 1:
                    break
            if flag == 1:
                break

    # print(k_save, flag)
    return k_save, flag

# history = [18, 14, 17, 15, 18, 23, 21, 27, 15, 14]
# history = np.random.randint(35, size=(10)) + 1
# print(history)

def dozencheck(history):

    # dozen1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # dozen2 = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    # dozen3 = [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]

    flag = 0

    for i in history:
        if i <= 12:
            flag = -1
            break

    if flag == 0:
        flag = 1

    if flag != 1:
        for i in history:
            if i <= 24 and i >= 13:
                flag = -2
                break

    if flag == -1:
        flag = 2

    if flag != 1 and flag != 2:
        for i in history:
            if i >= 25:
                flag = -3

    if flag == -2:
        flag = 3

    if flag == -1 or flag == -2 or flag == -3:
        flag = 0

    # print(flag)

    return flag


def rolls_add(flag, lobbyname):

    transfer_file = open(r"G:\Il mio Drive\Codes\Python\NoBet\Bot\rolls.dat", "r+")
    list = transfer_file.read()
    list_splits = list.split("\n")

    names = []

    for i in list_splits:
        if i != "":
            name = i.split("-")[0]
            name = name[:-1]            # I must remove the last space in name
            names.append(name)

    print(names)
    if not lobbyname in names:
        output = str(lobbyname) + " - " + str(flag) + "\n"
        transfer_file.write(output)

    transfer_file.close()


def rolls_remove(lobbyname):
    transfer_file = open(r"G:\Il mio Drive\Codes\Python\NoBet\Bot\rolls.dat", "r+")
    list = transfer_file.read()
    list_splits = list.split("\n")
    transfer_file.close()

    names = []
    dozens = []
    output = []

    for i in list_splits:
        if i != "":
            name = i.split("-")[0]
            dozen = i.split("-")[1]
            name = name[:-1]            # I must remove the last space in name
            names.append(name)
            dozens.append(dozen)

    for i in range(np.size(names)):
        if lobbyname != names[i]:
            single_out = str(names[i]) + " - " + str(dozens[i]) + "\n"
            output.append(single_out)
    
    transfer_file = open(r"G:\Il mio Drive\Codes\Python\NoBet\Bot\rolls.dat", "w")
    for j in output:
        transfer_file.write(j)

    transfer_file.close()

    