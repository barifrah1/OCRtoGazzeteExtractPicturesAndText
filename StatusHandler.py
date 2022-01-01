from Consts import STATUS_FOLDER
import Utils


class StatusHandler:
    def __init__(self, paper_name):
        self.paper_name = paper_name

    def write_to_file(self, application_number, i):
        try:
            new_i = i
            if(i == -1 or i == -2):
                new_i = 'x'
            with open('./'+STATUS_FOLDER+'/'+self.paper_name+'.txt', 'a') as fa:
                fa.write(str(application_number)+'-'+str(new_i)+'\n')
                fa.close()
        except:
            raise("Exception: writing to status file")
