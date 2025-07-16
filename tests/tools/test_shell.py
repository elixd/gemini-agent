from unittest.mock import patch, MagicMock
import subprocess

from agent.tools.shell import run_shell_command


def test_run_shell_command_success():
    """
    Tests that run_shell_command returns stdout on successful execution.
    """
    with patch("subprocess.run") as mock_run:
        # Configure the mock to simulate a successful command
        mock_result = MagicMock()
        mock_result.stdout = "file.txt\n"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        # Call the function
        result = run_shell_command.invoke({"command": "ls"})

        # Assert the result
        assert result == "file.txt\n"
        mock_run.assert_called_once_with(
            "ls", shell=True, capture_output=True, text=True, check=True
        )


def test_run_shell_command_error():
    """
    Tests that run_shell_command returns a formatted error string on failure.
    """
    with patch("subprocess.run") as mock_run:
        # Configure the mock to simulate a failed command
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="ls non_existent_dir", stderr="No such file or directory"
        )

        # Call the function
        result = run_shell_command.invoke({"command": "ls non_existent_dir"})

        # Assert the result
        assert "Error:" in result
        assert "Stderr: No such file or directory" in result

