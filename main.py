from pathlib import Path
from string import whitespace


def transliterate_transcribe():
    translation_board = {
        "а" : "a",
        "б" : "b",
        "в" : "w",
        "г" : "h",
        "ґ" : "g",
        "д" : "d",
        "е" : "e",
        "є" : ["ê", "je", "e", "ie"],
        "ж" : ["ž", "ż"],
        "з" : "z",
        "и" : ["i", "y"],
        "і" : ["ì", "i"],
        "ї" : ["ї", "ji"],
        "й" : "j",
        "к" : "k",
        "л" : ["l", "ł"],
        "м" : "m",
        "н" : "n",
        "о" : "o",
        "п" : "p",
        "р" : "r",
        "с" : "s",
        "т" : "t",
        "у" : "u",
        "ф" : "f",
        "х" : ["h", "ch"],
        "ц" : "c",
        "ч" : ["č", "cz"],
        "ш" : ["š", "sz"],
        "щ" : ["ŝ", "szcz"],
        "ь" : ["′", "i", "ć", "ś", "ź", "ń"],
        "ю" : ["û", "ju", "u", "iu"],
        "я" : ["â", "ja", "a", "ia"],
        "’" : ["’", ""]
    }

    ukrainian_file_path = Path("/home/user/Desktop/uk.txt")

    transliteration = ""
    transcribtion = ""
    to_liter = ""
    to_scrib = ""
    # next_letter = ""
    input_decision = ""
    proceed = False

    special_characters = """1234567890`~!@#$%^&*()_+-=[]\;',./<>?:"{}|"""
    ukr_exceptions = "єжиіїлхчшщьюя’"
    consonant = "бгґджзклмнпрстфхцчшщ"
    vovels = "аеєиіїоуюяйв"
    # semivowels = "йв"


    with open(ukrainian_file_path, "r") as i_file:
        file_contents = i_file.read()
        
    for i in range(len(file_contents)):
        letter = file_contents[i]
        prev_letter = file_contents[i-1]
        if i+1 < len(file_contents):
            next_letter = file_contents[i+1]
        else:
            next_letter = ""

        if letter.isupper():
            letter = letter.lower()
            is_upper = True
        else:
            is_upper = False

        if letter in whitespace or letter in special_characters:
            transcribtion += letter
            transliteration += letter
            continue

        else:
            if letter in ukr_exceptions or letter in ukr_exceptions.upper():
                match letter:
                    case "є"|"ю"|"я":
                        to_liter = translation_board[letter][0]

                        if prev_letter == "л" or prev_letter == "Л":
                            to_scrib = translation_board[letter][2]

                        elif prev_letter in consonant or prev_letter in consonant.upper():
                            to_scrib = translation_board[letter][3]

                        else:
                            to_scrib = translation_board[letter][1]


                    # there are exceptions with words that have foreing origin
                    # in such cases "ле" is written as "le"
                    case "л":
                        to_liter = translation_board[letter][0]

                        # precution, just to be on the safe side - you never know what someone will enter
                        #if next letter position is out of range - the л is the last character
                        if (next_letter in "яєюіь" or next_letter in "яєюіь".upper() or
                            next_letter == letter and
                            next_letter not in whitespace and
                            next_letter not in special_characters and
                            i != len(file_contents)):
                            to_scrib = translation_board[letter][0]

                        else:
                            to_scrib = translation_board[letter][1]


                    case "ж"|"и"|"і"|"ї"|"х"|"ч"|"ш"|"щ":
                        to_liter = translation_board[letter][0]
                        to_scrib = translation_board[letter][1]


                    case "ь":
                        to_liter = translation_board[letter][0]

                        if next_letter == "о" or next_letter == "О":
                            to_scrib = translation_board[letter][1]

                        elif next_letter == "ц" or next_letter == "Ц":
                            to_scrib = translation_board[letter][2]

                        elif next_letter == "с" or next_letter == "С":
                            to_scrib = translation_board[letter][3]

                        elif next_letter == "з" or next_letter == "З":
                            to_scrib = translation_board[letter][4]

                        elif next_letter == "н" or next_letter == "Н":
                            to_scrib = translation_board[letter][5]

                        elif next_letter == "л" or next_letter == "Л":
                            to_scrib = ""

                        else:
                            to_scrib = translation_board[letter][0]


                    case "’":
                        to_liter = letter
                        to_scrib = ""

                if is_upper:
                    transliteration += to_liter.title()
                    transcribtion += to_scrib.title()

                else:
                    transliteration += to_liter
                    transcribtion += to_scrib

            
            elif letter in translation_board:
                if is_upper:
                    transliteration += translation_board[letter.lower()].upper()
                    transcribtion += translation_board[letter.lower()].upper()

                else:
                    transliteration += translation_board[letter]
                    transcribtion += translation_board[letter]


            else:
                if not proceed:
                    while input_decision == "":
                        print("This file contains non-ukrainian characters.",
                            "Transliteration and transcribtion will get rid of those characters.")
                        input_decision = input("Do you wish to proceed? (y/n): ")

                        if input_decision == "y" or input_decision == "Y":
                            break

                        elif input_decision == "n" or input_decision == "N":
                            return "A non-ukrainian character appeared"

                        else:
                            input_decision = ""
                
                else:
                    transliteration += " "
                    transcribtion += " "

    return f"Liter - {transliteration} \nScribe - {transcribtion}"

print(transliterate_transcribe())
