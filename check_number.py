def isnumber(string_number):
        if string_number.isdecimal():
            return True
        elif string_number.isdigit():
            return True
        elif '.' in string_number:
            if string_number.count('.') > 1:
                return False
            string1 = string_number.split('.')
            for value in string1:
                if value.isdigit() or value.isdecimal():
                    continue
                else:
                    return False
            return True
        else:
            return False
