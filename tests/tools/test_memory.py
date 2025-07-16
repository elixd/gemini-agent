from unittest.mock import patch

from agent.tools.memory import save_memory


@patch("agent.tools.memory.write_memory")
@patch("agent.tools.memory.read_memory")
def test_save_memory_new_fact(mock_read_memory, mock_write_memory):
    """
    Tests that a new fact is correctly added to memory.
    """
    mock_read_memory.return_value = ["existing fact"]
    new_fact = "new fact"

    result = save_memory.invoke({"fact": new_fact})

    mock_read_memory.assert_called_once()
    mock_write_memory.assert_called_once_with(["existing fact", new_fact])
    assert "I will remember that" in result


@patch("agent.tools.memory.write_memory")
@patch("agent.tools.memory.read_memory")
def test_save_memory_existing_fact(mock_read_memory, mock_write_memory):
    """
    Tests that a duplicate fact is not added to memory.
    """
    existing_fact = "existing fact"
    mock_read_memory.return_value = [existing_fact]

    result = save_memory.invoke({"fact": existing_fact})

    mock_read_memory.assert_called_once()
    mock_write_memory.assert_not_called()
    assert "I will remember that" in result
