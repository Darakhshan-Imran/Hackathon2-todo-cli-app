"""Command handlers for Todo CLI."""

import argparse
from collections.abc import Callable

from src.cli.formatters import OutputFormatter, get_help_text
from src.exceptions import TodoError
from src.services import TodoService


class CommandHandler:
    """Handles CLI commands by delegating to the service layer."""

    def __init__(
        self,
        service: TodoService | None = None,
        output_func: Callable[[str], None] | None = None,
    ) -> None:
        """Initialize the command handler.

        Args:
            service: The TodoService to use (creates new one if not provided)
            output_func: Function to output results (defaults to print)
        """
        self._service = service if service is not None else TodoService()
        self._output = output_func if output_func is not None else print

    def execute(self, args: argparse.Namespace) -> int:
        """Execute a command based on parsed arguments.

        Args:
            args: Parsed command-line arguments

        Returns:
            Exit code (0 for success, 1 for error)
        """
        json_mode = getattr(args, "json", False)
        formatter = OutputFormatter(json_mode)

        command = args.command

        if command is None or command == "help":
            return self._handle_help()
        if command in ("exit", "quit"):
            return self._handle_exit(formatter)

        try:
            if command == "add":
                return self._handle_add(args, formatter)
            if command == "list":
                return self._handle_list(args, formatter)
            if command == "show":
                return self._handle_show(args, formatter)
            if command == "complete":
                return self._handle_complete(args, formatter)
            if command == "incomplete":
                return self._handle_incomplete(args, formatter)
            if command == "update":
                return self._handle_update(args, formatter)
            if command == "delete":
                return self._handle_delete(args, formatter)

            # Unknown command
            self._output(formatter.format_error(
                f"Unknown command: {command}",
                "COMMAND_ERROR",
            ))
            return 1

        except TodoError as e:
            self._output(formatter.format_error(e.message, e.code))
            return 1

    def _handle_help(self) -> int:
        """Handle the help command."""
        self._output(get_help_text())
        return 0

    def _handle_exit(self, formatter: OutputFormatter) -> int:
        """Handle the exit/quit command."""
        self._output(formatter.format_goodbye())
        return -1  # Special exit code to signal REPL termination

    def _handle_add(self, args: argparse.Namespace, formatter: OutputFormatter) -> int:
        """Handle the add command."""
        todo = self._service.create_todo(args.title, args.description)
        self._output(formatter.format_todo_created(todo))
        return 0

    def _handle_list(
        self, args: argparse.Namespace, formatter: OutputFormatter
    ) -> int:
        """Handle the list command."""
        todos = self._service.get_all_todos(args.status)
        self._output(formatter.format_todo_list(todos))
        return 0

    def _handle_show(
        self, args: argparse.Namespace, formatter: OutputFormatter
    ) -> int:
        """Handle the show command."""
        todo = self._service.get_todo(args.id)
        self._output(formatter.format_todo_detail(todo))
        return 0

    def _handle_complete(
        self, args: argparse.Namespace, formatter: OutputFormatter
    ) -> int:
        """Handle the complete command."""
        todo = self._service.complete_todo(args.id)
        self._output(formatter.format_todo_completed(todo))
        return 0

    def _handle_incomplete(
        self, args: argparse.Namespace, formatter: OutputFormatter
    ) -> int:
        """Handle the incomplete command."""
        todo = self._service.incomplete_todo(args.id)
        self._output(formatter.format_todo_incompleted(todo))
        return 0

    def _handle_update(
        self, args: argparse.Namespace, formatter: OutputFormatter
    ) -> int:
        """Handle the update command."""
        todo = self._service.update_todo(
            args.id,
            title=args.title,
            description=args.description,
        )
        self._output(formatter.format_todo_updated(todo))
        return 0

    def _handle_delete(
        self, args: argparse.Namespace, formatter: OutputFormatter
    ) -> int:
        """Handle the delete command."""
        # Validate ID first to get the integer value for output
        from src.utils import validate_id
        todo_id = validate_id(args.id)
        self._service.delete_todo(args.id)
        self._output(formatter.format_todo_deleted(todo_id))
        return 0
