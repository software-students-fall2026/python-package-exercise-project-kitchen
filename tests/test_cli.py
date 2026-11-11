"""Tests for the pyjokelang command-line interface."""

from pyjokelang.__main__ import main


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
