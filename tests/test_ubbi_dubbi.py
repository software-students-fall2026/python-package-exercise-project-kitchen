"""Tests for the ubbi dubbi function"""
import pytest

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

    # capital letters stay in the front or match case
    def test_capitals(self):
        """capital letters stay at the front of the word or stay as typed"""
        assert ubbi_dubbi("Hello") == "Hubellubo"
        assert ubbi_dubbi("Apple") == "Ubapple"
        assert ubbi_dubbi("HELLO") == "HUBELLUBO"
        assert ubbi_dubbi("bEar") == "bubEar"

    # prefix changes to something other than "ub"
    def test_custom_prefix(self):
        """other prefixes work and match the capitalization"""
        assert ubbi_dubbi("hello", prefix="ob") == "hobellobo"
        assert ubbi_dubbi("hello", prefix="ib") == "hibellibo"
        assert ubbi_dubbi("Apple", prefix="ob") == "Obapple"
        assert ubbi_dubbi("HELLO", prefix="ob") == "HOBELLOBO"
        assert ubbi_dubbi("hello", prefix="UB") == "hubellubo"

    # multiple words and extra whitespace
    def test_phrases_and_whitespace(self):
        """each word is converted and spaces collapse"""
        assert ubbi_dubbi("Hello apple make me") == "Hubellubo ubapple mubake mube"
        assert ubbi_dubbi("  hello   dog  ") == "hubellubo dubog"
        assert ubbi_dubbi("hello\ndog") == "hubellubo dubog"

    # nothing to convert
    def test_empty_and_no_vowels(self):
        """empty text and words without vowels are unchanged"""
        assert ubbi_dubbi("") == ""
        assert ubbi_dubbi("   ") == ""
        assert ubbi_dubbi("gym") == "gym"
        assert ubbi_dubbi("shh") == "shh"

    # single letters
    def test_single_letters(self):
        """one-letter words are handled"""
        assert ubbi_dubbi("a") == "uba"
        assert ubbi_dubbi("A") == "Uba"
        assert ubbi_dubbi("I") == "Ubi"