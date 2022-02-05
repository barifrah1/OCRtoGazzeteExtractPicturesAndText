from Consts import ACCURACY_FILE_NAME, STATUS_FOLDER, XML_FOLDER
import Utils
import os


class AccuracyCalculator:
    def __init__(self, paper_name, result):
        self.paper_name = paper_name
        self.real_app_num_to_image_name_dict = None
        self.result = result
        self.accuracy = None
        self.read_accuracy_file()
        self.calculate_accuracy(self.result)

    def read_accuracy_file(self):
        IMAGE_NAME_INDEX = 0
        APP_NUM_INDEX = 1
        if(Utils.is_paper_folder_exist(self.paper_name) and Utils.is_real_file_exist(self.paper_name)):
            try:
                with open('./'+XML_FOLDER+'/'+self.paper_name+'/word/media/'+ACCURACY_FILE_NAME, 'r') as fa:
                    self.real_app_num_to_image_name_dict = {}
                    line = fa.readline()
                    while(line != ''):
                        image_name = line.split('-')[IMAGE_NAME_INDEX]
                        app_num_with_backslash = line.split('-')[APP_NUM_INDEX]
                        app_num = app_num_with_backslash.split('\n')[0]
                        self.real_app_num_to_image_name_dict[app_num] = image_name
                        line = fa.readline()
                    fa.close()
            except:
                print(f"reading from real file failed {self.paper_name}")
                raise("Exception: reading from real file failed")

    def calculate_accuracy(self, result):
        hits = 0
        misses = 0
        misses_text = ""
        try:
            for app_num, image_name in self.real_app_num_to_image_name_dict.items():
                if(app_num not in result.keys()):
                    continue
                result_image_num = result[app_num].split('.')[0]
                if(image_name == result_image_num):
                    hits += 1
                else:
                    misses += 1
                    misses_text += app_num+": guess:"+result_image_num+" real:"+image_name+','
        except Exception as e:
            print(e, app_num)
            raise e
        try:
            accuracy = hits/len(self.real_app_num_to_image_name_dict.keys())
            print(
                f"accuracy for {self.paper_name} is: {accuracy}, num of hits: {hits}/{len(self.real_app_num_to_image_name_dict.keys())} , misses: {misses}, identified:{hits+misses}, misses_text:{misses_text}")
            AccuracyCalculator.write_to_accuracy_file(
                f"accuracy for {self.paper_name} is: {accuracy}, num of hits: {hits}/{len(self.real_app_num_to_image_name_dict.keys())}, misses: {misses}, identified:{hits+misses}, misses_text:{misses_text}")
            return accuracy
        except ZeroDivisionError:
            print('divide by zero is not allowed')

    @ staticmethod
    def write_to_accuracy_file(line_to_write):
        with open('./accuracy/log.txt', 'a') as f:
            f.write(line_to_write)
            f.write('\n')
            f.close
