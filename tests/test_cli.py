"""Tests for the pyjokelang command-line interface."""

import runpy
import sys
from unittest.mock import patch

import pytest

from pyjokelang.__main__ import main
from pyjokelang.cat_talk import CAT_SOUNDS


def run_cli(capsys, *argv):
    """Run the CLI with the given arguments and return (exit code, stdout, stderr)."""
    code = main(list(argv))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


class Tests:
    """Unit tests for main()."""

    def test_scramble(self, capsys):
        """The scramble command prints the scrambled text, with or without a key."""
        code, out, _ = run_cli(capsys, "scramble", "Hello world, meet me at noon!")
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "Rvb g u!mn bt,oi mt sxeawlwvb\n", (
            f"Expected the default-key scramble. Instead, it printed {out!r}"
        )

        code, out, _ = run_cli(capsys, "scramble", "Meet me at noon!", "--key", "tacos")
        assert out == "F agehe vbh!gx n\n", (
            f"Expected the 'tacos' scramble. Instead, it printed {out!r}"
        )

        # words given separately (no quotes) are joined with single spaces
        code, out, _ = run_cli(capsys, "scramble", "Meet", "me", "at", "noon!", "-k", "tacos")
        assert out == "F agehe vbh!gx n\n", (
            f"Expected unquoted words to be joined. Instead, it printed {out!r}"
        )

    def test_unscramble(self, capsys):
        """The unscramble command restores text scrambled with the same key."""
        code, out, _ = run_cli(capsys, "unscramble", "Rvb g u!mn bt,oi mt sxeawlwvb")
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "Hello world, meet me at noon!\n", (
            f"Expected the original message. Instead, it printed {out!r}"
        )

        code, out, _ = run_cli(capsys, "unscramble", "F agehe vbh!gx n", "--key", "tacos")
        assert out == "Meet me at noon!\n", (
            f"Expected the original message with key 'tacos'. Instead, it printed {out!r}"
        )

        code, out, _ = run_cli(capsys, "unscramble", "F agehe vbh!gx n", "--key", "pizza")
        assert out != "Meet me at noon!\n", "Expected the wrong key not to restore the message"

    def test_pig_latin(self, capsys):
        """The Pig Latin commands translate in both directions."""
        code, out, _ = run_cli(capsys, "to-pig-latin", "Hello, world!")
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "ELLO,h-AY ORLD.W-AY\n", (
            f"Expected the Pig Latin translation. Instead, it printed {out!r}"
        )

        code, out, _ = run_cli(capsys, "from-pig-latin", "ELLO,h-AY ORLD.W-AY")
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "Hello, world!\n", (
            f"Expected the English translation. Instead, it printed {out!r}"
        )

    def test_baby_talk(self, capsys):
        """The baby-talk command uses intensity 1 by default and accepts --intensity."""
        phrase = "The children love chocolate"
        code, out, _ = run_cli(capsys, "baby-talk", phrase)
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "The chiwdwen wobe chocowate\n", (
            f"Expected intensity 1 by default. Instead, it printed {out!r}"
        )

        code, out, _ = run_cli(capsys, "baby-talk", phrase, "--intensity", "2")
        assert out == "De tiwdwen wobe tocowate\n", (
            f"Expected the intensity 2 translation. Instead, it printed {out!r}"
        )

        code, out, _ = run_cli(capsys, "baby-talk", "Water please", "-i", "0")
        assert out == "Watew pwease\n", (
            f"Expected intensity 0 to skip whole-word swaps. Instead, it printed {out!r}"
        )

    def test_ubbi_dubbi(self, capsys):
        """The ubbi-dubbi command uses the 'ub' prefix by default and accepts --prefix."""
        code, out, _ = run_cli(capsys, "ubbi-dubbi", "Hello world")
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "Hubellubo wuborld\n", (
            f"Expected the default 'ub' prefix. Instead, it printed {out!r}"
        )

        code, out, _ = run_cli(capsys, "ubbi-dubbi", "Hello world", "--prefix", "ob")
        assert out == "Hobellobo woborld\n", (
            f"Expected the custom 'ob' prefix. Instead, it printed {out!r}"
        )

    def test_random_caps(self, capsys):
        """The random-caps command prints the randomly capitalized text."""
        # always pick the uppercase option so the output is predictable
        with patch(
            "pyjokelang.random_caps.random.choice",
            side_effect=lambda options: options[1],
        ):
            code, out, _ = run_cli(capsys, "random-caps", "Hello, world!")
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "HELLO, WORLD!\n", (
            f"Expected every letter in uppercase. Instead, it printed {out!r}"
        )

        # always pick the lowercase option
        with patch(
            "pyjokelang.random_caps.random.choice",
            side_effect=lambda options: options[0],
        ):
            code, out, _ = run_cli(capsys, "random-caps", "Hello, world!")
        assert out == "hello, world!\n", (
            f"Expected every letter in lowercase. Instead, it printed {out!r}"
        )

    def test_cat_talk(self, capsys):
        """The cat-talk command replaces every word with a cat sound."""
        # always pick the first sound, "meow", so the output is predictable
        with patch(
            "pyjokelang.cat_talk.random.choice",
            side_effect=lambda sounds: sounds[0],
        ):
            code, out, _ = run_cli(capsys, "cat-talk", "Hello, WORLD! my cat")
        assert code == 0, f"Expected exit code 0. Instead, it returned {code}"
        assert out == "Meow, MEOW! meow meow\n", (
            f"Expected 'meow' with matching capitals. Instead, it printed {out!r}"
        )

        # without patching, every word still becomes one of the cat sounds
        code, out, _ = run_cli(capsys, "cat-talk", "one two three")
        assert all(word in CAT_SOUNDS for word in out.split()), (
            f"Expected only cat sounds. Instead, it printed {out!r}"
        )
        assert len(out.split()) == 3, f"Expected 3 words. Instead, it printed {out!r}"

    def test_no_command_shows_help(self, capsys):
        """Running with no command prints the list of commands and exits with code 2."""
        code, out, _ = run_cli(capsys)
        assert code == 2, f"Expected exit code 2. Instead, it returned {code}"
        assert "commands:" in out, f"Expected the help text. Instead, it printed {out!r}"
        assert "scramble" in out and "baby-talk" in out, (
            f"Expected every command to be listed. Instead, it printed {out!r}"
        )

    def test_help_option(self, capsys):
        """--help prints usage information and exits with code 0."""
        with pytest.raises(SystemExit) as exit_info:
            main(["--help"])
        assert exit_info.value.code == 0, (
            f"Expected exit code 0. Instead, it exited with {exit_info.value.code}"
        )
        assert "usage: pyjokelang" in capsys.readouterr().out, "Expected the usage line"

        with pytest.raises(SystemExit) as exit_info:
            main(["scramble", "--help"])
        assert exit_info.value.code == 0, "Expected a command's --help to exit with code 0"
        assert "--key" in capsys.readouterr().out, "Expected scramble's help to list --key"

    def test_bad_arguments(self, capsys):
        """Unknown commands, missing text, and invalid options exit with code 2."""
        for argv in (["shout", "hi"], ["scramble"], ["baby-talk", "hi", "-i", "5"]):
            with pytest.raises(SystemExit) as exit_info:
                main(argv)
            assert exit_info.value.code == 2, (
                f"Expected exit code 2 for {argv}. Instead, it exited with "
                f"{exit_info.value.code}"
            )
            assert "error:" in capsys.readouterr().err, f"Expected an error message for {argv}"

    def test_function_errors(self, capsys):
        """Errors raised by a function are shown as a clean message with exit code 2."""
        with pytest.raises(SystemExit) as exit_info:
            main(["scramble", "hi", "--key", "123"])
        assert exit_info.value.code == 2, (
            f"Expected exit code 2. Instead, it exited with {exit_info.value.code}"
        )
        err = capsys.readouterr().err
        assert "key must contain at least one letter" in err, (
            f"Expected the ValueError message. Instead, it printed {err!r}"
        )
        assert "Traceback" not in err, "Expected no traceback in the error output"

        with pytest.raises(SystemExit) as exit_info:
            main(["baby-talk", "Hello, world!"])
        assert exit_info.value.code == 2, "Expected exit code 2 for punctuation in baby talk"
        assert "letters" in capsys.readouterr().err, "Expected baby talk's error message"

    def test_missing_function(self, capsys, monkeypatch):
        """A command whose function doesn't exist prints a friendly error and exits with code 1."""
        monkeypatch.delattr("pyjokelang.scrambler.scramble")
        code, out, err = run_cli(capsys, "scramble", "hi")
        assert code == 1, f"Expected exit code 1. Instead, it returned {code}"
        assert "scramble() hasn't been written yet" in err, (
            f"Expected the not-written-yet message. Instead, it printed {err!r}"
        )
        assert out == "", f"Expected nothing on stdout. Instead, it printed {out!r}"

    def test_run_as_module(self, capsys, monkeypatch):
        """'python -m pyjokelang' runs the CLI and exits with its return code."""
        monkeypatch.setattr(sys, "argv", ["pyjokelang", "scramble", "hi"])
        monkeypatch.delitem(sys.modules, "pyjokelang.__main__", raising=False)
        with pytest.raises(SystemExit) as exit_info:
            runpy.run_module("pyjokelang", run_name="__main__")
        assert exit_info.value.code == 0, (
            f"Expected exit code 0. Instead, it exited with {exit_info.value.code}"
        )
        assert capsys.readouterr().out == "rq\n", "Expected the scrambled text 'rq'"
