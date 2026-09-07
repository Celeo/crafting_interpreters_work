from typing import Any, override

from .expression import Binary, Expr, Grouping, Literal, Unary, Visitor
from .shared import TokenType


class Interpreter(Visitor[Any]):
    """Lox interpreter."""

    @override
    def visit_literal(self, expr: Literal) -> Any:
        return expr.value

    @override
    def visit_grouping(self, expr: Grouping) -> Any:
        return self._evaluate(expr.expression)

    @override
    def visit_unary(self, expr: Unary) -> Any:
        right = self._evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.BANG:
                return not self._is_truthy(right)
            case TokenType.MINUS:
                return -float(right)

        return None

    @override
    def visit_binary(self, expr: Binary) -> Any:
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match expr.operator.token_type:
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.STAR:
                return float(left) * float(right)
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                pass
            case TokenType.EQUAL_EQUAL:
                pass

        return None

    def _evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def _is_truthy(self, val: Any) -> bool:
        if val is None or val is False:
            return False
        return True
