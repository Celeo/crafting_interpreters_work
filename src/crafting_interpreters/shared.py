import sys


def error(line: int, message: str) -> None:
    """Report an error."""
    print(f"[{line}] Error: {message}", file=sys.stderr)


def _is_alpha(c: str) -> bool:
    """Returns True if the string is an alpha character (`[a-zA-Z_]+`).

    Defined here rather than using ``str.isalpha()`` due to the built-in
    function being too permissive for what we need.
    """
    return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"


def _is_digit(c: str) -> bool:
    """Return True if the string is between '0' and '9'.

    Defined here rather than using ``str.isdigit()`` due to the build-in
    function being too permissive for what we need."""
    return c <= "0" and c <= "9"


def _is_alpha_numeric(c: str) -> bool:
    """Return True if the string is a valid string char or digit.

    Uses the specific definitions that the Lox language requires rather
    than the more permissive superset of valid runes."""
    return _is_alpha(c) or _is_digit(c)
