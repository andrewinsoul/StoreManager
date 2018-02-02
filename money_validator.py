def money_checker(string_number):
    string_number = string_number.replace(' ', '')
    if string_number.isdecimal():
        return True
    elif string_number.isdigit():
        return True
    elif ',' in string_number:
        string1 = string_number.split(',')
        for value in string1:
            if string1.index(value) == 0:
                if not(value.isdigit() or value.isdecimal()):
                    return False
                continue
            elif len(value) != 3:
                return False
            elif value.isdigit() or value.isdecimal():
                continue
            else:
                return False
        return True
    else:
        return False


def wrapper(word, width=43):
    w = word.split()
    w_string = ''
    n = 1
    for value in w:
        if len(w_string) < width*n:
            w_string += value
            w_string += ' '
        else:
            w_string += '\n\t\t\t          '
            w_string += value
            w_string += ' '
            n = n + 1
    return w_string


def money_formatter(money):
    if ',' in money:
        money = money.replace(',', '')
    if ' ' in money:
        money = money.replace(' ', '')
    return money