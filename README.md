# pyjokelang

[![Build and test](https://github.com/software-students-fall2026/python-package-exercise-project-kitchen/actions/workflows/build.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-project-kitchen/actions/workflows/build.yml)

pyjokelang is a Python package that turns regular text into silly languages like Pig Latin, Baby Talk, Ubbi Dubbi, and Cat Talk. It also includes functions for scrambling and unscrambling messages and randomly changing capitalization. The package is meant to be a fun way to play around with text using Python.

## PyPI Package Page
[Link to package page](https://pypi.org/project/pyjokelang/)

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
    ubbi_dubbi
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
| `ubbi-dubbi` | English → Ubbi Dubbi (optional `--prefix`)|

Run `pyjokelang --help` to list the commands, or `pyjokelang <command> --help` to see a command's options.

If the `pyjokelang` command isn't found (for example on Windows, where pip's scripts folder may not be on your PATH), use `python -m pyjokelang` instead. It works exactly the same way.


## Pig Latin

`english_sentence_to_pig_latin` translates English text into Pig Latin, while `pig_latin_sentence_to_english` translates it back. The translator changes the order of letters in each word and uses helper functions to modify capitalization and punctuation.

### Translating English to Pig Latin

The vowels are `a`, `e`, `i`, `o`, and `u`. **Y never counts as a vowel.**

1. **Words starting with a consonant:** Move the first letter to the end of the word and add `-ay`.
2. **Words starting with a vowel:** Keep the word unchanged and add `-way`.
3. **Capitalization:** The word translator preserves the original capitalization of individual letters, while the sentence translator reverses uppercase and lowercase letters using `reverse_capitalization()`.
4. **Punctuation:** The sentence translator uses `reverse_punctuation()` to change `!` to `.`, `.` to `?`, and `?` to `!`. 
   * Other characters remain unchanged by this helper. Punctuation attached to words may move during translation.
5. **Full sentences:** Split the sentence into individual words, translate each word into Pig Latin, join the translated words with spaces, and apply the capitalization and punctuation helpers.
6. **Whitespace:** Multiple spaces between words are reduced to single spaces. Empty sentences return an empty string.

### Understanding the Pig Latin Helper Functions

The Pig Latin translator uses two helper functions to separate the translation process into smaller steps.

**`reverse_capitalization()`**

This first helper swaps the capitalization of alphabetic characters.

- Uppercase letters become lowercase.
- Lowercase letters become uppercase.
- Numbers, spaces, and punctuation will remain unchanged.

**`reverse_punctuation()`**

This helper changes common sentence-ending punctuation.

- Exclamation marks (`!`) become periods (`.`).
- Periods (`.`) become question marks (`?`).
- Question marks (`?`) become exclamation marks (`!`).

This transformation adds another layer of silliness to translated sentences.

### Pig Latin Design Decisions

### Design Decisions

Our implementation prioritizes simplicity and readability over linguistic accuracy.

For example, traditional Pig Latin sometimes moves an entire consonant cluster to the end of a word. Our translator only moves the first consonant.

This makes the transformation easier to understand and allows the reverse translator to use a straightforward set of rules.

We also chose to separate sentence translation from individual word translation.

This separation makes the code easier to maintain, test, and extend.

By using helper functions for capitalization and punctuation, we can modify individual behaviors without rewriting the entire translation process.

### Translating Pig Latin Back to English

`pig_latin_sentence_to_english` reverses the capitalization and punctuation transformations before translating each word back into English.

For each translated word:

1. **Words ending in `-way`:** Remove the final `-way` to recover the original vowel-starting word.
2. **Words ending in `-ay`:** Remove the final `-ay` and move the last remaining letter back to the beginning of the word.
3. **Other words:** If a word does not have a recognized Pig Latin suffix, leave it unchanged.
4. **Capitalization:** The sentence translator uses `reverse_capitalization()` again to restore the original uppercase and lowercase letters.
5. **Punctuation:** The `restore_punctuation()` helper reverses the punctuation changes made during translation.

The translator is designed to translate text in both directions, although certain punctuation placements and unusual word patterns may not round-trip correctly.

### Translation Examples

| **English** | **Pig Latin (Word Translation)** | **What Happens** |
| ----------- | -------------------------------- | ---------------- |
| hello | elloh-ay | `h` moves to the end |
| world | orldw-ay | `w` moves to the end |
| apple | apple-way | Starts with a vowel |
| string | trings-ay | Only the first consonant moves |
| yes | esy-ay | `y` is treated as a consonant |
| Quiet | uietQ-ay | The original capital `Q` moves to the end |

### `english_sentence_to_pig_latin(text)`

Translates an English sentence into Pig Latin and returns the modified string.

| **Argument** | **Description** |
| ------------ | --------------- |
| `text` | The English sentence to translate into Pig Latin. |

### `pig_latin_sentence_to_english(text)`

Translates a Pig Latin sentence back into English and returns the result.

| **Argument** | **Description** |
| ------------ | --------------- |
| `text` | The Pig Latin sentence to translate back into English. |

### How It Works

1. **Split the sentence.** Separate the input text into individual words.
2. **Translate each word.** Check whether the first letter is a vowel or consonant and apply the corresponding Pig Latin rule.
3. **Reconstruct the sentence.** Join the translated words with single spaces.
4. **Transform punctuation.** Apply `reverse_punctuation()` to change punctuation marks.
5. **Reverse capitalization.** Apply `reverse_capitalization()` to swap uppercase and lowercase letters.
6. **Translate back.** To recover the original sentence, reverse the capitalization and punctuation changes, remove the Pig Latin suffixes, and move consonants back to the beginning of their words.

### Examples

```python
from pyjokelang import (
    english_sentence_to_pig_latin,
    pig_latin_sentence_to_english
)

# Translate English into Pig Latin
english_sentence_to_pig_latin("Hello world")
# 'ELLOh-AY ORLDW-AY'

english_sentence_to_pig_latin("Apple")
# 'aPPLE-WAY'

english_sentence_to_pig_latin("string")
# 'TRINGS-AY'

# Translate Pig Latin back into English
pig_latin_sentence_to_english("ELLOh-AY ORLDW-AY")
# 'Hello world'

pig_latin_sentence_to_english("aPPLE-WAY")
# 'Apple'

pig_latin_sentence_to_english("TRINGS-AY")
# 'string'

# Empty strings
english_sentence_to_pig_latin("")
# ''

pig_latin_sentence_to_english("")
# ''
```

### From the Command Line

```bash
pyjokelang to-pig-latin "Hello world"
# ELLOh-AY ORLDW-AY

pyjokelang from-pig-latin "ELLOh-AY ORLDW-AY"
# Hello world

pyjokelang to-pig-latin "Apple"
# aPPLE-WAY

pyjokelang from-pig-latin "aPPLE-WAY"
# Apple
```

## Ubbi Dubbi

`ubbi_dubbi` converts English text into Ubbi Dubbi, a real English word game. It inserts a prefix, `ub` by default, before every group of vowels in each word, so "hello" becomes "hubellubo".

### Ubbi Dubbi Rules

1. **Vowel groups:** The vowels are `a`, `e`, `i`, `o`, and `u`. A run of consecutive vowels counts as one group and gets one prefix, so `speak` becomes `spubeak`.
2. **The letter `y`:** `y` counts as a vowel when it comes right after a consonant (`my` → `muby`). It is a consonant at the start of a word or right after a vowel (`yes` → `yubes`, `play` → `plubay`).
3. **Silent e:** A final `e` is left alone if the word has another vowel group (`make` → `mubake`). If it is the only vowel group, or part of a longer group like `ee`, it still gets a prefix (`me` → `mube`, `agree` → `ubagrubee`).
4. **Capitalization:** If a word starts with a capital vowel, the capital moves to the prefix (`Apple` → `Ubapple`). All-caps words get an all-caps prefix (`HELLO` → `HUBELLUBO`). Other capitals stay where they are.
5. **Whitespace:** Multiple spaces between words are reduced to single spaces. No leading or trailing whitespace is included in the output. Empty strings return an empty string.
6. **Words with no vowel groups** (like `shh`) are unchanged.
7. **Input restrictions:** Only English letters and whitespace are accepted. No numbers or punctuation allowed.

### `ubbi_dubbi(phrase, prefix="ub")`

Converts `phrase` into Ubbi Dubbi and returns the modified string.

| **Argument** | **Description** |
| ------------ | --------------- |
| `phrase` | The English text to convert. Accepts English letters and whitespace only. |
| `prefix` | Optional text inserted before each vowel group. Must be one or more English letters. Defaults to `"ub"`. Try `"ob"` or `"ib"` for other versions of the game. |

### Errors

The function raises:

- `TypeError` if `phrase` is not a string.
- `TypeError` if `prefix` is not a string.
- `ValueError` if `phrase` contains numbers, punctuation, or other unsupported characters.
- `ValueError` if `prefix` is empty or contains anything other than English letters.

### How It Works

1. **Validate the input.** Check that `phrase` and `prefix` are valid.
2. **Split the phrase.** The input text is split into individual words.
3. **Find vowel groups.** Each word is scanned for runs of consecutive vowels, using the `y` rule above.
4. **Insert the prefix.** The prefix is placed before each vowel group, matching the word's capitalization. A silent final `e` is skipped.
5. **Reconstruct the phrase.** The converted words are joined with single spaces.

### Limitations

The silent `e` and `y` rules are based on spelling, not pronunciation, so some words come out differently than they sound. For example, `canyon` becomes `cubanubyon`, because the `y` is treated as a vowel.

### Examples

```python
from pyjokelang import ubbi_dubbi

ubbi_dubbi("Hello world")
# 'Hubellubo wuborld'

# One prefix per group of vowels
ubbi_dubbi("speak")
# 'spubeak'

# Silent e
ubbi_dubbi("make")
# 'mubake'

# Capitalization
ubbi_dubbi("Apple HELLO")
# 'Ubapple HUBELLUBO'

# The letter y
ubbi_dubbi("my yes play")
# 'muby yubes plubay'

# Custom prefix
ubbi_dubbi("Hello world", prefix="ob")
# 'Hobellobo woborld'

# Multiple spaces
ubbi_dubbi("Hello   world")
# 'Hubellubo wuborld'

# Empty string
ubbi_dubbi("")
# ''
```

### From the Command Line

```bash
pyjokelang ubbi-dubbi "Hello world"
# Hubellubo wuborld

pyjokelang ubbi-dubbi "Hello world" --prefix ob
# Hobellobo woborld
```

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
2. **Intensity 1 (Intermediate):** Applies all basic letter replacements and replaces certain full words with baby talk equivalents. This is the default intensity level.
3. **Intensity 2 (Extreme):** Applies all previous transformations and additionally replaces letter combinations:
   - `th` → `d`
   - `ch` → `t`
4. **Capitalization:** Letter replacements preserve the original capitalization. Full-word replacements capitalize the first letter if the original word starts with a capital.
5. **Whitespace:** Multiple spaces between words are reduced to single spaces. No leading or trailing whitespace is included in the output. Empty strings return an empty string.
6. **Input restrictions:** Only English letters and whitespace are accepted. No numbers or punctuation allowed — babies don't know what those are yet!

### Full-Word Replacements

At intensity levels 1 and 2, the following words are replaced before individual letters are processed.

| **English** | **Baby Talk** |
| ----------- | ------------- |
| hello | hewwo |
| please | pwease |
| water | wawa |
| mother | mama |
| father | dada |

### `baby_talk(normal_phrase, intensity=1)`

Converts `normal_phrase` into baby talk using the specified intensity level and returns the modified string.

| **Argument** | **Description** |
| ------------ | --------------- |
| `normal_phrase` | The English text to convert into baby talk. Accepts English letters and whitespace only. |
| `intensity` | Optional transformation level: `0` for basic letter swaps, `1` for letter and full-word swaps, or `2` for extreme transformations. Defaults to `1`. |

### Errors

The function raises:

- `TypeError` if `normal_phrase` is not a string.
- `TypeError` if `intensity` is not an integer (booleans are also rejected).
- `ValueError` if `normal_phrase` contains numbers, punctuation, or other unsupported characters.
- `ValueError` if `intensity` is not `0`, `1`, or `2`.

### How It Works

1. **Validate the input.** Check that the phrase contains only English letters and whitespace, and that the intensity is a valid integer between 0 and 2.
2. **Split the phrase.** The input text is split into individual words.
3. **Check for keywords.** At intensity levels 1 and 2, each word is checked against a dictionary of predefined baby talk replacements. If a match is found, the entire word is replaced without further letter substitutions.
4. **Replace individual letters.** Words that do not match a keyword have their letters replaced according to the selected intensity level.
5. **Apply extreme transformations.** At intensity level 2, two-letter combinations (`th` and `ch`) are checked before individual letters to ensure the correct replacements.
6. **Reconstruct the phrase.** The translated words are joined with single spaces, without leading or trailing whitespace, and the resulting phrase is returned.

### Examples

```python
from pyjokelang import baby_talk

# Default intensity is 1
baby_talk("Hello world")
# 'Hewwo wowwd'

# Intensity 0: Basic letter replacements
baby_talk("Water please", 0)
# 'Watew pwease'

# Intensity 1: Letter and full-word replacements
baby_talk("Water please", 1)
# 'Wawa pwease'

# Intensity 2: Extreme transformations
baby_talk("The children love chocolate", 2)
# 'De tiwdwen wobe tocowate'

# Capitalization
baby_talk("Mother and Father", 1)
# 'Mama and Dada'

# Multiple spaces
baby_talk("Hello   world", 1)
# 'Hewwo wowwd'

# Empty string
baby_talk("", 1)
# ''
```

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
