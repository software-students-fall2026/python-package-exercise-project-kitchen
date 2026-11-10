"""Tests for the baby talk function"""
from pyjokelang.baby_talk import baby_talk

# test intensity 0 - basic
def test_level_0_letter_swaps():
    """intensity lvl 0 swaps single letters only"""
    assert baby_talk("rabbit", 0).strip() == "wabbit"
    assert baby_talk("little", 0).strip() == "wittwe"
    assert baby_talk("very", 0).strip() == "bewy"
# test intensity 0 - ignores keywords
def test_level_0_ignores_keywords_and_double_letters():
    """intensity 0 does not use the keyword list or th/ch swaps"""
    assert baby_talk("mother", 0).strip() == "mothew"
    assert baby_talk("water", 0).strip() == "watew"
    assert baby_talk("this church", 0).strip() == "this chuwch"

# test intensity 0 - ignores complicated swaps

# test intensity 1 - swaps keywords properly
def test_level_1_keywords():
    """Tests basic keyword swap"""
    assert baby_talk("mother", 1).strip() == "mama"
    assert baby_talk("water", 1).strip() == "wawa"
    assert baby_talk("please", 1).strip() == "pwease"

# test intensity 1 - swaps keywords and level 0 swaps still made
def test_level_1_non_keywords_still_get_lvl_0_swaps():
    """Words that aren't keywords still get single-letter swaps."""
    assert baby_talk("river", 1).strip() == "wibew"
    assert baby_talk("hello river", 1).strip() == "hewwo wibew"
    assert baby_talk("this", 1).strip() == "this"

# test intensity 2 - swaps th and ch properly
def test_level_2_th_ch():
    """lvl 2 makes th -> d and ch -> t."""
    assert baby_talk("this", 2).strip() == "dis"
    assert baby_talk("chair", 2).strip() == "taiw"
    assert baby_talk("church", 2).strip() == "tuwt"
    assert baby_talk("three", 2).strip() == "dwee"

# test intensity 2 - swaps th and ch but NOT in keywords

# test that capitalization stays the same
def test_keeps_caps():
    """caps stay capital after a swap."""
    assert baby_talk("Rabbit", 0).strip() == "Wabbit"
    assert baby_talk("Hello", 1).strip() == "Hewwo"
    assert baby_talk("This", 2).strip() == "Dis"
    assert baby_talk("Church", 2).strip() == "Tuwt"

# test short phrase
def test_multiple_words():
    """Each word in a phrase is converted."""
    assert baby_talk("Rabbit run", 0).strip() == "Wabbit wun"
    assert baby_talk("Hello mother", 1).strip() == "Hewwo mama"
    assert baby_talk("this church", 2).strip() == "dis tuwt"


# test long phrase at each intensity level

LONG_PHRASE = (
    "Please bring the little rabbit some very cold water "
    "for my mother and father with three cherries"
)

def test_long_phrase_level_0():
    """lvl 0: letter swaps only, no keywords or th/ch."""
    expected = (
        "Pwease bwing the wittwe wabbit some bewy cowd watew "
        "fow my mothew and fathew with thwee chewwies"
    )
    assert baby_talk(LONG_PHRASE, 0).strip() == expected


def test_long_phrase_level_1():
    """lvl 1: keywords (please, water, mother, father) plus letter swaps."""
    expected = (
        "Pwease bwing the wittwe wabbit some bewy cowd wawa "
        "fow my mama and dada with thwee chewwies"
    )
    assert baby_talk(LONG_PHRASE, 1).strip() == expected


def test_long_phrase_level_2():
    """lvl 2: everything above plus th -> d and ch -> t."""
    expected = (
        "Pwease bwing de wittwe wabbit some bewy cowd wawa "
        "fow my mama and dada wid dwee tewwies"
    )
    assert baby_talk(LONG_PHRASE, 2).strip() == expected

def test_long_phrase_keeps_word_count():
    """Conversion never adds or drops words."""
    word_count = len(LONG_PHRASE.split())
    for level in (0, 1, 2):
        assert len(baby_talk(LONG_PHRASE, level).split()) == word_count


# test invalid phrase inpput
# test invalid intensity - should only be 0, 1, 2
