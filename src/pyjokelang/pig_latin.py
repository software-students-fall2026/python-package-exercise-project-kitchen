'''
English to pig latin:

Move the first letter to the end of the word and add -ay. 

Unless the first letter is a vowel, then keep the word unchanged and add -ay.

If the word ends in a vowel add -way instead.

Use a helper function to reverse capital and lowercase letters. 

Use a helper function to scramble punctuation.

Use a helper function to translate full sentences.

KNOWN ISSUE: For words with W, the pig latin to english doesn't work 

(ex hello world -> ellohay orldway -> hello orld). 

PROPOSED SOLUTION: Add dashes so we know where to split

'''

def english_word_to_pig_latin(text):
    """Translate a single English word into Pig Latin."""
    if not text:
        return ""
    vowels = "aeiou"
    word = text
    # if the first letter is a vowel, keep that here
    if word[0].lower() in vowels:
        pig_latin_word = word + "-way"
    # if it's not a vowel, then add the first letter to the end and add ay
    else:
        pig_latin_word = word[1:] + word[0] + "-ay"
    return pig_latin_word

def english_sentence_to_pig_latin(text):
    """Translate an entire English sentence into Pig Latin."""
    translated_words = []
    words = text.split()
    for word in words:
        translated_words.append(english_word_to_pig_latin(word))
    translated_sentence = reverse_punctuation(" ".join(translated_words))
    translated_sentence = reverse_capitalization(translated_sentence)
    return translated_sentence

def reverse_capitalization(text):
    """This will turn all capital letters into lowercase and vice versa."""
    reverse_capped_text = ""
    for letter in text:
        if letter.isupper():
            reverse_capped_text += letter.lower()
        elif letter.islower():
            reverse_capped_text += letter.upper()
        else:
            reverse_capped_text += letter
    return reverse_capped_text


def pig_latin_word_to_english(text):
    """Translate a single Pig Latin word back into English."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    word = text

    # if it ends in "-way", the word started with a vowel, so just remove the "-way"
    if word.lower().endswith("-way") and len(word) > 4:
        return word[:-4]
    # otherwise remove the "-ay" and move the last letter back to the front
    if word.lower().endswith("-ay") and len(word) > 3:
        stem = word[:-3]
        return stem[-1] + stem[:-1]
    # anything else isn't Pig Latin, so leave it unchanged
    return word


def pig_latin_sentence_to_english(text):
    """Translate a full Pig Latin sentence back into English."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    # undo the sentence translator's helpers first
    sentence = reverse_capitalization(text)
    sentence = restore_punctuation(sentence)
    translated_words = []
    words = sentence.split()
    for word in words:
        translated_words.append(pig_latin_word_to_english(word)) #call helper

    return " ".join(translated_words)

def reverse_punctuation(text):
    """This will turn ! into . and turn . into ? and ? to !."""
    reversed_punctuation_text = ""
    for character in text:
        if character == "!":
            reversed_punctuation_text += "."
        elif character == ".":
            reversed_punctuation_text += "?"
        elif character == "?":
            reversed_punctuation_text += "!"
        else:
            reversed_punctuation_text += character
    return reversed_punctuation_text


def restore_punctuation(text):
    """Undo reverse_punctuation(): turn . back into !, ? back into . and ! back into ?."""
    restored_punctuation_text = ""
    for character in text:
        if character == ".":
            restored_punctuation_text += "!"
        elif character == "?":
            restored_punctuation_text += "."
        elif character == "!":
            restored_punctuation_text += "?"
        else:
            restored_punctuation_text += character
    return restored_punctuation_text
