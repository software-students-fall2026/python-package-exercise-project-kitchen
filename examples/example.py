
"""
Example program that demonstrates the functions in pyjokelang.

Run it from the project root with:
    pipenv run python examples/example.py
"""

from pyjokelang import (
    scramble,
    unscramble,
    baby_talk,
    random_caps,
    cat_talk,
    english_sentence_to_pig_latin,
    pig_latin_sentence_to_english,
    ubbi_dubbi
)


def scramble_example():
    """Show scramble() and unscramble(), with the default key and a secret key."""
    print("=== Scramble and Unscramble ===")
    message = "Meet me at noon!"
    print(f"Original message:          {message}")

    # With the default key, anyone with pyjokelang can unscramble it
    scrambled = scramble(message)
    print(f"Scrambled (default key):   {scrambled}")
    print(f"Unscrambled:               {unscramble(scrambled)}")

    # With a secret key, only someone who knows the key can unscramble it
    secret = scramble(message, key="tacos")
    print(f"Scrambled (key 'tacos'):   {secret}")
    print(f"Unscrambled with 'tacos':  {unscramble(secret, key='tacos')}")
    print(f"Unscrambled with 'pizza':  {unscramble(secret, key='pizza')}")
    print()


def pig_latin_example():
    """Show English to Pig Latin translation and back."""
    print("=== Pig Latin ===")

    # Translate a full sentence
    message = "Hello world"
    translated = english_sentence_to_pig_latin(message)

    print(f"Original:    {message}")
    print(f"Pig Latin:   {translated}")
    print(f"English:     {pig_latin_sentence_to_english(translated)}")
    print()

    # Demonstrate words starting with vowels
    message = "Apple"
    translated = english_sentence_to_pig_latin(message)

    print(f"Original:    {message}")
    print(f"Pig Latin:   {translated}")
    print(f"English:     {pig_latin_sentence_to_english(translated)}")
    print()

    # Demonstrate punctuation changes
    message = "Hello!"
    translated = english_sentence_to_pig_latin(message)

    print(f"Original:    {message}")
    print(f"Pig Latin:   {translated}")
    print(f"English:     {pig_latin_sentence_to_english(translated)}")
    print()


def baby_talk_example():
    """Show Baby Talk at all three intensity levels."""
    print("=== Baby Talk ===")
    message = "Hello world please bring water"

    print(f"Original:     {message}")

    # Default intensity is 1
    print(f"Default:      {baby_talk(message)}")

    # Demonstrate each intensity level
    for intensity in range(3):
        translated = baby_talk(message, intensity)
        print(f"Intensity {intensity}:  {translated}")

    print()


def random_caps_example():
    """Show random capitalization."""
    print("=== Random Capitalization ===")
    message = "Hello world!"

    print(f"Original:  {message}")

    # Each call may produce a different result
    print(f"Random 1:  {random_caps(message)}")
    print(f"Random 2:  {random_caps(message)}")
    print()


def cat_talk_example():
    """Show Cat Talk with default and custom sounds."""
    print("=== Cat Talk ===")
    message = "Hello world!"

    print(f"Original:       {message}")

    # Randomly choose from the default cat sounds
    print(f"Default sounds: {cat_talk(message)}")

    # Use a custom list of cat sounds
    print(f"Custom sounds:  {cat_talk(message, sounds=['meow'])}")

    # Demonstrate capitalization and punctuation
    message = "I LOVE my cat."
    print(f"Original:       {message}")
    print(f"Cat Talk:       {cat_talk(message)}")
    print()

def ubbi_dubbi_example():
    """Show Ubbi Dubbi with the default and a custom prefix."""
    print("=== Ubbi Dubbi ===")
    message = "Hello world"

    print(f"Original:       {message}")
    print(f"Default prefix: {ubbi_dubbi(message)}")
    print(f"Prefix 'ob':    {ubbi_dubbi(message, prefix='ob')}")

    # Silent e, the letter y, and capitalization
    message = "Make my Apple"
    print(f"Original:       {message}")
    print(f"Ubbi Dubbi:     {ubbi_dubbi(message)}")
    print()

def main():
    """Run every example."""
    scramble_example()
    pig_latin_example()
    baby_talk_example()
    random_caps_example()
    cat_talk_example()
    ubbi_dubbi_example()

if __name__ == "__main__":
    main()
