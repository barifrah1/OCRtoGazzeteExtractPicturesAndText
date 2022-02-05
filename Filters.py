from ExcelHandler import ExcelHandler
from shutil import copy


class Filters():
    list_to_filter = []
    filterd_list = []

    @staticmethod
    def Filter():
        copy_of_list_to_filter = Filters.list_to_filter.copy()
        Filters.filterd_list = Filters.intersection_of_lists(
            copy_of_list_to_filter)
        return Filters.filterd_list

    @staticmethod
    def intersection_of_lists(lists):
        if(len(lists) == 0):
            return []
        if(len(lists) == 1):
            return lists[0]
        else:
            new_lists = lists
            new_lists[1] = list(set(lists[0]) & set(lists[1]))
            return Filters.intersection_of_lists(new_lists[1:])

    @staticmethod
    def filter_list_of_applications_number_by_app_num_and_class(rows_for_date, application_number, class_number):
        application_number = int(application_number)
        class_number = int(class_number)
        if(application_number != -1):
            row_data = ExcelHandler.get_rowdata_by_application_number(
                rows_for_date, str(application_number))
            if(row_data['class_number'] == str(class_number)):
                Filters.list_to_filter.append([application_number])
                return 'ONE'

            else:
                Filters.list_to_filter.append([application_number])
                return 'ONE'
        else:
            return 'ZERO'

    @staticmethod
    def filter_list_of_application_numbers_by_application_date(rows_for_date, application_date):
        filter_flag = 'MULTIPLE'
        candidates_by_date = ExcelHandler.get_application_numbers_by_application_date(
            rows_for_date, application_date)
        if(len(candidates_by_date) == 1):
            filter_flag = "ONE"
            Filters.list_to_filter.append(candidates_by_date)
        elif(len(candidates_by_date) == 0):
            filter_flag = "ZERO"
        else:
            filter_flag = "MULTIPLE"
            Filters.list_to_filter.append(candidates_by_date)
        return filter_flag

    @staticmethod
    def filter_list_of_application_numbers_by_class_number(rows_for_date, class_number):
        candidates_by_class = ExcelHandler.get_application_numbers_by_class(
            rows_for_date, class_number)
        if(len(candidates_by_class) == 1):
            filter_flag = "ONE"
            Filters.list_to_filter.append(candidates_by_class)
        elif(len(candidates_by_class) == 0):
            filter_flag = "ZERO"
        else:
            filter_flag = "MULTIPLE"
            Filters.list_to_filter.append(candidates_by_class)
        return filter_flag

    @staticmethod
    def filter_list_of_application_numbers_by_country(rows_for_date, countries_in_text):
        candidates_by_country = ExcelHandler.get_application_number_by_country(
            rows_for_date, countries_in_text)
        if(len(candidates_by_country) == 1):
            filter_flag = "ONE"
            Filters.list_to_filter.append(candidates_by_country)
        elif(len(candidates_by_country) == 0):
            filter_flag = "ZERO"
        else:
            filter_flag = "MULTIPLE"
            Filters.list_to_filter.append(candidates_by_country)
        return filter_flag

    @staticmethod
    def filter_list_of_application_numbers_by_city(rows_for_date, cities_in_text):
        candidates_by_city = ExcelHandler.get_application_number_by_city(
            rows_for_date, cities_in_text)
        if(len(candidates_by_city) == 1):
            filter_flag = "ONE"
            Filters.list_to_filter.append(candidates_by_city)
        elif(len(candidates_by_city) == 0):
            filter_flag = "ZERO"
        else:
            filter_flag = "MULTIPLE"
            Filters.list_to_filter.append(candidates_by_city)
        return filter_flag

    @staticmethod
    def filter_list_of_application_numbers_by_applicant(rows_for_date, applicants_in_text):
        candidates_by_applicant = ExcelHandler.get_application_number_by_city(
            rows_for_date, applicants_in_text)
        if(len(candidates_by_applicant) == 1):
            filter_flag = "ONE"
            Filters.list_to_filter.append(candidates_by_applicant)
        elif(len(candidates_by_applicant) == 0):
            filter_flag = "ZERO"
        else:
            filter_flag = "MULTIPLE"
            Filters.list_to_filter.append(candidates_by_applicant)
        return filter_flag
