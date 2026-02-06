"""Argument parser for Todo CLI commands."""

import argparse
from collections.abc import Sequence


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Returns:
        Configured ArgumentParser with all subcommands
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Todo CLI - In-Memory Task Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global flags
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add command
    add_parser = subparsers.add_parser("add", help="Create a new todo")
    add_parser.add_argument("title", help="Todo title")
    add_parser.add_argument(
        "description",
        nargs="?",
        default="",
        help="Todo description (optional)",
    )
    add_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # list command
    list_parser = subparsers.add_parser("list", help="Show all todos")
    list_parser.add_argument(
        "--status",
        choices=["complete", "incomplete"],
        help="Filter by status",
    )
    list_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # show command
    show_parser = subparsers.add_parser("show", help="Show todo details")
    show_parser.add_argument("id", help="Todo ID")
    show_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Mark todo as complete")
    complete_parser.add_argument("id", help="Todo ID")
    complete_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # incomplete command
    incomplete_parser = subparsers.add_parser(
        "incomplete", help="Mark todo as incomplete"
    )
    incomplete_parser.add_argument("id", help="Todo ID")
    incomplete_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # update command
    update_parser = subparsers.add_parser("update", help="Update todo fields")
    update_parser.add_argument("id", help="Todo ID")
    update_parser.add_argument("--title", help="New title")
    update_parser.add_argument("--description", help="New description")
    update_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # delete command
    delete_parser = subparsers.add_parser("delete", help="Remove a todo")
    delete_parser.add_argument("id", help="Todo ID")
    delete_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # help command (handled separately but needs subparser for consistency)
    subparsers.add_parser("help", help="Show help message")

    # exit/quit commands
    subparsers.add_parser("exit", help="Exit the application")
    subparsers.add_parser("quit", help="Exit the application")

    return parser


def parse_args(args: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: Command-line arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments namespace
    """
    parser = create_parser()
    return parser.parse_args(args)
