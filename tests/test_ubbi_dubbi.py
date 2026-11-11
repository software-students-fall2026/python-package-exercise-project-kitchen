"""Tests for the ubbi dubbi function"""


import pytest

from pyjokelang.ubbi_dubbi import ubbi_dubbi

LONG_PHRASE = (
    "Please bring the little rabbit some very cold water "
    "for my mother and father with three cherries"
)

class TestUbbiDubbi:
    """Unit tests for Ubbi Dubbi"""

    # basic tests - prefix goes before each group of vowels
    def test_basic_words(self):
        """prefix is added before each vowel group, default is ub"""
        assert ubbi_dubbi("hello") == "hubellubo"
        assert ubbi_dubbi("dog") == "dubog"
        assert ubbi_dubbi("banana") == "bubanubanuba"
        assert ubbi_dubbi("hello") == ubbi_dubbi("hello", prefix="ub")
        assert ubbi_dubbi("dog", "zz") == "dzzog"

    # consecutive vowel tests
    def test_consecutive_vowels(self):
        """a run of vowels gets a single prefix"""
        assert ubbi_dubbi("speak") == "spubeak"
        assert ubbi_dubbi("boat") == "buboat"
        assert ubbi_dubbi("beautiful") == "bubeautubifubul"

    # silent e tests
    def test_silent_e(self):
        """a final e doesn't get a prefix"""
        assert ubbi_dubbi("make") == "mubake"
        assert ubbi_dubbi("like") == "lubike"
        assert ubbi_dubbi("there") == "thubere"

    # silent e code doesn't replace all e's
    def test_silent_e_exceptions(self):
        """e keeps its prefix when it's the only vowel or part of a longer group"""
        assert ubbi_dubbi("me") == "mube"
        assert ubbi_dubbi("the") == "thube"
        assert ubbi_dubbi("agree") == "ubagrubee"
        assert ubbi_dubbi("helps") == "hubelps"

    # y as a vowel
    def test_y_as_a_vowel(self):
        """y treated as a vowel unless it's the first letter"""
        assert ubbi_dubbi("my") == "muby"
        assert ubbi_dubbi("happy") == "hubappuby"
        assert ubbi_dubbi("gym") == "gubym"
        assert ubbi_dubbi("sky") == "skuby"

    # y as a consonant when at start or after another vowel
    def test_y_as_consonant(self):
        """y at the start of a word and after another vowel is a consonant"""
        assert ubbi_dubbi("yes") == "yubes"
        assert ubbi_dubbi("yellow") == "yubellubow"
        assert ubbi_dubbi("play") == "plubay"
        assert ubbi_dubbi("beyond") == "bubeyubond"

    # capital letters stay in the front or match case
    def test_capitals(self):
        """capital letters stay at the front of the word or stay as typed"""
        assert ubbi_dubbi("Hello") == "Hubellubo"
        assert ubbi_dubbi("Apple") == "Ubapple"
        assert ubbi_dubbi("HELLO") == "HUBELLUBO"
        assert ubbi_dubbi("bEar") == "bubEar"

    # silent e with different capitalization
    def test_silent_e_with_caps(self):
        """a final e is skipped in capitalized and all-caps words too"""
        assert ubbi_dubbi("Make") == "Mubake"
        assert ubbi_dubbi("MAKE") == "MUBAKE"
        assert ubbi_dubbi("Eve") == "Ubeve"

    # testing capital letters with the letter y
    def test_capitals_with_y(self):
        """testing capital rules with words containing y"""
        assert ubbi_dubbi("My") == "Muby"
        assert ubbi_dubbi("MY") == "MUBY"
        assert ubbi_dubbi("Yes") == "Yubes"
        assert ubbi_dubbi("YES") == "YUBES"

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
        assert ubbi_dubbi("shh") == "shh"

    # single letters
    def test_single_letters(self):
        """one-letter words are handled"""
        assert ubbi_dubbi("a") == "uba"
        assert ubbi_dubbi("A") == "Uba"
        assert ubbi_dubbi("I") == "Ubi"

    # non-string phrase
    def test_invalid_phrase_type(self):
        """non-string phrases raise TypeError"""
        with pytest.raises(TypeError):
            ubbi_dubbi(123)
        with pytest.raises(TypeError):
            ubbi_dubbi(None)
        with pytest.raises(TypeError):
            ubbi_dubbi(["hello"])

    # bad characters in the phrase
    def test_invalid_phrase_characters(self):
        """anything besides letters and spaces raises ValueError"""
        with pytest.raises(ValueError):
            ubbi_dubbi("hello!")
        with pytest.raises(ValueError):
            ubbi_dubbi("ro-om")
        with pytest.raises(ValueError):
            ubbi_dubbi("café")
        with pytest.raises(ValueError):
            ubbi_dubbi("room 12")

    # non-string prefix
    def test_invalid_prefix_type(self):
        """non-string prefixes raise TypeError"""
        with pytest.raises(TypeError):
            ubbi_dubbi("hello", prefix=5)
        with pytest.raises(TypeError):
            ubbi_dubbi("hello", prefix=None)
        with pytest.raises(TypeError):
            ubbi_dubbi("hello", prefix=["ub"])

    # bad characters in the prefix
    def test_invalid_prefix_characters(self):
        """prefixes must be one or more plain letters"""
        with pytest.raises(ValueError):
            ubbi_dubbi("hello", prefix="")
        with pytest.raises(ValueError):
            ubbi_dubbi("hello", prefix="u2")
        with pytest.raises(ValueError):
            ubbi_dubbi("hello", prefix="u b")
        with pytest.raises(ValueError):
            ubbi_dubbi("hello", prefix="ü")

    # long phrase with a mix of word types
    def test_long_phrase(self):
        """every word in a long phrase is converted correctly"""
        expected = (
            "Plubease brubing thube lubittle rubabbubit subome vuberuby "
            "cubold wubatuber fubor muby mubothuber uband fubathuber "
            "wubith thrubee chuberrubies"
        )
        assert ubbi_dubbi(LONG_PHRASE) == expected

    def test_long_phrase_keeps_word_count(self):
        """conversion never adds or drops words"""
        word_count = len(LONG_PHRASE.split())
        assert len(ubbi_dubbi(LONG_PHRASE).split()) == word_count
        assert len(ubbi_dubbi(LONG_PHRASE, prefix="ob").split()) == word_count

    # long phrase with capitals and a custom prefix
    def test_long_phrase_with_caps_and_prefix(self):
        """capitals and a custom prefix work across several words"""
        assert ubbi_dubbi("Apple Pie And HELLO") == "Ubapple Pubie Uband HUBELLUBO"
        assert (
            ubbi_dubbi("Apple Pie And HELLO", prefix="ob")
            == "Obapple Pobie Oband HOBELLOBO"
        )
