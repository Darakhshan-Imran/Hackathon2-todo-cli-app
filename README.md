# Run in REPL mode
  uv run python -m src.main

  # Then try:
  todo> add "Test task" "My description"
  todo> list
  todo> show 1
  todo> complete 1
  todo> list --status complete
  todo> update 1 --title "Updated task"
  todo> incomplete 1
  todo> delete 1
  todo> help
  todo> exit