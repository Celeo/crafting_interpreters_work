from dataclasses import dataclass
from typing import Any

from .shared import (
    KEYWORDS,
    Token,
    TokenType,
    error,
    is_alpha,
    is_alpha_numeric,
    is_digit,
)


@dataclass(init=False)
class Scanner:
    """Scanner utility."""

    source: str
    tokens: list[Token]
    _start: int
    _current: int
    _line: int
    had_error: bool

    def __init__(self, source: str) -> None:
        """Create class instance with given ``source``."""
        self.source = source
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self.had_error = False

    def scan_tokens(self) -> None:
        """Scan tokens from the source."""
        while not self._is_at_end():
            self._start = self._current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self._line))

    def _scan_token(self) -> None:
        c = self._advance()
        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
            case ",":
                self._add_token(TokenType.COMMA)
            case ".":
                self._add_token(TokenType.DOT)
            case "-":
                self._add_token(TokenType.MINUS)
            case "+":
                self._add_token(TokenType.PLUS)
            case ";":
                self._add_token(TokenType.SEMICOLON)
            case "*":
                self._add_token(TokenType.STAR)
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
            case "/":
                if self._match("/"):
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self._line += 1
            case '"':
                self._string()
            case _:
                if is_digit(c):
                    self._number()
                elif is_alpha(c):
                    self._identifier()
                else:
                    error(self._line, "Unexpected character.")
                    self.had_error = True

    def _advance(self) -> str:
        c = self.source[self._current]
        self._current += 1
        return c

    def _add_token(self, token_type: TokenType, literal: Any | None = None) -> None:
        text = self.source[self._start : self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self._current] != expected:
            return False
        self._current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self._current]

    def _peek_next(self) -> str:
        if self._current + 1 >= len(self.source):
            return "\0"
        return self.source[self._current + 1]

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self._line += 1
            self._advance()
        if self._is_at_end():
            error(self._line, "Unterminated string.")
            return
        self._advance()
        text = self.source[self._start + 1 : self._current - 1]
        self._add_token(TokenType.STRING, text)

    def _number(self) -> None:
        while is_digit(self._peek()):
            self._advance()
        if self._peek() == "." and is_digit(self._peek_next()):
            self._advance()
            while is_digit(self._peek()):
                self._advance()
        self._add_token(
            TokenType.NUMBER, float(self.source[self._start : self._current])
        )

    def _identifier(self) -> None:
        while is_alpha_numeric(self._peek()):
            self._advance()
        text = self.source[self._start : self._current]
        token_type = KEYWORDS.get(text)
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        self._add_token(token_type)

    def _is_at_end(self) -> bool:
        return self._current >= len(self.source)
