"""Output formatters for Todo CLI - human-readable and JSON formats."""

import json
from typing import Any

from src.models import Todo


class OutputFormatter:
    """Formats command output for display."""

    def __init__(self, json_mode: bool = False) -> None:
        """Initialize the formatter.

        Args:
            json_mode: If True, output JSON; otherwise human-readable
        """
        self.json_mode = json_mode

    def format_todo_created(self, todo: Todo) -> str:
        """Format output for a newly created todo.

        Args:
            todo: The created Todo

        Returns:
            Formatted output string
        """
        if self.json_mode:
            return self._json_output({"success": True, "todo": todo.to_dict()})
        return f'Todo {todo.id} created: "{todo.title}"'

    def format_todo_list(self, todos: list[Todo]) -> str:
        """Format output for a list of todos.

        Args:
            todos: List of todos to display

        Returns:
            Formatted output string
        """
        if self.json_mode:
            return self._json_output({
                "success": True,
                "todos": [t.to_dict() for t in todos],
                "count": len(todos),
            })

        if not todos:
            return "No todos found. Use 'add' command to create one."

        # Build table
        lines = []
        header = f"{'ID':<4} {'Title':<30} {'Status':<12} {'Description':<30}"
        lines.append(header)
        lines.append("-" * len(header))

        for todo in todos:
            desc = todo.description if todo.description else "(no description)"
            if len(desc) > 27:
                desc = desc[:27] + "..."
            title = todo.title
            if len(title) > 27:
                title = title[:27] + "..."
            lines.append(
                f"{todo.id:<4} {title:<30} {todo.status.value:<12} {desc:<30}"
            )

        return "\n".join(lines)

    def format_todo_detail(self, todo: Todo) -> str:
        """Format output for a single todo's full details.

        Args:
            todo: The todo to display

        Returns:
            Formatted output string
        """
        if self.json_mode:
            return self._json_output({"success": True, "todo": todo.to_dict()})

        lines = [
            f"Todo #{todo.id}",
            "-" * 40,
            f"Title:       {todo.title}",
            f"Description: {todo.description or '(no description)'}",
            f"Status:      {todo.status.value}",
            f"Created:     {todo.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        return "\n".join(lines)

    def format_todo_completed(self, todo: Todo) -> str:
        """Format output for a todo marked as complete.

        Args:
            todo: The completed todo

        Returns:
            Formatted output string
        """
        if self.json_mode:
            return self._json_output({
                "success": True,
                "todo": todo.to_dict(),
                "message": f"Todo {todo.id} marked as complete",
            })
        return f"Todo {todo.id} marked as complete"

    def format_todo_incompleted(self, todo: Todo) -> str:
        """Format output for a todo marked as incomplete.

        Args:
            todo: The incompleted todo

        Returns:
            Formatted output string
        """
        if self.json_mode:
            return self._json_output({
                "success": True,
                "todo": todo.to_dict(),
                "message": f"Todo {todo.id} marked as incomplete",
            })
        return f"Todo {todo.id} marked as incomplete"

    def format_todo_updated(self, todo: Todo) -> str:
        """Format output for an updated todo.

        Args:
            todo: The updated todo

        Returns:
            Formatted output string
        """
        if self.json_mode:
            return self._json_output({
                "success": True,
                "todo": todo.to_dict(),
                "message": f"Todo {todo.id} updated",
            })
        return f"Todo {todo.id} updated"

    def format_todo_deleted(self, todo_id: int) -> str:
        """Format output for a deleted todo.

        Args:
            todo_id: The ID of the deleted todo

        Returns:
            Formatted output string
        """
        if self.json_mode:
            return self._json_output({
                "success": True,
                "message": f"Todo {todo_id} deleted",
            })
        return f"Todo {todo_id} deleted"

    def format_error(self, message: str, code: str) -> str:
        """Format an error message.

        Args:
            message: Error message
            code: Error code

        Returns:
            Formatted error string
        """
        if self.json_mode:
            return self._json_output({
                "error": True,
                "message": message,
                "code": code,
            })
        return f"Error: {message}"

    def format_goodbye(self) -> str:
        """Format the goodbye message.

        Returns:
            Formatted goodbye string
        """
        if self.json_mode:
            return self._json_output({
                "success": True,
                "message": "Session ended",
            })
        return "Goodbye!"

    def _json_output(self, data: dict[str, Any]) -> str:
        """Convert data to JSON string.

        Args:
            data: Dictionary to convert

        Returns:
            JSON string
        """
        return json.dumps(data, indent=2)


def get_help_text() -> str:
    """Get the help text for the CLI.

    Returns:
        Help text string
    """
    return """Todo CLI - In-Memory Task Manager

Commands:
  add "<title>" ["<description>"]     Create a new todo
  list [--status <status>]            Show all todos
  show <id>                           Show todo details
  complete <id>                       Mark as complete
  incomplete <id>                     Mark as incomplete
  update <id> [--title] [--desc]      Update todo fields
  delete <id>                         Remove a todo
  help                                Show this message
  exit                                Exit the application

Global Flags:
  --json                              Output as JSON

Examples:
  add "Buy groceries" "Milk, eggs"
  list --status incomplete
  complete 1
  update 1 --title "New title"
"""
