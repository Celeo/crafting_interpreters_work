import sys

from crafting_interpreters.ast_printer import AstPrinter
from crafting_interpreters.parser import Parser

from .scanner import Scanner


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
    if run(content):
        sys.exit(65)


def run_prompt() -> None:
    """Run a REPL in the terminal."""
    while True:
        line = input("> ")
        if not line:
            break
        run(line)


def run(content: str) -> bool:
    """Execute the given code."""
    scanner = Scanner(content)
    scanner.scan_tokens()
    if scanner.had_error:
        return True

    parser = Parser(scanner.tokens)
    expression = parser.parse()
    if parser.had_error:
        return True

    if expression:
        print(AstPrinter().format_ast(expression))
    return False


if __name__ == "__main__":
    main()
