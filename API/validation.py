# meh

from utils import PdfField

def has_letters(arg):
    all_non_letters = False
    for x in arg:
        if x.isalpha():
            all_non_letters = True
            break
    
    return all_non_letters

def has_digits(arg):
    all_non_digits = False
    for x in arg:
        if x.isdigit():
            all_non_digits = True

    return all_non_digits

class Validator:
    def __init__(self, config):
        self.config = config

    def _validate(self, value, constraints, key):
        # print(constraints)
        # print(value)
        missing_constraints = dict()

        if ("min_char" in constraints):
            is_length_enough = constraints["min_char"] <= len(value)
            if not is_length_enough:
                missing_constraints[key] = "too short"
        
        if ("max_char" in constraints):
            is_length_not_too_long = len(value) <= constraints["max_char"]
            if not is_length_not_too_long:
                missing_constraints[key] = "too long"
        
        if ("letters_allowed" in constraints):
            if has_letters(value) and not constraints["letters_allowed"]:
                missing_constraints[key] = "letters not allowed"

        if ("numbers_allowed" in constraints):
            if has_digits(value) and not constraints["numbers_allowed"]:
                missing_constraints[key] = "numbers not allowed"

        return missing_constraints

    def validate(self, parsed_dict) -> dict:
        errors = dict()
        for key, value in parsed_dict.items():
            if key == PdfField.SENDER_NAME:
                errors.update(self._validate(value, self.config["sender"]["name"], "sender name"))
            elif key == PdfField.SENDER_STREET:
                errors.update(self._validate(value, self.config["sender"]["street"], "sender street"))
            elif key == PdfField.RECEIVER_STREET:
                errors.update(self._validate(value, self.config["receiver"]["street"], "receiver street"))
            elif key == PdfField.SENDER_ZIP_CODE:
                print(self.config["sender"]["zip"])
                print(value)
                errors.update(self._validate(value, self.config["sender"]["zip"], "sender zip code"))
            elif key == PdfField.RECEIVER_ZIP_CODE:
                errors.update(self._validate(value, self.config["receiver"]["zip"], "receiver zip code"))       
            elif key == PdfField.RECEIVER_NAME:
                errors.update(self._validate(value, self.config["receiver"]["name"], "receiver name"))
            elif key == PdfField.SENDER_CITY:
                errors.update(self._validate(value, self.config["sender"]["city"], "sender city"))
            elif key == PdfField.RECEIVER_CITY:
                errors.update(self._validate(value, self.config["receiver"]["city"], "receiver city"))
        print(errors)
        return errors

def validateName(self, name) -> str:
        if (len(name)>self.config["pdf_parameters"]["name"]["max_length"]):
            name=name[0:self.config["pdf_parameters"]["name"]["max_length"]-4]+".pdf"
            if(name.find("..")):
                name.replace("..", ".")

        for sign in self.config["pdf_parameters"]["name"]["not_allowed_characters"]:
            name.replace(sign,"")
            
        if(self.config["pdf_parameters"]["name"]["no_spaces_around"]):
            name = name.replace(".pdf","")
            name = name.strip()
            name+=".pdf"
        return name

