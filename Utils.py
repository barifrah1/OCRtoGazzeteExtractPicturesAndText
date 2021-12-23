import datetime
import os
# get: integer, returns its roman number as string


def int_to_Roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

# convert date from yy-mm-dd to d.m.yyyy


def convert_file_date(file_date):
    DAY = 0
    MONTH = 1
    YEAR = 2
    formatted = datetime.datetime.strptime(
        '19'+file_date, '%Y-%m-%d').strftime('%d.%m.%y')
    result = formatted.split('.')
    if(int(result[DAY]) < 9):  # day
        result[DAY] = result[DAY][1]  # remove zero
    if(int(result[MONTH]) < 9):
        result[MONTH] = result[MONTH][1]  # remove zero
    return result[DAY]+'.'+result[MONTH]+'.'+'19'+result[YEAR]


def is_htm_file(file_name):
    return len(file_name.split('.')) > 1 and file_name.split('.')[1] == 'htm'


def parse_numbers_from_string(s, excel_rows_for_date):
    numbers = []
    current = []
    for index, t in enumerate(s):
        if(t.isdigit()):
            current.append(t)
        else:
            if((t == ' ' or t == ',' or (t == '.' and index+1 < len(s) and s[index+1].isdigit() == False)) and len(current) > 0):
                try:
                    num = int(''.join(map(str, current)))
                except Exception as e:
                    candidates = []
                    application_and_class_array = excel_rows_for_date[[
                        "Application No.", "Class No."]].values
                    for row in application_and_class_array:
                        if(len(numbers) == 0):  # application_number
                            candidate = str(int(row[0])).lower()
                            candidates.append(candidate)
                        elif(len(numbers) == 1):
                            candidate = str(int(row[1])).lower()
                            candidates.append(candidate)
                        else:
                            return numbers
                    results = process.extract(s.lower(), candidates)
                    if(results[0][1] > results[1][1]):
                        num = int(results[0][0])
                    else:
                        num = -1
                numbers.append(num)
                current = []
            else:
                if(len(current) > 0 and current[0].isdigit()):
                    current.append(t)
    return numbers


def create_folder_if_not_exist(folder_name):
    # if status folder doesnt exist yet, create it
    if(os.path.exists(folder_name) == False):
        os.mkdir(folder_name)


def check_if_num_in_string(num, tag):
    if(str(num) in tag.text):
        return True
    else:
        return False


def remove_og_from_date(date):
    if(date is not None and date != ""):
        return date.split(' ')[1]
    else:
        raise ValueError


def get_only_zero_value_from_dict(dict):
    keys_with_zero_values = []
    for key in dict.keys():
        if(dict[key] == 0):
            keys_with_zero_values.append(key)
    return keys_with_zero_values
