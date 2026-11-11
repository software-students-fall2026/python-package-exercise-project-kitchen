# pyjokelang

[![Build and test](https://github.com/software-students-fall2026/python-package-exercise-project-kitchen/actions/workflows/build.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-project-kitchen/actions/workflows/build.yml)

pyjokelang is a Python package that turns regular text into silly languages like Pig Latin, Baby Talk, Ubbi Dubbi, and Cat Talk. It also includes functions for scrambling and unscrambling messages and randomly changing capitalization. The package is meant to be a fun way to play around with text using Python.

## PyPI Package Page
[Link to package page](https://pypi.org/project/pyjokelang/0.1.0/)

## Installation

pyjokelang needs Python 3.14 or newer. From your own project's directory, install it into a [pipenv](https://packaging.python.org/en/latest/tutorials/managing-dependencies/#managing-dependencies) virtual environment:

```bash
pipenv install pyjokelang
```

Or install it with pip:

```bash
pip install pyjokelang
```

## Usage

Import the functions you want into your own code:

```python
from pyjokelang import (
    baby_talk,
    cat_talk,
    english_sentence_to_pig_latin,
    pig_latin_sentence_to_english,
    random_caps,
    scramble,
    unscramble,
)
```

Each function is documented in its own section below. For a complete program that uses every function, see [`examples/example.py`](./examples/example.py).

## Command line

Installing pyjokelang also adds a `pyjokelang` command:

```bash
pyjokelang <command> TEXT
```

| Command | What it does |
|---|---|
| `to-pig-latin` | English → Pig Latin |
| `from-pig-latin` | Pig Latin → English |
| `baby-talk` | English → Baby Talk (`--intensity 0`, `1` or `2`) |
| `scramble` | Text → gibberish (optional `--key`) |
| `unscramble` | Gibberish → text (use the same `--key`) |
| `random-caps` | Randomly capitalize each letter |
| `cat-talk` | Replace every word with a cat sound |

Run `pyjokelang --help` to list the commands, or `pyjokelang <command> --help` to see a command's options.

If the `pyjokelang` command isn't found (for example on Windows, where pip's scripts folder may not be on your PATH), use `python -m pyjokelang` instead. It works exactly the same way.


## Pig Latin Rules
 
> Confirm with Jade in order to ensure our methods match each other and follow the same rules
 
`to_pig_latin` and `from_pig_latin` follow these rules, so any text translated into Pig Latin can be translated back.
 
### Translating English to Pig Latin
 
The vowels are a, e, i, o and u. **Y never counts as a vowel.**
 
1. **Words starting with a consonant:** Move the first letter to the end of the word and add -ay.
2. **Words starting with a vowel:** Keep the word unchanged and add -way.
3. **Capitals:** The word translator preserves the original capitalization of letters, while the sentence translator reverses uppercase and lowercase letters using the reverse_capitalization() helper.
4. **Punctuation:** The sentence translator uses reverse_punctuation() to change ! to ., . to ?, and ? to !. Other characters remain unchanged.
5. **Full Sentences:** Split the sentence into individual words, translate each word into Pig Latin, join the translated words with spaces, and apply the capitalization and punctuation helpers.
6. **Whitespace:** Multiple spaces between words are reduced to single spaces. Empty sentences return an empty string.


### Translating Pig Latin back to English
 
**Finding translated words:** a translated word has letters containing at least one vowel, then a dash, then any moved letters, then `ay`. Anything else stays unchanged.
 
For each translated word:
 
1. **Remove only the final `ay`** (or `AY`) after the dash. Any "ay" before the dash belongs to the word, so `ay-way` becomes `way`.
2. **Move the letters back:** put the letters between the dash and the final `ay` in front of the letters before the dash, and remove the dash. If there are no letters between them, the word started with a vowel, so just remove `-ay`.
3. **Restore the capitalization** using the first matching rule:
   - **All caps:** if the whole word is in capitals, keep the whole result in capitals.
   - **Capitalized:** if only the first letter is a capital, make that letter lowercase and capitalize the new first letter of the word. If "qu" moved back, only the `q` becomes a capital.
   - **Lowercase:** keep the whole result in lowercase.
   
| Pig Latin | English | What happens |
|---|---|---|
| ing-stray | string | `str` moves back in front of `ing` |
| es-yay | yes | a moved `y` goes back to the front like any consonant |
| apple-ay | apple | no moved letters, so only `-ay` is removed |
| ay-way | way | only the final `ay` is removed |
| Ello-hay | Hello | `E` becomes lowercase and `h` becomes a capital |
| ELLO-HAY | HELLO | everything stays in capitals |
| Apple-ay | Apple | the first letter doesn't change, so it stays a capital |
| I-ay | I | a single-letter word keeps its capital |
| Iet-quay | Quiet | `I` becomes lowercase and only `q` becomes a capital |

## Scramble and Unscramble

`scramble` turns any text into unreadable gibberish, and `unscramble` turns it back. Share the scrambled text with a friend, and they can unscramble it on their own machine. Add a secret `key` and only someone who knows the key can read it.

```python
from pyjokelang import scramble, unscramble

scramble("Hello world, meet me at noon!")
# 'Rvb g u!mn bt,oi mt sxeawlwvb'

unscramble("Rvb g u!mn bt,oi mt sxeawlwvb")
# 'Hello world, meet me at noon!'

secret = scramble("Meet me at noon!", key="tacos")
# 'F agehe vbh!gx n'

unscramble(secret, key="tacos")
# 'Meet me at noon!'

unscramble(secret, key="pizza")   # wrong key, still gibberish
# 'Qwhi ei sw cgsf!'
```

### `scramble(text, key="kitchen")`

Scrambles `text` and returns the result. The output is always the same length as the input, and the same text and key always give the same output.

| Argument | Description |
|---|---|
| `text` | The message to scramble. |
| `key` | Optional secret word. Only its letters are used, and it isn't case-sensitive, so `"Tacos!"` works the same as `"tacos"`. Defaults to `"kitchen"`. |

### `unscramble(text, key="kitchen")`

Turns text made by `scramble` back into the original message. Use the same `key` that was used to scramble it; a different key gives gibberish.

| Argument | Description |
|---|---|
| `text` | The scrambled message. |
| `key` | The key used to scramble the message. Defaults to `"kitchen"`. |

### Errors

Both functions raise:

- `TypeError` if `text` or `key` isn't a string
- `ValueError` if `key` has no letters, for example `""` or `"123"`

### How it works

Scrambling happens in two steps:

1. **Shift the letters.** Each letter moves forward through the alphabet by the matching letter of the key (a = 0, b = 1, …, z = 25), repeating the key as needed. This is a [Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher). Capital letters stay capital, and everything else is left as it is.
2. **Rearrange every character.** Characters are written in a zigzag across 3 rows and read off row by row. This is a [rail fence cipher](https://en.wikipedia.org/wiki/Rail_fence_cipher), and it hides where the spaces and punctuation were.

`unscramble` undoes the two steps in reverse order.

### From the command line

```bash
pyjokelang scramble 'Meet me at noon!' --key tacos
pyjokelang unscramble 'F agehe vbh!gx n' --key tacos
```



## Baby Talk

`baby_talk` converts normal English text into baby talk by replacing letters and common words to imitate how a baby might speak. The function supports three intensity levels, allowing users to choose how much their text is transformed.

### Baby Talk Rules

The function applies different transformations depending on the selected intensity level.

1. **Intensity 0 (Basic):** Replaces individual letters:
   - `r` → `w`
   - `l` → `w`
   - `v` → `b`
2. **Intensity 1 (Intermediate):** Applies all basic letter replacements and replaces certain full words with baby talk equivalents.
3. **Intensity 2 (Extreme):** Applies all previous transformations and additionally replaces letter combinations:
   - `th` → `d`
   - `ch` → `t`
4. **Capitalization:** Letter replacements preserve the original capitalization. Full-word replacements capitalize the first letter if the original word starts with a capital.
5. **Whitespace:** Multiple spaces between words are reduced to single spaces. No leading or trailing whitespace is included in the output. Empty strings return an empty string.
6. **Punctuation:** Punctuation is preserved during letter replacements. However, full-word replacements only occur when the word matches a keyword exactly, without punctuation.

### Full-Word Replacements

At intensity levels 1 and 2, the following words are replaced before individual letters are processed.

| **English** | **Baby Talk** |
| ----------- | ------------- |
| hello | hewwo |
| please | pwease |
| water | wawa |
| mother | mama |
| father | dada |

### Examples

```python
from pyjokelang import baby_talk

baby_talk("Hello world", 0)
# 'Hewwo wowwd'

baby_talk("Hello world", 1)
# 'Hewwo wowwd'

baby_talk("Water please", 1)
# 'Wawa pwease'

baby_talk("The children love chocolate", 2)
# 'De tiwdwen wobe tocowate'

baby_talk("Mother and father", 2)
# 'Mama and dada'

baby_talk("Hello   world", 0)
# 'Hewwo wowwd'

baby_talk("", 0)
# ''
```

### `baby_talk(normal_phrase, intensity)`

Converts `normal_phrase` into baby talk using the specified intensity level and returns the modified string.

| **Argument** | **Description** |
| ------------ | --------------- |
| `normal_phrase` | The English text to convert into baby talk. |
| `intensity` | The transformation level: `0` for basic letter swaps, `1` for letter and full-word swaps, or `2` for extreme transformations. |

### How It Works

1. **Split the phrase.** The input text is split into individual words.
2. **Check for keywords.** At intensity levels 1 and 2, each word is checked against a dictionary of predefined baby talk replacements. If a match is found, the entire word is replaced without further letter substitutions.
3. **Replace individual letters.** Words that do not match a keyword have their letters replaced according to the selected intensity level.
4. **Apply extreme transformations.** At intensity level 2, two-letter combinations (`th` and `ch`) are checked before individual letters to ensure the correct replacements.
5. **Reconstruct the phrase.** The translated words are joined with single spaces, without leading or trailing whitespace, and the resulting phrase is returned.

### From the Command Line

```bash
pyjokelang baby-talk "Hello world" --intensity 0
# Hewwo wowwd

pyjokelang baby-talk "Water please" --intensity 1
# Wawa pwease

pyjokelang baby-talk "The children love chocolate" --intensity 2
# De tiwdwen wobe tocowate
```

## Random Capitalization

`random_caps` randomly changes the capitalization of letters in a string, creating text with a mix of uppercase and lowercase letters.

### Random Capitalization Rules

The function goes through each character in the input text and applies the following rules:

1. **Letters:** Each letter is randomly converted to either uppercase or lowercase.
2. **Non-alphabetic characters:** Spaces, numbers, and punctuation remain unchanged.
3. **Original capitalization:** The original capitalization is ignored, and each letter has an equal chance of being uppercase or lowercase.
4. **Randomness:** Running the function multiple times on the same text may produce different results.
5. **Empty strings:** An empty string returns an empty string.

### Examples

```python
from pyjokelang import random_caps

random_caps("Hello world!")
# 'hELLo WoRLd!'

random_caps("Hello world!")
# 'HeLlO wOrLD!'

random_caps("Python is fun")
# 'pYtHoN Is FuN'

random_caps("123! @#$")
# '123! @#$'

random_caps("")
# ''
```

Note: The outputs above are examples. Actual capitalization varies randomly each time the function is called.

### `random_caps(text)`

Randomly changes the capitalization of each letter in `text` and returns the modified string.

| **Argument** | **Description** |
| ------------ | --------------- |
| `text` | The string whose letters will be randomly capitalized. |

### How It Works

1. **Validate the input.** Check that `text` is a string. If not, raise a `TypeError`.
2. **Check each character.** Iterate through every character in the input string.
3. **Randomize capitalization.** For alphabetic characters, randomly choose between the lowercase and uppercase versions using `random.choice()`.
4. **Preserve other characters.** Leave spaces, numbers, and punctuation unchanged.
5. **Reconstruct the string.** Join all processed characters together and return the result.

### Errors

The function raises:

- `TypeError` if `text` is not a string.

### Limitations

`random_caps` is not reversible because it does not preserve the original capitalization. Running the function again will generate another random capitalization pattern rather than restoring the original text.


### From the Command Line

```bash
pyjokelang random-caps "Hello world!"
# hELLo WoRLd!

pyjokelang random-caps "Python is fun"
# pYtHoN Is FuN
```

The output varies each time because capitalization is randomized.


## Cat Talk
 
`cat_talk` turns every word in a sentence into a random cat sound, while keeping the sentence's spacing, numbers and punctuation.
 
### Cat Talk Rules
 
The function finds each word in the input text and applies the following rules:
 
1. **Words:** Each word is replaced with a random cat sound. The default sounds are `meow`, `purr`, `hiss`, `mrrp`, `mew`, `nya`, `prrr`, `yowl` and `mrow`.
2. **Word count:** The result always has the same number of words as the input. A contraction like `don't` counts as one word, and each part of a hyphenated word like `well-known` counts as its own word.
3. **Capitalization:** A capitalized word becomes a capitalized sound, and an all-caps word becomes an all-caps sound. A single capital letter, like `I`, becomes a capitalized sound.
4. **Non-alphabetic characters:** Spaces, numbers, and punctuation remain unchanged.
5. **Randomness:** Running the function multiple times on the same text may produce different results.
6. **Empty strings:** An empty string returns an empty string.
### Examples
 
```python
from pyjokelang import cat_talk
 
cat_talk("Hello world!")
# 'Mrrp mrow!'
 
cat_talk("Hello world!")
# 'Mew nya!'
 
cat_talk("I LOVE my cat.")
# 'Nya HISS prrr meow.'
 
cat_talk("Don't stop, keep going!")
# 'Yowl mrow, yowl yowl!'
 
cat_talk("I have 3 cats?!", sounds=["meow"])
# 'Meow meow 3 meow?!'
 
cat_talk("Feed me now", sounds=("purr", "hiss"))
# 'Purr purr hiss'
 
cat_talk("123! @#$")
# '123! @#$'
 
cat_talk("")
# ''
```
 
Note: The outputs above are examples. Actual sounds vary randomly each time the function is called, unless `sounds` has only one sound.
 
### `cat_talk(text, sounds=CAT_SOUNDS)`
 
Replaces each word in `text` with a random cat sound and returns the modified string.
 
| **Argument** | **Description** |
| ------------ | --------------- |
| `text` | The string whose words will be replaced with cat sounds. |
| `sounds` | Optional list or tuple of cat sounds to choose from. Defaults to `CAT_SOUNDS`, the nine sounds listed in the rules above. |
 
### How It Works
 
1. **Validate the input.** Check that `text` is a string and that `sounds` isn't empty. If not, raise an error.
2. **Find each word.** Use a regular expression to find every run of letters, including apostrophes inside a word.
3. **Pick a sound.** For each word, randomly choose a sound from `sounds` using `random.choice()`.
4. **Match the capitalization.** Make the sound all caps or capitalized if the original word was.
5. **Preserve other characters.** Leave spaces, numbers, and punctuation unchanged, and return the result.
### Errors
 
The function raises:
 
- `TypeError` if `text` is not a string.
- `ValueError` if `sounds` is empty.
### Limitations
 
`cat_talk` is not reversible because every word is replaced with a random sound, so the original words can't be recovered.
 
 
### From the Command Line
 
```bash
pyjokelang cat-talk "Hello world!"
# Mrrp mrow!
 
pyjokelang cat-talk "I LOVE my cat."
# Nya HISS prrr meow.
```
 
The output varies each time because the sounds are randomized.


## Contributing

These steps work the same on macOS, Linux and Windows. You need Python 3.14 or newer.

### Set up

[Install pipenv](https://packaging.python.org/en/latest/tutorials/managing-dependencies/#managing-dependencies) if you don't have it yet. Then clone the repository and install the dependencies from the project root:

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-project-kitchen.git
cd python-package-exercise-project-kitchen
pipenv install --dev
```

This installs the development tools and the package itself in editable mode, so your code changes take effect without reinstalling. No environment variables or secret configuration files are needed.

### Run the tests

```bash
pipenv run python -m pytest
```

### Lint

The code must follow the PEP 8 style guide. Check it with pylint:

```bash
pipenv run pylint src tests examples
```

### Build

```bash
pipenv run python -m build
```

The package files are created in the `dist/` folder.

GitHub Actions runs the tests, the linter and the build on Python 3.14 and 3.15 for every pull request to `main`. Make sure all three pass locally before you open a pull request.


## Team Members
- [Jade Leong](https://github.com/jade-leong)
- [Risha Chada](https://github.com/rishachada)
- [Sanjana Chauhan](https://github.com/schauhans)
- [Seth DeRusha](https://github.com/sethderusha)
- [Yufei Huang](https://github.com/yufeiihuang)
