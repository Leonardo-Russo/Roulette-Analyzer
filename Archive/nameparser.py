def get_first_name(fullname):
    firstname = ''
    try:
        firstname = fullname.split()[0] 
    except Exception as e:
        print(str(e))
    return firstname

def get_last_name(fullname):
    lastname = ''
    try:
        index=0
        for part in fullname.split():
            if index > 0:
                if index > 1:
                    lastname += ' ' 
                lastname +=  part
            index += 1
    except Exception as e:
            print(str(e))
    return lastname

def get_last_word(string):
    return string.split()[-1]
