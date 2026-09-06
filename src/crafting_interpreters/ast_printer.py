from typing import override

from .expression import Binary, Expr, Grouping, Literal, Unary, Visitor


class AstPrinter(Visitor[str]):
    def print_ast(self, expr: Expr) -> str:
        """Print the given Expression tree in a LISP-like format."""
        return expr.accept(self)

    @override
    def visit_binary(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.left, expr.right)

    @override
    def visit_grouping(self, expr: Grouping) -> str:
        return self._parenthesize("group", expr.expression)

    @override
    def visit_literal(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    @override
    def visit_unary(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, expr.right)

    def _parenthesize(self, name: str, *exprs: Expr) -> str:
        ret = f"({name}"
        for expr in exprs:
            ret += f" {expr.accept(self)}"
        ret += ")"
        return ret
