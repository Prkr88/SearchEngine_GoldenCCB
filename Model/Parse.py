def parse_doc(doc):
    '''print(doc)'''
    numbers_rules("10,123,000,000")
    numbers_rules("123")
    numbers_rules("1010.56")
    numbers_rules("10,123,000")
    numbers_rules("55")


'''this function converts all the number in the document acording to the rules'''


def numbers_rules(num_str):
    num_edit = num_str.replace(",", "")
    number_split = num_edit.split(".", 1)
    before_point = number_split[0]
    if len(number_split) > 1:
        after_point = number_split[1]
    else:
        after_point = ''
    if len(before_point) > 9:
        ans = format_num(before_point, 'B', 9, after_point)
    elif len(before_point) > 6:
        ans = format_num(before_point, 'M', 6, after_point)
    elif len(before_point) > 3:
        ans = format_num(before_point, 'K', 3, after_point)
    else:
        if after_point != '':
            ans = before_point + '.' + after_point
        else:
            ans = before_point
    print(ans)

'''this function formats big numbers acording to rules'''


def format_num(number, sign, mode, after_point):
    zero_killer = 1
    num_desired_format = number[:-mode] + '.' + number[-mode:]
    num_desired_format = list(num_desired_format)
    while num_desired_format[len(num_desired_format) - zero_killer] == '0' and after_point == '':
        num_desired_format[len(num_desired_format) - zero_killer] = ''
        zero_killer = zero_killer + 1
    num_desired_format = "".join(num_desired_format)
    return num_desired_format + after_point + sign


def num_precent(number):
    return number + "%"


def num_dollar(number):
    return number + " Dollars"


numbers_rules("10,123,000,000")
numbers_rules("123")
numbers_rules("1010.56")
numbers_rules("10,123,000")
numbers_rules("55")
numbers_rules("55.560")
print(num_precent("100"))
print(num_dollar("100"))
