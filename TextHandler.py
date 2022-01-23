from Consts import STATUS_FOLDER
import Utils
from spellchecker import SpellChecker


class TextHandler:
    def __init__(self):
        self.spell = SpellChecker()
        self.no_alternatives = ['no', 'no.', 'no,']
        self.class_alternatives = ['class', 'clans']

    def get_all_misspellings_for_word(self, word, edit_distance=1):
        if(edit_distance == 1):
            return self.spell.edit_distance_1(word)
        else:
            return self.spell.edit_distance_1(word)

    def check_if_string_contain_appnum_tag(self, str):
        no_check = map(lambda t: t in str.lower()).reduce(
            lambda t1, t2: t1 or t2)
        class_check = ('class' in str.lower() or 'clans' in str.lower())
        if(no_check == True and class_check == True):
            return True
        elif no_check == True:
            class_alternatives = self.get_all_misspellings_for_word('class')
            for word in class_alternatives:
                if(word in str.lower()):
                    return True
            return False
        return False

    def parse_numbers_from_string(self, s):
        application_number = -1
        class_number = -1
        tokens = s.split(' ')
        # save index of every token contain at least one digit
        for i, t in enumerate(tokens):
            if(TextHandler.check_if_word_includes_digit()):
                if(i > 0 and tokens[i-1] in self.no_alternatives):
                    application_number = tokens[i]
                elif(i > 0 and tokens[i-1] in self.class_alternatives or self.get_all_misspellings_for_word('class')):
                    class_number = tokens[i]
        return application_number, class_number

    @staticmethod
    def check_if_word_includes_digit(word):
        for ch in word:
            if(ch.is_digit()):
                return True
        return False
