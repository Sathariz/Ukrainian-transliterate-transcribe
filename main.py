from pathlib import Path
from string import whitespace

special_characters = """1234567890`~!@#$%^&*()_+-=[]\;',./<>?:"{}|"""

def trancliterate_exceptions(prev, current, next, last_letter):

    consonant = "бгґджзклмнпрстфхцчшщ"

    if next.isupper():
        next = next.lower()

    if prev.isupper():
        prev = prev.lower()

    consonant_table = {
        "є" : ["ê", "je", "e", "ie"],
        "ж" : ["ž", "ż"],
        "и" : ["i", "y"],
        "і" : ["ì", "i"],
        "ї" : ["ї", "ji"],
        "л" : ["l", "ł"],
        "х" : ["h", "ch"],
        "ч" : ["č", "cz"],
        "ш" : ["š", "sz"],
        "щ" : ["ŝ", "szcz"],
        "ь" : ["′", "i", "ć", "ś", "ź", "ń"],
        "ю" : ["û", "ju", "u", "iu"],
        "я" : ["â", "ja", "a", "ia"]
    }

    match current:
        case "є"|"ю"|"я":
            if prev == "л":
                to_scrib = consonant_table[current][2]

            elif prev in consonant:
                to_scrib = consonant_table[current][3]

            else:
                to_scrib = consonant_table[current][1]


        # there are exceptions with words that have foreing origin
        # in such cases "ле" is written as "le"
        case "л":
            # precution, just to be on the safe side - you never know what someone will enter
            #if next letter position is out of range - the л is the last character
            if (next in "яєюіь" or
                next == current and
                next not in whitespace and
                next not in special_characters and
                last_letter):
                to_scrib = consonant_table[current][0]

            else:
                to_scrib = consonant_table[current][1]


        case "ж"|"и"|"і"|"ї"|"х"|"ч"|"ш"|"щ":
            to_scrib = consonant_table[current][1]


        case "ь":
            if next == "о":
                to_scrib = consonant_table[current][1]

            elif next == "ц":
                to_scrib = consonant_table[current][2]

            elif next == "с":
                to_scrib = consonant_table[current][3]

            elif next == "з":
                to_scrib = consonant_table[current][4]

            elif next == "н":
                to_scrib = consonant_table[current][5]

            elif next == "л":
                to_scrib = ""

            else:
                to_scrib = consonant_table[current][0]


    return (consonant_table[current][0], to_scrib)



def transliterate_transcribe():
    translation_board = {
        "а" : "a",
        "б" : "b",
        "в" : "w",
        "г" : "h",
        "ґ" : "g",
        "д" : "d",
        "е" : "e",
        "з" : "z",
        "й" : "j",
        "к" : "k",
        "м" : "m",
        "н" : "n",
        "о" : "o",
        "п" : "p",
        "р" : "r",
        "с" : "s",
        "т" : "t",
        "у" : "u",
        "ф" : "f",
        "ц" : "c",
    }

    ukrainian_file_path = Path("/home/user/Desktop/uk.txt")

    transliteration = ""
    transcribtion = ""
    to_liter = ""
    to_scrib = ""
    next_letter = ""
    is_last_letter = False
    input_decision = ""
    ukr_exceptions = "єжиіїлхчшщьюя"


    with open(ukrainian_file_path, "r", encoding="utf-8") as i_file:
        file_contents = i_file.read()


    for char in file_contents:
        if (char not in translation_board or
            char not in ukr_exceptions or
            char not in whitespace or
            char not in special_characters):
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

    for position, letter in enumerate(file_contents):
        letter = file_contents[position]
        prev_letter = file_contents[position-1]
        if position+1 < len(file_contents):
            next_letter = file_contents[position+1]
        else:
            next_letter = ""

        if position == len(file_contents):
            is_last_letter = True

        if letter.isupper():
            letter = letter.lower()
            is_upper = True
        else:
            is_upper = False


        if letter in whitespace or letter in special_characters:
            transcribtion += letter
            transliteration += letter
            continue

        if letter in ukr_exceptions:
            to_liter, to_scrib = trancliterate_exceptions(prev_letter, letter, next_letter, is_last_letter)

            if is_upper:
                transliteration += to_liter.title()
                transcribtion += to_scrib.title()

            else:
                transliteration += to_liter
                transcribtion += to_scrib

        
        elif letter in translation_board:
            if is_upper:
                transliteration += translation_board[letter].upper()
                transcribtion += translation_board[letter].upper()

            else:
                transliteration += translation_board[letter]
                transcribtion += translation_board[letter]


        # ’ is not in the translation_board nor consonant_table
        elif letter == "’":
            to_liter = letter
            to_scrib = ""

        # a non-ukrainian character
        else:
            transliteration += ""
            transcribtion += ""


    return f"Liter - {transliteration} \nScribe - {transcribtion}"

print(transliterate_transcribe())
