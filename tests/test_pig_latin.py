"""Tests for the english to pig latin."""


import pytest

from pyjokelang.pig_latin import (
    english_word_to_pig_latin,
    english_sentence_to_pig_latin,
    pig_latin_word_to_english,
    pig_latin_sentence_to_english,
    restore_punctuation,
)

class TestPigLatin:
    """Unit tests for English to Pig Latin functions."""

    def test_word_consonants(self):
        """Test words beginning with consonants."""
        assert english_word_to_pig_latin("hello") == "elloh-ay"
        assert english_word_to_pig_latin("goodbye") == "oodbyeg-ay"
        assert english_word_to_pig_latin("software") == "oftwares-ay"

    def test_word_vowels(self):
        """Test words beginning with vowels."""
        assert english_word_to_pig_latin("apple") == "apple-way"
        assert english_word_to_pig_latin("orange") == "orange-way"
        assert english_word_to_pig_latin("ocean") == "ocean-way"

    def test_single_letter(self):
        """Test words containing one letter."""
        assert english_word_to_pig_latin("m") == "m-ay"
        assert english_word_to_pig_latin("b") == "b-ay"
        assert english_word_to_pig_latin("i") == "i-way"

    def test_sentence_known_output(self):
        """Test translating full sentences."""
        assert english_sentence_to_pig_latin("hello world") == "ELLOH-AY ORLDW-AY"
        assert english_sentence_to_pig_latin("i love software") == "I-WAY OVEL-AY OFTWARES-AY"
        assert english_sentence_to_pig_latin("we are the best") == "EW-AY ARE-WAY HET-AY ESTB-AY"

    def test_sentence_capitalization(self):
        """Test lowercase, uppercase, and mixed-case sentences."""
        assert english_sentence_to_pig_latin("hello world") == "ELLOH-AY ORLDW-AY"
        assert english_sentence_to_pig_latin("I LOVE SOFTWARE") == "i-WAY ovel-AY oftwares-AY"
        assert english_sentence_to_pig_latin("We Are The Best") == "Ew-AY aRE-WAY HEt-AY ESTb-AY"

    def test_sentence_whitespace(self):
        """Test empty sentences and extra spaces."""
        assert english_sentence_to_pig_latin("") == ""
        assert english_sentence_to_pig_latin("   ") == ""
        assert english_sentence_to_pig_latin("hello   world") == "ELLOH-AY ORLDW-AY"

    def test_word_invalid_input(self):
        """Invalid word types and empty words raise errors."""
        with pytest.raises(TypeError):
            english_word_to_pig_latin(123)
        with pytest.raises(TypeError):
            english_word_to_pig_latin(None)
        with pytest.raises(TypeError):
            english_word_to_pig_latin(["hello"])
        with pytest.raises(ValueError):
            english_word_to_pig_latin("")


    def test_sentence_invalid_input(self):
        """Invalid sentence types raise errors."""
        with pytest.raises(TypeError):
            english_sentence_to_pig_latin(123)
        with pytest.raises(TypeError):
            english_sentence_to_pig_latin(None)
        with pytest.raises(TypeError):
            english_sentence_to_pig_latin(["hello", "world"])

class TestPigLatinToEnglish:
    """Unit tests for Pig Latin to English functions."""

    def test_word_consonants(self):
        """Test words that started with a consonant."""
        assert pig_latin_word_to_english("elloh-ay") == "hello"
        assert pig_latin_word_to_english("ithw-ay") == "with"
        assert pig_latin_word_to_english("oftwares-ay") == "software"

    def test_word_vowels(self):
        """Test words that started with a vowel."""
        assert pig_latin_word_to_english("apple-way") == "apple"
        assert pig_latin_word_to_english("orange-way") == "orange"
        assert pig_latin_word_to_english("i-way") == "i"

    def test_word_keeps_capitalization(self):
        """Test that capital letters move back with their letter."""
        assert pig_latin_word_to_english("elloH-ay") == "Hello"
        assert pig_latin_word_to_english("Apple-way") == "Apple"
        assert pig_latin_word_to_english("ELLOH-AY") == "HELLO"

    def test_word_not_pig_latin(self):
        """Test that words without a Pig Latin ending are left unchanged."""
        assert pig_latin_word_to_english("hello") == "hello"
        assert pig_latin_word_to_english("-ay") == "-ay"
        assert pig_latin_word_to_english("") == ""

    def test_sentence_known_output(self):
        """Test translating full sentences made by the sentence translator."""
        assert pig_latin_sentence_to_english("ELLOH-AY ORLDW-AY") == "hello world"
        assert pig_latin_sentence_to_english("i-WAY ovel-AY oftwares-AY") == "I LOVE SOFTWARE"
        assert pig_latin_sentence_to_english("Ew-AY aRE-WAY HEt-AY ESTb-AY") == "We Are The Best"

    def test_sentence_punctuation(self):
        """Test that punctuation changed by the sentence translator is restored."""
        assert pig_latin_sentence_to_english("ELLOh-AY ORLD.w-AY") == "Hello World!"
        assert pig_latin_sentence_to_english("OWh-AY aRE-WAY OU!y-AY") == "How Are You?"
        assert pig_latin_sentence_to_english("I-WAY ON'TD-AY NOW?K-AY") == "i don't know."

    def test_sentence_whitespace(self):
        """Test empty sentences and extra spaces."""
        assert pig_latin_sentence_to_english("") == ""
        assert pig_latin_sentence_to_english("   ") == ""
        assert pig_latin_sentence_to_english("ELLOH-AY   ORLDW-AY") == "hello world"

    def test_restore_punctuation(self):
        """Test that restore_punctuation() undoes reverse_punctuation()."""
        assert restore_punctuation(".") == "!"
        assert restore_punctuation("?") == "."
        assert restore_punctuation("!") == "?"
        assert restore_punctuation("no change, here") == "no change, here"

    @pytest.mark.parametrize(
        "sentence",
        [
            "hello world",
            "Hello World!",
            "We were with them.",
            "How are you?",
            "I LOVE SOFTWARE",
            "Don't stop, keep going!",
            "",
        ],
    )
    def test_round_trip(self, sentence):
        """Test that translating to Pig Latin and back gives the original sentence."""
        assert pig_latin_sentence_to_english(english_sentence_to_pig_latin(sentence)) == sentence

    def test_word_round_trip(self):
        """Test that the word translators undo each other."""
        for word in ["hello", "Apple", "with", "WAY", "i", "b"]:
            assert pig_latin_word_to_english(english_word_to_pig_latin(word)) == word

    def test_invalid_input(self):
        """Test that non-string input raises a TypeError."""
        with pytest.raises(TypeError):
            pig_latin_word_to_english(123)
        with pytest.raises(TypeError):
            pig_latin_sentence_to_english(None)
        with pytest.raises(TypeError):
            pig_latin_sentence_to_english(["hello"])
