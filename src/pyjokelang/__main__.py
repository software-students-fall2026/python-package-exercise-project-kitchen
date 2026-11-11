"""
Command-line interface for pyjokelang.

Run it with either:
    pyjokelang <command> [options] TEXT
    python -m pyjokelang <command> [options] TEXT

Commands:
    to-pig-latin      English -> Pig Latin        pig_latin.english_sentence_to_pig_latin
    from-pig-latin    Pig Latin -> English        pig_latin.pig_latin_sentence_to_english
    baby-talk         English -> Baby Talk        baby_talk.baby_talk
    scramble          text -> gibberish           scrambler.scramble
    unscramble        gibberish -> text           scrambler.unscramble
    random-caps       text -> rAnDoM cApS         random_caps.random_caps
    cat-talk          text -> meow purr hiss      cat_talk.cat_talk
    ubbi-dubbi        English -> Ubbi Dubbi       ubbi_dubbi.ubbi_dubbi

Functions are looked up by name when a command runs, so a command whose
function hasn't been written yet prints a friendly error instead of
crashing the whole CLI. If you name your function differently, update the
name in your command's _add_<name>() function below.

Adding a new command:
1. Write an _add_<name>(subparsers) function like the ones below. It creates
   the subcommand, adds its arguments, and sets func= to a function that
   takes the parsed args and returns the translated text.
2. Call it from _build_parser().
"""

import argparse
import importlib
import sys

from pyjokelang.scrambler import DEFAULT_KEY


def _call(module_name, function_name, *args, **kwargs):
    """
    Call pyjokelang.<module_name>.<function_name>(*args, **kwargs).

    Raises:
        NotImplementedError: If the function doesn't exist yet.
    """
    module = importlib.import_module(f"pyjokelang.{module_name}")
    function = getattr(module, function_name, None)
    if function is None:
        raise NotImplementedError(f"{function_name}() hasn't been written yet")
    return function(*args, **kwargs)


def _text(args):
    """Join the TEXT words back into a single string."""
    return " ".join(args.text)


def _add_text_argument(parser):
    """Add the TEXT argument shared by every command."""
    parser.add_argument(
        "text",
        nargs="+",
        help="the text to translate (quotes are optional)",
    )


def _add_key_argument(parser, action):
    """Add the -k/--key option shared by scramble and unscramble."""
    parser.add_argument(
        "-k",
        "--key",
        default=DEFAULT_KEY,
        help=f"secret word used to {action} the text (default: {DEFAULT_KEY})",
    )


def _add_to_pig_latin(subparsers):
    """Register the 'to-pig-latin' command."""
    parser = subparsers.add_parser(
        "to-pig-latin",
        help="translate English into Pig Latin",
        description="Translate English into Pig Latin.",
    )
    _add_text_argument(parser)
    parser.set_defaults(
        func=lambda args: _call("pig_latin", "english_sentence_to_pig_latin", _text(args))
    )


def _add_from_pig_latin(subparsers):
    """Register the 'from-pig-latin' command."""
    parser = subparsers.add_parser(
        "from-pig-latin",
        help="translate Pig Latin back into English",
        description="Translate Pig Latin back into English.",
    )
    _add_text_argument(parser)
    parser.set_defaults(
        func=lambda args: _call("pig_latin", "pig_latin_sentence_to_english", _text(args))
    )


def _add_baby_talk(subparsers):
    """Register the 'baby-talk' command."""
    parser = subparsers.add_parser(
        "baby-talk",
        help="translate English into Baby Talk",
        description="Translate English into Baby Talk.",
    )
    _add_text_argument(parser)
    parser.add_argument(
        "-i",
        "--intensity",
        type=int,
        choices=(0, 1, 2),
        default=1,
        help="0 = letter swaps only, 1 = also swap whole words, "
        "2 = also swap 'th' and 'ch' (default: 1)",
    )
    parser.set_defaults(
        func=lambda args: _call("baby_talk", "baby_talk", _text(args), args.intensity)
    )


def _add_scramble(subparsers):
    """Register the 'scramble' command."""
    parser = subparsers.add_parser(
        "scramble",
        help="scramble text into gibberish",
        description="Scramble text into gibberish that only the same key can unscramble.",
    )
    _add_text_argument(parser)
    _add_key_argument(parser, "scramble")
    parser.set_defaults(
        func=lambda args: _call("scrambler", "scramble", _text(args), key=args.key)
    )


def _add_unscramble(subparsers):
    """Register the 'unscramble' command."""
    parser = subparsers.add_parser(
        "unscramble",
        help="turn scrambled gibberish back into the original text",
        description="Unscramble text that was scrambled with the same key.",
    )
    _add_text_argument(parser)
    _add_key_argument(parser, "unscramble")
    parser.set_defaults(
        func=lambda args: _call("scrambler", "unscramble", _text(args), key=args.key)
    )


def _add_random_caps(subparsers):
    """Register the 'random-caps' command."""
    parser = subparsers.add_parser(
        "random-caps",
        help="randomly capitalize each letter",
        description="Randomly uppercase or lowercase each letter. Spaces, numbers, "
        "and punctuation stay unchanged.",
    )
    _add_text_argument(parser)
    parser.set_defaults(
        func=lambda args: _call("random_caps", "random_caps", _text(args))
    )

def _add_cat_talk(subparsers):
    """Register the 'cat-talk' command."""
    parser = subparsers.add_parser(
        "cat-talk",
        help="turn every word into a random cat sound",
        description="Turn every word into a random cat sound.",
    )
    _add_text_argument(parser)
    parser.set_defaults(
        func=lambda args: _call("cat_talk", "cat_talk", _text(args))
    )

def _add_ubbi_dubbi(subparsers):
    """Register the 'ubbi-dubbi' command."""
    parser = subparsers.add_parser(
        "ubbi-dubbi",
        help="translate English into Ubbi Dubbi",
        description="Translate English into Ubbi Dubbi.",
    )
    _add_text_argument(parser)
    parser.add_argument(
        "-p",
        "--prefix",
        default="ub",
        help="text inserted before each group of vowels (default: ub)",
    )
    parser.set_defaults(
        func=lambda args: _call(
            "ubbi_dubbi", "ubbi_dubbi", _text(args), prefix=args.prefix
        )
    )


def _build_parser():
    """Create the argument parser with every command registered."""
    parser = argparse.ArgumentParser(
        prog="pyjokelang",
        description="Translate English into silly joke languages, and back again.",
    )
    subparsers = parser.add_subparsers(title="commands", metavar="<command>")
    _add_to_pig_latin(subparsers)
    _add_from_pig_latin(subparsers)
    _add_baby_talk(subparsers)
    _add_scramble(subparsers)
    _add_unscramble(subparsers)
    _add_random_caps(subparsers)
    _add_cat_talk(subparsers)
    _add_ubbi_dubbi(subparsers)
    return parser


def main(argv=None):
    """
    Run the command-line interface.

    Args:
        argv: List of command-line arguments. Defaults to sys.argv[1:].

    Returns:
        The exit code: 0 on success, 1 if the command isn't available yet,
        2 for bad arguments.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 2
    try:
        print(args.func(args))
    except NotImplementedError as error:
        print(f"pyjokelang: {error}", file=sys.stderr)
        return 1
    except (TypeError, ValueError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    sys.exit(main())
