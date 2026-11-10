
"""Tests for Cat Talk."""
import random

import pytest

from pyjokelang.cat_talk import CAT_SOUNDS, cat_talk


class TestCatTalk:
    """Unit tests for the cat_talk function."""

    def test_every_word_becomes_a_cat_sound(self):
        """Each word is replaced by one of the cat sounds."""
        result = cat_talk("the quick brown fox jumps")
        words = result.split()
        assert len(words) == 5
        assert all(word in CAT_SOUNDS for word in words)
        assert "quick" not in result

    def test_custom_sounds(self):
        """The sounds argument controls which sounds are used."""
        assert cat_talk("one two three", sounds=["meow"]) == "meow meow meow"
        assert cat_talk("hello", sounds=("purr",)) == "purr"
        result = cat_talk("a b c d e f g h", sounds=["mew", "nya"])
        assert set(result.split()) <= {"mew", "nya"}

    def test_punctuation_and_spacing_stay_the_same(self):
        """Punctuation, numbers, and spaces stay where they are."""
        assert cat_talk("Hello, world!", sounds=["meow"]) == "Meow, meow!"
        assert cat_talk("I have 3 cats?!", sounds=["purr"]) == "Purr purr 3 purr?!"
        assert cat_talk("  spaced   out  ", sounds=["hiss"]) == "  hiss   hiss  "

    def test_capitalization_matches(self):
        """Capitalized and all-caps words give capitalized and all-caps sounds."""
        assert cat_talk("Hello", sounds=["meow"]) == "Meow"
        assert cat_talk("HELLO", sounds=["meow"]) == "MEOW"
        assert cat_talk("I LOVE you", sounds=["meow"]) == "Meow MEOW meow"

    def test_word_count_stays_the_same(self):
        """Contractions and hyphenated words are counted the way the README describes."""
        assert cat_talk("don't stop", sounds=["meow"]) == "meow meow"
        assert cat_talk("well-known", sounds=["meow"]) == "meow-meow"
        sentence = "We were with them, and it was fun."
        assert len(cat_talk(sentence).split()) == len(sentence.split())

    def test_sounds_are_random(self):
        """Different random choices give different results for the same text."""
        random.seed(1)
        first = cat_talk("one two three four five six seven eight")
        random.seed(2)
        second = cat_talk("one two three four five six seven eight")
        assert first != second

    def test_edge_inputs(self):
        """Empty text and text with no words stay unchanged."""
        assert cat_talk("") == ""
        assert cat_talk("123 !?") == "123 !?"
        assert cat_talk("   ") == "   "

    def test_invalid_input(self):
        """Non-string text or an empty sounds list raises an error."""
        with pytest.raises(TypeError):
            cat_talk(123)
        with pytest.raises(TypeError):
            cat_talk(None)
        with pytest.raises(ValueError):
            cat_talk("hello", sounds=[])
