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
