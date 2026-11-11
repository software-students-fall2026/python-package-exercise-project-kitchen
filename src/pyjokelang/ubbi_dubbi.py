"""Ubbi Dubbi is a famous English language game and coded 'secret language' """

vowels = "aeiou"
vowels_with_y = "aeiouy"

def find_vowels(word):
    """Return a (start, end) pair for each string of consecutive vowels."""
    vowel_string = []
    i = 0
    while i < len(word):
        if word[i].lower() in vowels:
            start = i
            while i < len(word) and word[i].lower() in vowels:
                i += 1
            vowel_string.append((start, i))
        else:
            i += 1
    return vowel_string

def insert_prefix(prefix, vowel_string, start, uppercase):
    """Put prefix before a string of consecutive vowels matching the case"""
    # can only insert prefix if start = False
    if uppercase:
        return prefix.upper() + vowel_string
    if start and vowel_string[0].isupper():
        return prefix.capitalize() + vowel_string.lower()
    return prefix.lower()+vowel_string

# now need actual function to use insert prefix and convert each word to ubbi dubbi
def convert_word(word, prefix):
    """Changes one word to Ubbi Dubbi"""







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
    return " ".join(_convert_word(word, prefix) for word in phrase.split())
