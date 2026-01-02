"""Integration tests for Todo CLI commands."""

import json

import pytest

from src.cli.commands import CommandHandler
from src.cli.parser import create_parser
from src.services import TodoService
from src.store import TodoStore


class CliOutputCapture:
    """Helper for capturing CLI output."""

    def __init__(self) -> None:
        self.lines: list[str] = []

    def capture(self, text: str) -> None:
        self.lines.append(text)

    def output(self) -> str:
        return "\n".join(self.lines)

    def last(self) -> str:
        return self.lines[-1] if self.lines else ""


@pytest.fixture
def cli_setup():
    """Create a fresh CLI setup for each test."""
    store = TodoStore()
    service = TodoService(store)
    output = CliOutputCapture()
    handler = CommandHandler(service, output.capture)
    parser = create_parser()
    return {
        "handler": handler,
        "parser": parser,
        "output": output,
        "service": service,
    }


class TestAddCommand:
    """Tests for the add command."""

    def test_add_creates_todo(self, cli_setup) -> None:
        """add command creates a todo and outputs confirmation."""
        args = cli_setup["parser"].parse_args(["add", "Buy groceries"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        assert 'Todo 1 created: "Buy groceries"' in cli_setup["output"].last()
        assert cli_setup["service"].count() == 1

    def test_add_with_description(self, cli_setup) -> None:
        """add command accepts description argument."""
        args = cli_setup["parser"].parse_args(["add", "Buy groceries", "Milk, eggs"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        todo = cli_setup["service"].get_todo(1)
        assert todo.description == "Milk, eggs"

    def test_add_empty_title_fails(self, cli_setup) -> None:
        """add command fails with empty title."""
        args = cli_setup["parser"].parse_args(["add", ""])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()
        assert "Title" in cli_setup["output"].last()

    def test_add_json_output(self, cli_setup) -> None:
        """add command outputs JSON when --json flag is used."""
        args = cli_setup["parser"].parse_args(["add", "Test", "--json"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = json.loads(cli_setup["output"].last())
        assert output["success"] is True
        assert output["todo"]["title"] == "Test"
        assert output["todo"]["id"] == 1


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty(self, cli_setup) -> None:
        """list command shows message when no todos exist."""
        args = cli_setup["parser"].parse_args(["list"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        assert "No todos found" in cli_setup["output"].last()

    def test_list_shows_todos(self, cli_setup) -> None:
        """list command shows all todos."""
        cli_setup["service"].create_todo("First")
        cli_setup["service"].create_todo("Second")

        args = cli_setup["parser"].parse_args(["list"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = cli_setup["output"].last()
        assert "First" in output
        assert "Second" in output

    def test_list_filter_incomplete(self, cli_setup) -> None:
        """list command filters by incomplete status."""
        todo1 = cli_setup["service"].create_todo("Complete me")
        cli_setup["service"].create_todo("Keep me")
        cli_setup["service"].complete_todo(todo1.id)

        args = cli_setup["parser"].parse_args(["list", "--status", "incomplete"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = cli_setup["output"].last()
        assert "Keep me" in output
        assert "Complete me" not in output

    def test_list_filter_complete(self, cli_setup) -> None:
        """list command filters by complete status."""
        todo1 = cli_setup["service"].create_todo("Complete me")
        cli_setup["service"].create_todo("Keep me")
        cli_setup["service"].complete_todo(todo1.id)

        args = cli_setup["parser"].parse_args(["list", "--status", "complete"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = cli_setup["output"].last()
        assert "Complete me" in output
        assert "Keep me" not in output

    def test_list_json_output(self, cli_setup) -> None:
        """list command outputs JSON when --json flag is used."""
        cli_setup["service"].create_todo("Test")

        args = cli_setup["parser"].parse_args(["list", "--json"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = json.loads(cli_setup["output"].last())
        assert output["success"] is True
        assert output["count"] == 1
        assert len(output["todos"]) == 1


class TestShowCommand:
    """Tests for the show command."""

    def test_show_displays_todo(self, cli_setup) -> None:
        """show command displays todo details."""
        cli_setup["service"].create_todo("Test", "Description")

        args = cli_setup["parser"].parse_args(["show", "1"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = cli_setup["output"].last()
        assert "Test" in output
        assert "Description" in output

    def test_show_nonexistent_fails(self, cli_setup) -> None:
        """show command fails for nonexistent todo."""
        args = cli_setup["parser"].parse_args(["show", "99"])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()
        assert "99" in cli_setup["output"].last()

    def test_show_invalid_id_fails(self, cli_setup) -> None:
        """show command fails for invalid ID."""
        args = cli_setup["parser"].parse_args(["show", "abc"])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()

    def test_show_json_output(self, cli_setup) -> None:
        """show command outputs JSON when --json flag is used."""
        cli_setup["service"].create_todo("Test", "Desc")

        args = cli_setup["parser"].parse_args(["show", "1", "--json"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = json.loads(cli_setup["output"].last())
        assert output["success"] is True
        assert output["todo"]["title"] == "Test"


class TestCompleteCommand:
    """Tests for the complete command."""

    def test_complete_marks_todo(self, cli_setup) -> None:
        """complete command marks todo as complete."""
        cli_setup["service"].create_todo("Test")

        args = cli_setup["parser"].parse_args(["complete", "1"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        assert "marked as complete" in cli_setup["output"].last()
        todo = cli_setup["service"].get_todo(1)
        assert todo.is_complete()

    def test_complete_nonexistent_fails(self, cli_setup) -> None:
        """complete command fails for nonexistent todo."""
        args = cli_setup["parser"].parse_args(["complete", "99"])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()

    def test_complete_json_output(self, cli_setup) -> None:
        """complete command outputs JSON when --json flag is used."""
        cli_setup["service"].create_todo("Test")

        args = cli_setup["parser"].parse_args(["complete", "1", "--json"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = json.loads(cli_setup["output"].last())
        assert output["success"] is True
        assert output["todo"]["status"] == "complete"


class TestIncompleteCommand:
    """Tests for the incomplete command."""

    def test_incomplete_marks_todo(self, cli_setup) -> None:
        """incomplete command marks todo as incomplete."""
        todo = cli_setup["service"].create_todo("Test")
        cli_setup["service"].complete_todo(todo.id)

        args = cli_setup["parser"].parse_args(["incomplete", "1"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        assert "marked as incomplete" in cli_setup["output"].last()
        todo = cli_setup["service"].get_todo(1)
        assert not todo.is_complete()

    def test_incomplete_nonexistent_fails(self, cli_setup) -> None:
        """incomplete command fails for nonexistent todo."""
        args = cli_setup["parser"].parse_args(["incomplete", "99"])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()

    def test_incomplete_json_output(self, cli_setup) -> None:
        """incomplete command outputs JSON when --json flag is used."""
        todo = cli_setup["service"].create_todo("Test")
        cli_setup["service"].complete_todo(todo.id)

        args = cli_setup["parser"].parse_args(["incomplete", "1", "--json"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = json.loads(cli_setup["output"].last())
        assert output["success"] is True
        assert output["todo"]["status"] == "incomplete"


class TestUpdateCommand:
    """Tests for the update command."""

    def test_update_title(self, cli_setup) -> None:
        """update command updates title."""
        cli_setup["service"].create_todo("Original")

        args = cli_setup["parser"].parse_args(["update", "1", "--title", "Updated"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        assert "updated" in cli_setup["output"].last()
        todo = cli_setup["service"].get_todo(1)
        assert todo.title == "Updated"

    def test_update_description(self, cli_setup) -> None:
        """update command updates description."""
        cli_setup["service"].create_todo("Test", "Original")

        args = cli_setup["parser"].parse_args(
            ["update", "1", "--description", "New desc"]
        )
        result = cli_setup["handler"].execute(args)

        assert result == 0
        todo = cli_setup["service"].get_todo(1)
        assert todo.description == "New desc"

    def test_update_no_fields_fails(self, cli_setup) -> None:
        """update command fails when no fields provided."""
        cli_setup["service"].create_todo("Test")

        args = cli_setup["parser"].parse_args(["update", "1"])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()

    def test_update_nonexistent_fails(self, cli_setup) -> None:
        """update command fails for nonexistent todo."""
        args = cli_setup["parser"].parse_args(["update", "99", "--title", "Test"])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()

    def test_update_json_output(self, cli_setup) -> None:
        """update command outputs JSON when --json flag is used."""
        cli_setup["service"].create_todo("Original")

        args = cli_setup["parser"].parse_args(
            ["update", "1", "--title", "Updated", "--json"]
        )
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = json.loads(cli_setup["output"].last())
        assert output["success"] is True
        assert output["todo"]["title"] == "Updated"


class TestDeleteCommand:
    """Tests for the delete command."""

    def test_delete_removes_todo(self, cli_setup) -> None:
        """delete command removes todo."""
        cli_setup["service"].create_todo("Test")

        args = cli_setup["parser"].parse_args(["delete", "1"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        assert "deleted" in cli_setup["output"].last()
        assert cli_setup["service"].count() == 0

    def test_delete_nonexistent_fails(self, cli_setup) -> None:
        """delete command fails for nonexistent todo."""
        args = cli_setup["parser"].parse_args(["delete", "99"])
        result = cli_setup["handler"].execute(args)

        assert result == 1
        assert "Error:" in cli_setup["output"].last()

    def test_delete_json_output(self, cli_setup) -> None:
        """delete command outputs JSON when --json flag is used."""
        cli_setup["service"].create_todo("Test")

        args = cli_setup["parser"].parse_args(["delete", "1", "--json"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = json.loads(cli_setup["output"].last())
        assert output["success"] is True
        assert "deleted" in output["message"]


class TestHelpCommand:
    """Tests for the help command."""

    def test_help_shows_usage(self, cli_setup) -> None:
        """help command shows usage information."""
        args = cli_setup["parser"].parse_args(["help"])
        result = cli_setup["handler"].execute(args)

        assert result == 0
        output = cli_setup["output"].last()
        assert "add" in output
        assert "list" in output
        assert "complete" in output


class TestExitCommand:
    """Tests for the exit command."""

    def test_exit_returns_signal(self, cli_setup) -> None:
        """exit command returns special exit code."""
        args = cli_setup["parser"].parse_args(["exit"])
        result = cli_setup["handler"].execute(args)

        assert result == -1
        assert "Goodbye" in cli_setup["output"].last()

    def test_quit_returns_signal(self, cli_setup) -> None:
        """quit command returns special exit code."""
        args = cli_setup["parser"].parse_args(["quit"])
        result = cli_setup["handler"].execute(args)

        assert result == -1
        assert "Goodbye" in cli_setup["output"].last()
