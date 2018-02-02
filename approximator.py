def price_estimator(price):
    """
    :param price:
    :return an approximated value of price, if the last digit is less than five, it's rounded to 0 and 1 is
    added to the value before the last value if last value id greater than 5, the returned value will always
    have zero as it's last value.:
    Examples:
    price_estimator(40693) = 40,690
    price_estimator(40698) = 40,700
    """
    price = list(str(price))
    if int(price[-1]) != 0:
        last_digit = int(price.pop())
        if last_digit >= 5:
            if int(price[-1]) != 9:
                price[-1] = str(int(price[-1])+1)
            else:
                n = 0
                while int(price[-1]) == 9:
                    price.pop()
                    n += 1
                price[-1] = str(int(price[-1])+1)
                price += ['0']*n
        price.append('0')
    price = ''.join(price)
    return '{0:,}'.format(int(price))