"""Cat Talk: Turns every word in a sentence into a random cat noise."""

CAT_SOUNDS = ("meow", "purr", "hiss", "mrrp", "mew", "nya", "prrr", "yowl", "mrow")

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
    raise NotImplementedError("cat_talk() hasn't been written yet")
