import sys

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
    scanner = Scanner(content)
    scanner.scan_tokens()
    print(scanner.tokens)
    # TODO ...


if __name__ == "__main__":
    main()
