"""Ubbi Dubbi is a famous English language game and coded 'secret language' """

vowels = "aeiou"
vowels_with_y = "aeiouy"

def find_vowels(word):
    """Return a (start, end) pair for each run of consecutive vowels."""
    runs = []
    i = 0
    while i < len(word):
        if word[i].lower() in vowels:
            start = i
            while i < len(word) and word[i].lower() in vowels:
                i += 1
            runs.append((start, i))
        else:
            i += 1
    return runs