import pytest
from agent.tools.shell import run_shell_command

def test_run_shell_command_simple():
    result = run_shell_command.invoke({"command": "echo 'hello'"})
    assert "Command: echo 'hello'" in result
    assert "Stdout: hello" in result
    assert "Exit Code: 0" in result

def test_run_shell_command_error():
    result = run_shell_command.invoke({"command": "ls non_existent_dir"})
    assert "Command: ls non_existent_dir" in result
    assert "Stderr: ls: non_existent_dir: No such file or directory" in result
    assert "Exit Code: 1" in result

def test_run_shell_command_pipe():
    result = run_shell_command.invoke({"command": "echo 'hello' | wc -c"})
    assert "Command: echo 'hello' | wc -c" in result
    assert "Stdout: 6" in result
    assert "Exit Code: 0" in result

def test_run_shell_command_in_directory(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    f = d / "file.txt"
    f.write_text("content")
    result = run_shell_command.invoke({"command": "ls", "directory": str(d)})
    assert f"Directory: {d}" in result
    assert "Stdout: file.txt" in result
    assert "Exit Code: 0" in result
