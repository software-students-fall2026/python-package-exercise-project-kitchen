"""Tests for the ubbi dubbi function"""

from pyjokelang.ubbi_dubbi import ubbi_dubbi

class TestUbbiDubbi:
    """Unit tests for Ubbi Dubbi"""

    # basic tests - prefix goes before each group of vowels
    def test_basic_words(self):
        """ub is added before each vowel group"""
        assert ubbi_dubbi("hello") == "hubellubo"
        assert ubbi_dubbi("dog") == "dubog"
        assert ubbi_dubbi("banana") == "bubanubanuba"

    # consecutive vowel tests
    def test_consecutive_vowels(self):
        """a run of vowels gets a single prefix"""
        assert ubbi_dubbi("speak") == "spubeak"
        assert ubbi_dubbi("boat") == "buboat"
        assert ubbi_dubbi("beautiful") == "bubeautubifubul"