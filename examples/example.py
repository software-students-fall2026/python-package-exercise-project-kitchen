
"""
Example program demonstrating the functions in pyjokelang.

Run from the project root:
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
)


def scramble_example():
    """Demonstrate scrambling and unscrambling messages."""
    print("=== Scramble and unscramble ===")
    message = "Meet me at noon!"
    print(f"Original message:          {message}")

    scrambled = scramble(message)
    print(f"Scrambled (default key):   {scrambled}")
    print(f"Unscrambled:               {unscramble(scrambled)}")

    secret = scramble(message, key="tacos")
    print(f"Scrambled (key 'tacos'):   {secret}")
    print(f"Unscrambled with 'tacos':  {unscramble(secret, key='tacos')}")
    print(f"Unscrambled with 'pizza':  {unscramble(secret, key='pizza')}")
    print()


def pig_latin_example():
    """Demonstrate English to Pig Latin and back."""
    print("=== Pig Latin ===")
    message = "Hello world"

    translated = english_sentence_to_pig_latin(message)
    print(f"Original:    {message}")
    print(f"Pig Latin:   {translated}")
    print(f"English:     {pig_latin_sentence_to_english(translated)}")
    print()


def baby_talk_example():
    """Demonstrate all three Baby Talk intensity levels."""
    print("=== Baby Talk ===")
    message = "Hello world, please bring water"

    print(f"Original:     {message}")

    for intensity in range(3):
        print(f"Intensity {intensity}:  {baby_talk(message, intensity)}")

    print()


def random_caps_example():
    """Demonstrate random capitalization."""
    print("=== Random Capitalization ===")
    message = "Hello world!"

    print(f"Original:  {message}")
    print(f"Random:    {random_caps(message)}")
    print()


def cat_talk_example():
    """Demonstrate Cat Talk with default and custom sounds."""
    print("=== Cat Talk ===")
    message = "Hello world!"

    print(f"Original:       {message}")
    print(f"Default sounds: {cat_talk(message)}")
    print(f"Custom sounds:  {cat_talk(message, sounds=['meow'])}")
    print()


def main():
    """Run every example."""
    scramble_example()
    pig_latin_example()
    baby_talk_example()
    random_caps_example()
    cat_talk_example()


if __name__ == "__main__":
    main()
