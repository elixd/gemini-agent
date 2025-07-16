import subprocess
from langchain_core.tools import tool

@tool
def run_shell_command(command: str, directory: str = None, description: str = None) -> str:
    """This tool executes a given shell command as `bash -c <command>`. Command can start background processes using `&`. Command is executed as a subprocess that leads its own process group. Command process group can be terminated as `kill -- -PGID` or signaled as `kill -s SIGNAL -- -PGID`.

The following information is returned:

Command: Executed command.
Directory: Directory (relative to project root) where command was executed, or `(root)`.
Stdout: Output on stdout stream. Can be `(empty)` or partial on error and for any unwaited background processes.
Stderr: Output on stderr stream. Can be `(empty)` or partial on error and for any unwaited background processes.
Error: Error or `(none)` if no error was reported for the subprocess.
Exit Code: Exit code or `(none)` if terminated by signal.
Signal: Signal number or `(none)` if no signal was received.
Background PIDs: List of background processes started or `(none)`.
Process Group PGID: Process group started or `(none)`"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            cwd=directory
        )
        # The output is a structured string for clarity.
        return f"Command executed successfully.\n--- STDOUT ---\n{result.stdout}\n--- STDERR --n{result.stderr}"
    except subprocess.CalledProcessError as e:
        return f"Command failed with return code {e.returncode}.\n--- STDOUT ---\n{e.stdout}\n--- STDERR ---\n{e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"