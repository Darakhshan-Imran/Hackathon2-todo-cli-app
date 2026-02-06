"""Main entry point for Todo CLI application."""

import shlex
import sys

from src.cli.commands import CommandHandler
from src.cli.parser import create_parser
from src.services import TodoService


def run_repl() -> int:
    """Run the REPL (Read-Eval-Print Loop).

    Returns:
        Exit code (0 for normal exit, 1 for error)
    """
    # Initialize shared service and handler
    service = TodoService()
    handler = CommandHandler(service)
    parser = create_parser()

    # Welcome message (FR-023)
    print("Todo CLI - In-Memory Task Manager")
    print("Type 'help' for available commands, 'exit' to quit.\n")

    while True:
        try:
            # Read input
            line = input("todo> ").strip()

            # Empty input shows help hint
            if not line:
                print("Type 'help' for available commands.")
                continue

            # Parse the command
            try:
                # Use shlex to handle quoted strings properly
                argv = shlex.split(line)
            except ValueError as e:
                print(f"Error: Invalid command syntax - {e}")
                continue

            # Parse arguments
            try:
                args = parser.parse_args(argv)
            except SystemExit:
                # argparse calls sys.exit on error; catch and continue
                continue

            # Execute command
            result = handler.execute(args)

            # Check for exit signal
            if result == -1:
                return 0

        except KeyboardInterrupt:
            print("\nGoodbye!")
            return 0
        except EOFError:
            print("\nGoodbye!")
            return 0


def run_single_command(argv: list[str]) -> int:
    """Run a single command and exit.

    Args:
        argv: Command-line arguments

    Returns:
        Exit code
    """
    service = TodoService()
    handler = CommandHandler(service)
    parser = create_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 1

    result = handler.execute(args)
    return 0 if result in (0, -1) else 1


def main() -> int:
    """Main entry point.

    Returns:
        Exit code
    """
    if len(sys.argv) > 1:
        # Single command mode
        return run_single_command(sys.argv[1:])
    else:
        # REPL mode
        return run_repl()


if __name__ == "__main__":
    sys.exit(main())
