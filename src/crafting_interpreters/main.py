import sys


def main() -> None:
    """CLI entrypoint"""
    if len(sys.argv) > 2:
        print("Usage: jlox [script]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        run_file(sys.argv[0])
    else:
        run_prompt()


def run_file(path: str) -> None:
    """Load a file from the disk and run it's content"""
    with open(path) as f:
        content = f.read()
    run(content)


def run_prompt() -> None:
    """Run a REPL in the terminal"""
    while True:
        line = input("> ")
        if not line:
            break
        run(line)


def run(content: str) -> None:
    """Execute the code"""
    pass


if __name__ == "__main__":
    main()
