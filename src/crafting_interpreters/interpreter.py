import sys
from typing import Any, override

from .expression import Binary, Expr, Grouping, Literal, Unary, Visitor
from .shared import Token, TokenType


class Interpreter(Visitor[Any]):
    """Lox interpreter."""

    def __init__(self) -> None:
        self.had_runtime_error = True

    def interpret(self, expression: Expr) -> None:
        try:
            value = self._evaluate(expression)
            print(self._stringify(value))
        except LoxRuntimeError as e:
            self._runtime_error(e)

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
                self._check_number_operand(expr.operator, right)
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
                raise LoxRuntimeError(
                    expr.operator, "Operands must be two numbers or two strings."
                )
            case TokenType.MINUS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self._check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self._check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.GREATER:
                self._check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self._check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self._check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self._is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self._is_equal(left, right)

        return None

    def _evaluate(self, expr: Expr) -> Any:
        return expr.accept(self)

    def _is_truthy(self, val: Any) -> bool:
        return not (val is None or val is False)

    def _is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def _check_number_operand(self, operator: Token, operand: Any) -> None:
        if isinstance(operand, float):
            return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def _check_number_operands(self, operator: Token, left: Any, right: Any) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def _stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0:-2]
            return text
        return str(obj)

    def _runtime_error(self, error: "LoxRuntimeError") -> None:
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        self.had_runtime_error = True


class LoxRuntimeError(Exception):
    """Lox runtime error."""

    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = message
        super().__init__(message)
