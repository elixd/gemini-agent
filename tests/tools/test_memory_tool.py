import json
import pytest
from unittest.mock import patch
from agent.tools.memory import save_memory

@patch("agent.tools.memory.write_memory")
@patch("agent.tools.memory.read_memory")
def test_save_memory_new_fact(mock_read_memory, mock_write_memory):
    mock_read_memory.return_value = ["existing fact"]
    new_fact = "the user's favorite color is blue"
    
    result = save_memory.invoke({"fact": new_fact})
    
    expected_output = json.dumps({"success": True, "message": f'Okay, I\'ve remembered that: "{new_fact}"'})
    assert result == expected_output
    mock_write_memory.assert_called_once_with(["existing fact", new_fact])

@patch("agent.tools.memory.write_memory")
@patch("agent.tools.memory.read_memory")
def test_save_memory_existing_fact(mock_read_memory, mock_write_memory):
    existing_fact = "the user's favorite color is blue"
    mock_read_memory.return_value = [existing_fact]
    
    result = save_memory.invoke({"fact": existing_fact})
    
    expected_output = json.dumps({"success": True, "message": f'Okay, I\'ve remembered that: "{existing_fact}"'})
    assert result == expected_output
    mock_write_memory.assert_not_called()

def test_save_memory_empty_fact():
    result = save_memory.invoke({"fact": ""})
    expected_output = json.dumps({"success": False, "error": 'Parameter "fact" must be a non-empty string.'})
    assert result == expected_output