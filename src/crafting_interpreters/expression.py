from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar

from .shared import Token

R = TypeVar("R")


class Visitor[R](ABC):
    """Visitor pattern implementation."""

    @abstractmethod
    def visit_binary(self, expr: "Binary") -> R: ...

    @abstractmethod
    def visit_grouping(self, expr: "Grouping") -> R: ...

    @abstractmethod
    def visit_literal(self, expr: "Literal") -> R: ...

    @abstractmethod
    def visit_unary(self, expr: "Unary") -> R: ...


class Expr(ABC):
    """AST expression."""

    @abstractmethod
    def accept(self, visitor: Visitor[R]) -> R: ...


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary(self)
