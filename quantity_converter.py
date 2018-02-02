def qty_converter(quantity):
    if quantity == '0':
        return 0
    value1 = ''
    n = 0
    a = 1
    ans = 0
    if '+' in quantity:
        quantity_list = quantity.split('+')
        for qty in quantity_list:
            for value in qty:
                if value.isalpha():
                    break
                elif value.isspace():
                    continue
                value1 += value
            value1 = int(value1)
            if 'pcs' in qty:
                ans += value1
            elif 'dzn' in qty:
                ans += value1 * 12
            elif 'grs' in qty:
                ans += value1 * 144
            n += 1
            if n == a:
                value1 = ''
                a += 1
        return ans

    else:
        for index in quantity:
            if index.isalpha():
                break
            elif index.isspace():
                continue
            value1 += index
        value1 = int(value1)
        if 'pcs' in quantity:
            return value1
        elif 'dzn' in quantity:
            return value1 * 12
        elif 'grs' in quantity:
            return value1 * 144


def per_product(price):
    value = ''
    for index in price:
        if index ==',':
            continue
        if index == ' ':
            break
        value += index
    value = int(value)
    if 'pcs' in price:
        return value
    elif 'dzn' in price:
        return value
        # return int(round(value/12, 0))
    elif 'grs' in price:
        # return int(round(value/144, 0))
        return value
    else:
        raise ('IOError', 'invalid unit, unit must be grs, dzn or pcs')
