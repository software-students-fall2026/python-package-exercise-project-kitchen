"""Ubbi Dubbi is a famous English language game and coded 'secret language' """

VOWELS = "aeiou"

def is_vowel(word, i):
    """True if the letter at position i acts as a vowel (y only sometimes)."""
    char = word[i].lower()
    if char in VOWELS:
        return True
    return char == "y" and i > 0 and word[i - 1].lower() not in VOWELS

def find_vowels(word):
    """Return a (start, end) pair for each string of consecutive vowels."""
    vowel_string = []
    i = 0
    while i < len(word):
        if is_vowel(word, i):
            start = i
            while i < len(word) and is_vowel(word, i):
                i += 1
            vowel_string.append((start, i))
        else:
            i += 1
    return vowel_string

def insert_prefix(prefix, vowel_string, start, uppercase):
    """Put prefix before a string of consecutive vowels matching the case"""
    if uppercase:
        return prefix.upper() + vowel_string
    # capital start moves prefix to front and capitalizes
    if start and vowel_string[0].isupper():
        return prefix.capitalize() + vowel_string.lower()
    return prefix.lower()+vowel_string

def convert_word(word, prefix):
    """Changes one word to Ubbi Dubbi"""
    vstr = find_vowels(word) # returns array of consecutive vowels
    prev_end=0
    uppercase = word.isupper() and len(word) > 1
    ui_phrase = []
    for index, (start, end) in enumerate(vstr):
        split_word = word[start:end]
        silent_e = (
            len(vstr) > 1 # prevents words with only one vowel being classified as silent_e
            # then make sure last letter is e
            and index == len(vstr) - 1
            and end == len(word)
            and split_word.lower() == "e"
        )
        ui_phrase.append(word[prev_end:start])
        if silent_e:
            ui_phrase.append(split_word)
        else:
            ui_phrase.append(insert_prefix(prefix, split_word, start == 0, uppercase))
        prev_end = end
    ui_phrase.append(word[prev_end:])
    return "".join(ui_phrase)

def ubbi_dubbi(phrase, prefix="ub"):
    # can alter the prefix for variations of ubbi dubbi, but "ub" is standard
    """Convert a phrase to Ubbi Dubbi by adding a prefix before vowel sounds."""
    if not isinstance(phrase, str):
        raise TypeError("phrase must be a string")
    if not all(
        (char.isascii() and char.isalpha()) or char.isspace()
        for char in phrase
    ):
        raise ValueError("phrase may only contain letters and spaces")
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a string")
    if not (prefix.isascii() and prefix.isalpha()):
        raise ValueError("prefix must be one or more letters")
    return " ".join(convert_word(word, prefix) for word in phrase.split())
