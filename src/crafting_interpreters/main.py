import sys

from .ast_printer import AstPrinter
from .expression import Binary, Grouping, Literal, Unary
from .scanner import Token
from .shared import TokenType


def main() -> None:
    """CLI entrypoint."""
    if len(sys.argv) > 2:
        print("Usage: jlox [script]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()


def run_file(path: str) -> None:
    """Load a file from the disk and run it's content."""
    with open(path) as f:
        content = f.read()
    run(content)


def run_prompt() -> None:
    """Run a REPL in the terminal."""
    while True:
        line = input("> ")
        if not line:
            break
        run(line)


def run(content: str) -> None:
    """Execute the given code."""
    # scanner = Scanner(content)
    # tokens = scanner.tokens
    # ast = AstPrinter()
    # print(ast.print_ast(tokens))

    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", None, 1), Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(Literal(45.67)),
    )
    ast = AstPrinter()
    print(ast.print_ast(expression))


if __name__ == "__main__":
    main()
