import datetime

#get: integer, returns its roman number as string
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
    while  num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

#convert date from yy-mm-dd to d.m.yyyy
def convert_file_date(file_date):
    DAY=0
    MONTH = 1
    YEAR= 2
    formatted = datetime.datetime.strptime('19'+file_date, '%Y-%m-%d').strftime('%d.%m.%y')
    result = formatted.split('.')
    if(result[DAY]<9): #day
        result[DAY]= result[DAY][1] #remove zero
    if(result[MONTH]<9):
        result[MONTH] = result[MONTH][1] #remove zero
    return result[DAY]+'.'+result[MONTH]+'.'+result[YEAR]
        
    