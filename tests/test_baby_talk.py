"""Tests for the baby talk function"""

import pytest
from pyjokelang.baby_talk import baby_talk

LONG_PHRASE = (
        "Please bring the little rabbit some very cold water "
        "for my mother and father with three cherries"
    )

class TestBabyTalk:
    """Unit tests for Baby Talk"""
    # test intensity 0 - basic
    def test_level_0_letter_swaps(self):
        """intensity lvl 0 swaps single letters only"""
        assert baby_talk("rabbit", 0) == "wabbit"
        assert baby_talk("little", 0) == "wittwe"
        assert baby_talk("very", 0) == "bewy"
    # test intensity 0 - ignores keywords
    def test_level_0_ignores_keywords_and_double_letters(self):
        """intensity 0 does not use the keyword list or th/ch swaps"""
        assert baby_talk("mother", 0) == "mothew"
        assert baby_talk("water", 0)== "watew"
        assert baby_talk("this church", 0) == "this chuwch"
    # test intensity 1 - swaps keywords properly
    def test_level_1_keywords(self):
        """Tests basic keyword swap"""
        assert baby_talk("mother", 1) == "mama"
        assert baby_talk("water", 1)== "wawa"
        assert baby_talk("please", 1) == "pwease"
    # test intensity 1 - swaps keywords and level 0 swaps still made
    def test_level_1_non_keywords_still_get_lvl_0_swaps(self):
        """Words that aren't keywords still get single-letter swaps."""
        assert baby_talk("river", 1)== "wibew"
        assert baby_talk("hello river", 1) == "hewwo wibew"
        assert baby_talk("this", 1) == "this"
    # test intensity 2 - swaps th and ch properly
    def test_level_2_th_ch(self):
        """lvl 2 makes th -> d and ch -> t."""
        assert baby_talk("this", 2) == "dis"
        assert baby_talk("chair", 2) == "taiw"
        assert baby_talk("church", 2) == "tuwt"
        assert baby_talk("three", 2) == "dwee"
    # test intensity 2 - swaps th and ch but NOT in keywords
    # test that capitalization stays the same
    def test_keeps_caps(self):
        """caps stay capital after a swap."""
        assert baby_talk("Rabbit", 0) == "Wabbit"
        assert baby_talk("Hello", 1) == "Hewwo"
        assert baby_talk("This", 2) == "Dis"
        assert baby_talk("Church", 2) == "Tuwt"
    # test short phrase
    def test_multiple_words(self):
        """Each word in a phrase is converted."""
        assert baby_talk("Rabbit run", 0) == "Wabbit wun"
        assert baby_talk("Hello mother", 1) == "Hewwo mama"
        assert baby_talk("this church", 2) == "dis tuwt"
    # test LONG PHRASE at each intensity level
    def test_long_phrase_level_0(self):
        """lvl 0: letter swaps only, no keywords or th/ch."""
        expected = (
            "Pwease bwing the wittwe wabbit some bewy cowd watew "
            "fow my mothew and fathew with thwee chewwies"
        )
        assert baby_talk(LONG_PHRASE, 0) == expected
    def test_long_phrase_level_1(self):
        """lvl 1: keywords (please, water, mother, father) plus letter swaps."""
        expected = (
            "Pwease bwing the wittwe wabbit some bewy cowd wawa "
            "fow my mama and dada with thwee chewwies"
        )
        assert baby_talk(LONG_PHRASE, 1) == expected
    def test_long_phrase_level_2(self):
        """lvl 2: everything above plus th -> d and ch -> t."""
        expected = (
            "Pwease bwing de wittwe wabbit some bewy cowd wawa "
            "fow my mama and dada wid dwee tewwies"
        )
        assert baby_talk(LONG_PHRASE, 2) == expected
    def test_long_phrase_keeps_word_count(self):
        """Conversion never adds or drops words."""
        word_count = len(LONG_PHRASE.split())
        for level in (0, 1, 2):
            assert len(baby_talk(LONG_PHRASE, level).split()) == word_count
    # test invalid phrase inpput
    def test_invalid_phrase_type(self):
        """Non-string input phrases raise TypeError"""
        with pytest.raises(TypeError):
            baby_talk(123, 0)
        with pytest.raises(TypeError):
            baby_talk(None, 1)
        with pytest.raises(TypeError):
            baby_talk(["hello"], 2)
    def test_invalid_phrase_characters(self):
        """Input phrases with anything besides letters and spaces raise ValueError"""
        with pytest.raises(ValueError):
            baby_talk("hello!", 1)
        with pytest.raises(ValueError):
            baby_talk("room", 12)
        with pytest.raises(ValueError):
            baby_talk("hello, mother", 1)
        with pytest.raises(ValueError):
            baby_talk("café", 1)
    # test invalid intensity - should only be 0, 1, 2
    def test_invalid_intensity(self):
        """Intensity outside 0, 1, 2 raises ValueError"""
        with pytest.raises(ValueError):
            baby_talk("hello, 3")
        with pytest.raises(ValueError):
            baby_talk("hello", -1)
        with pytest.raises(ValueError):
            baby_talk("hello", 100)
    def test_invalid_intensity_type(self):
        """Non-integer intensity raises TypeError."""
        with pytest.raises(TypeError):
            baby_talk("hello", "high")
        with pytest.raises(TypeError):
            baby_talk("hello", 1.5)
        with pytest.raises(TypeError):
            baby_talk("hello", None)
        with pytest.raises(TypeError):
            baby_talk("hello", True)
    def test_default_intensity(self):
        """Intensity defaults to 1."""
        assert baby_talk("Hello river") == baby_talk("Hello river", 1)
        assert baby_talk("Hello mother") == "Hewwo mama"
        assert baby_talk("rabbit") == "wabbit"
    def test_whitespace_handling(self):
        """Extra spaces collapse to single spaces; blank input gives an empty string."""
        assert baby_talk("  rabbit   run  ", 0) == "wabbit wun"
        assert baby_talk("   ", 1) == ""
        assert baby_talk("rabbit\nrun", 0) == "wabbit wun"
    #if all-caps word is a keyword - default to 1st letter uppercase
    def test_all_caps(self):
        """Documents how all-uppercase words are handled."""
        assert baby_talk("RABBIT", 0) == "WABBIT"
        assert baby_talk("HELLO", 1) == "Hewwo"
