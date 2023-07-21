wiki = {15, 4, 2, 17, 6, 13, 11, 8, 10, 24, 33, 20, 31, 22, 29, 28, 35, 26}
test = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

equals = 0

for i in wiki:
    for j in test:
        if i == j:
            equals += 1
            break

if equals == len(wiki):
    print("The arrays are the same!")

else:
    print("Error! The two arrays do not have the same numbers :(")


