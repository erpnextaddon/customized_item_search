
import re
from num2words import num2words

def convert_number_to_given_language(number, language):
    """
    return the number in arabic
    """
    return num2words(number, lang=language)