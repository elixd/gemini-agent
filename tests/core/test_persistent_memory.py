import json
from unittest.mock import patch, mock_open

from core.persistent_memory import read_memory, write_memory


@patch("os.path.exists")
@patch("builtins.open", new_callable=mock_open, read_data='["fact 1", "fact 2"]')
def test_read_memory_existing(mock_file, mock_exists):
    """
    Tests reading memory from an existing file.
    """
    mock_exists.return_value = True
    memory = read_memory()
    mock_exists.assert_called_once()
    mock_file.assert_called_once_with("memory.json", "r")
    assert memory == ["fact 1", "fact 2"]


@patch("os.path.exists")
def test_read_memory_non_existing(mock_exists):
    """
    Tests reading memory when the file does not exist.
    """
    mock_exists.return_value = False
    memory = read_memory()
    mock_exists.assert_called_once()
    assert memory == []


@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def test_write_memory(mock_json_dump, mock_file):
    """
    Tests writing memory to a file.
    """
    facts = ["fact 1", "fact 2"]
    write_memory(facts)
    mock_file.assert_called_once_with("memory.json", "w")
    mock_json_dump.assert_called_once_with(facts, mock_file(), indent=2)
