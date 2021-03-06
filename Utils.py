import datetime
import os
from fuzzywuzzy import fuzz, process, utils

# convert integer to roman number for example : 1 to I, 2 to II


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


# convert roman string to int
def roman_to_int(S: str) -> int:
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    summ = 0
    for i in range(len(S)-1, -1, -1):
        num = roman[S[i]]
        if 3*num < summ:
            summ = summ-num
        else:
            summ = summ+num
    return summ

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

# check if file is .htm


def is_htm_file(file_name):
    return len(file_name.split('.')) > 1 and file_name.split('.')[1] == 'htm'


def parse_numbers_from_string(s, excel_rows_for_date, keys_not_found_yet):
    numbers = []
    current = []
    for index, t in enumerate(s):
        if(t.isdigit()):
            current.append(t)
        else:
            if((t == ' ' or t == ',' or (t == '.' and index+1 < len(s) and s[index+1].isdigit() == False)) and len(current) > 0):
                try:
                    num = int(''.join(map(str, current)))
                    if(len(numbers) == 0 and num not in keys_not_found_yet):
                        raise Exception(
                            "application number not in keys_not_found_yet")
                except Exception as e:
                    candidates = []
                    application_and_class_array = excel_rows_for_date[[
                        "Application No.", "Class No."]].values
                    for row in application_and_class_array:
                        if(row[0] not in keys_not_found_yet):
                            continue
                        if(len(numbers) == 0):  # application_number
                            candidate = str(int(row[0])).lower()
                            candidates.append(candidate)
                        elif(len(numbers) == 1):
                            candidate = str(int(row[1])).lower()
                            candidates.append(candidate)
                        else:
                            return numbers
                    results = process.extract(s.lower(), candidates)
                    if(len(results) > 1 and results[0][1] > results[1][1]):
                        num = int(results[0][0])
                    else:
                        num = -1
                numbers.append(num)
                current = []
            else:
                if(len(current) > 0 and current[0].isdigit()):
                    current.append(t)
    return numbers


def check_if_string_contain_appnum_tag(string):
    return ('No.' in string or 'No,' in string or 'No ') and ('Class' in string or 'Clans' in string)
# check if one of array elements is in the string


def is_array_element_in_string(string, array):
    for a in array:
        result = check_if_num_in_text(a, string)
        if(result):
            return a
    return -1

# get folder name and checks if it already exists , if not create it using mkdir


def create_folder_if_not_exist(folder_name):
    # if status folder doesnt exist yet, create it
    if(os.path.exists(folder_name) == False):
        os.mkdir(folder_name)

# checks if num shows in tag.text


def check_if_num_in_string(num, tag):
    if(str(num) in tag.text):
        return True
    else:
        return False


# checks if num is in string


def check_if_num_in_text(num, s):
    if(str(num) in s):
        return True
    else:
        return False


# remove the word OG from string


def remove_og_from_date(date: str):
    if(date is not None and date != ""):
        return date.split(' ')[1]
    else:
        raise ValueError

# get dictionary and return keys with value is 0


def get_only_zero_value_from_dict(dict):
    keys_with_zero_values = []
    for key in dict.keys():
        if(dict[key] == 0):
            keys_with_zero_values.append(key)
    return keys_with_zero_values


def convert_to_int_then_str(x):
    try:
        y = str(int(x))
        return y
    except Exception as e:
        raise Exception(f"Cannot convert {x} to int or string")

# get row from excel , return trademark type


def parse_trademark_type(row):
    if('Word' in str(row['Symbol Contents'].values[0]) and 'Symbol' in str(row['Symbol Contents'].values[0])):
        return 'Image'
    elif(('Word' in str(row['Symbol Contents'].values[0]) and str(row['Sign'].values[0]) != '')):
        return 'Text'
    else:
        return 'Image'


def add_curly_braces_to_string(s):
    return '{'+s+'}'
