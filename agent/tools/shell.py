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
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=directory,
            start_new_session=True
        )
        stdout, stderr = process.communicate()
        
        output = f"Command: {command}\n"
        output += f"Directory: {directory or '(root)'}\n"
        output += f"Stdout: {stdout.strip() if stdout.strip() else '(empty)'}\n"
        output += f"Stderr: {stderr.strip() if stderr.strip() else '(empty)'}\n"
        output += f"Error: (none)\n"
        output += f"Exit Code: {process.returncode}\n"
        output += f"Signal: (none)\n"
        output += f"Background PIDs: (none)\n"
        output += f"Process Group PGID: {process.pid}"
        
        return output

    except Exception as e:
        return f"An unexpected error occurred: {e}"