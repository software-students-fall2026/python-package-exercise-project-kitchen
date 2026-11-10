"""Baby Talk - Turns normal english into how a baby speaks"""

# baby talk function turns regular words into baby talk by changing
# the letters to phonetically match how baby talk sounds

# Intensity Level 0: ONLY swaps letters, not full words
letter_swap = {"r":"w", "l":"w", "v":"b"}

#Intensity Level 1: swaps letters AND full words
keyword_swap = {
    "hello": "hewwo",
    "please": "pwease",
    "water": "wawa",
    "mother": "mama",
    "father": "dada"}

#Intensity Level 2: swaps letters AND full words AND "extreme" letters
double_letter_swap = {"th": "d", "ch": "t"}

def swap_char(char):
    """swap char helper function to reduce branches"""
    if char.lower() in letter_swap:
        if char.isupper():
            return letter_swap[char.lower()].upper()
        return letter_swap[char.lower()]
    return char

def swap_letters(word, intensity):
    """switches the necessary chars in English to baby talk"""
    # first checks if word is in keyword swap. if yes, we just return new word
    # and don't worry about swapping single or double letters
    return_phrase = ""
    if intensity>0:
        # we only want to swap words for intensity levels 1 and 2
        if word.lower() in keyword_swap:
            if word[0].isupper():
                return_phrase += keyword_swap[word.lower()].capitalize()
            else:
                return_phrase += keyword_swap[word.lower()]
            return return_phrase
    i=0 #char index for word

    while i < len(word):
        if intensity==2:
            # need to check if next two letters are either "th" or "ch"
            # only conduct this swap if we have intensity level 2
            letter_pair = word[i:i+2].lower()
            if letter_pair in double_letter_swap:
                if word[i].isupper():
                    return_phrase += double_letter_swap[letter_pair].capitalize()
                else:
                    return_phrase += double_letter_swap[letter_pair]
                i+=2
            else:
                return_phrase += swap_char(word[i])
                i+=1
        else:
            return_phrase += swap_char(word[i])
            i+=1
    return return_phrase

def baby_talk(normal_phrase, intensity=1):
    """Converts a normal phrase to baby talk"""
    # default intensity is 1!

    if not isinstance(normal_phrase, str):
        raise TypeError("normal_phrase must be a string")
    if not all(
        (char.isascii() and char.isalpha()) or char.isspace()
        for char in normal_phrase
    ):
        raise ValueError("normal_phrase may only contain letters and spaces")
    if not isinstance(intensity, int) or isinstance(intensity, bool):
        raise TypeError("intensity must be an integer")
    if intensity not in (0, 1, 2):
        raise ValueError("intensity must be 0, 1, or 2")
    # finished input validation above
    normal_words = normal_phrase.split()
    baby_phrase = []
    for word in normal_words:
        baby_phrase.append(swap_letters(word, intensity))
    return " ".join(baby_phrase)
