import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    """All possible token types."""

    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


KEYWORDS: dict[str, TokenType] = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}
"""Reserved Lox language keywords."""


@dataclass
class Token:
    """A single token."""

    token_type: TokenType
    lexeme: str
    literal: Any
    line: int

    def __str__(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"


def error(obj: int | Token, message: str) -> None:
    """Report an error.

    Importantly this only *logs* the error; no sort of record
    is kept of there being an error; that's the responsibility
    of the calling code."""
    if isinstance(obj, int):
        report(obj, "", message)
    else:
        # TODO line numbers here?
        if obj.token_type == TokenType.EOF:
            report(0, " at end", message)
        else:
            report(0, f"at '{obj.lexeme}'", message)


def report(line: int, where: str, message: str) -> None:
    """Report an error.

    Importantly this only *logs* the error; no sort of record
    is kept of there being an error; that's the responsibility
    of the calling code."""
    print(f"[line {line}] Error{where}: {message}", file=sys.stderr)


def is_alpha(c: str) -> bool:
    """Returns True if the string is an alpha character (`[a-zA-Z_]+`).

    Defined here rather than using ``str.isalpha()`` due to the built-in
    function being too permissive for what we need.
    """
    return ("a" <= c <= "z") or ("A" <= c <= "Z") or c == "_"


def is_digit(c: str) -> bool:
    """Return True if the string is between '0' and '9'.

    Defined here rather than using ``str.isdigit()`` due to the build-in
    function being too permissive for what we need."""
    return c >= "0" and c <= "9"


def is_alpha_numeric(c: str) -> bool:
    """Return True if the string is a valid string char or digit.

    Uses the specific definitions that the Lox language requires rather
    than the more permissive superset of valid runes."""
    return is_alpha(c) or is_digit(c)
