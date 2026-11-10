"""Cat Talk: Turns every word in a sentence into a random cat noise."""
import random
import re

CAT_SOUNDS = ("meow", "purr", "hiss", "mrrp", "mew", "nya", "prrr", "yowl", "mrow")

# a word is a run of letters, and can include apostrophes inside it (like "don't")
WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)*")


def _match_capitals(word, sound):
    """Give the cat sound the same capitalization style as the word it replaces."""
    if word.isupper() and len(word) > 1:
        return sound.upper()
    if word[0].isupper():
        return sound.capitalize()
    return sound


def cat_talk(text, sounds=CAT_SOUNDS):
    """Replace every word in text with a random cat sound.

    Spaces, numbers, and punctuation preserved, so the result has the
    same number of words. Capitalized words become capitalized sounds, and
    all-caps words become all-caps sounds. This is one way only since
    there is no way to recover (since its randomized)

    Args:
        text: The English text to translate.
        sounds: The cat sounds to choose from. Defaults to CAT_SOUNDS.

    Raises:
        TypeError: If text is not a string.
        ValueError: If sounds is empty.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not sounds:
        raise ValueError("sounds must contain at least one cat sound")

    return WORD_PATTERN.sub(
        lambda match: _match_capitals(match.group(0), random.choice(sounds)),
        text,
    )
