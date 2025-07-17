# Tool Behavior Documentation

This document outlines the behavior of the available tools by showcasing their output in various scenarios.

## `list_directory`

### Scenario 1: List an existing directory

**Tool Call:**
```json
{
  "tool_name": "list_directory",
  "parameters": {
    "path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir"
  }
}
```

**Output:**
```
Directory listing for /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir:
[DIR] subdir
file1.txt
file2.log
```

### Scenario 2: List a non-existent directory

**Tool Call:**
```json
{
  "tool_name": "list_directory",
  "parameters": {
    "path": "/Users/ilya/Documents/projects/gemini-test/non_existent_dir"
  }
}
```

**Output:**
```
Error listing directory: ENOENT: no such file or directory, stat '/Users/ilya/Documents/projects/gemini-test/non_existent_dir'
```

### Scenario 3: List a file instead of a directory

**Tool Call:**
```json
{
  "tool_name": "list_directory",
  "parameters": {
    "path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt"
  }
}
```

**Output:**
```
Error: Path is not a directory: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt
```

### Scenario 4: List a directory with an ignored file pattern

**Tool Call:**
```json
{
  "tool_name": "list_directory",
  "parameters": {
    "path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir",
    "ignore": [
      "*.log"
    ]
  }
}
```

**Output:**
```
Directory listing for /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir:
[DIR] subdir
file1.txt
```

### Scenario 5: List the current directory

**Tool Call:**
```json
{
  "tool_name": "list_directory",
  "parameters": {
    "path": "/Users/ilya/Documents/projects/gemini-test"
  }
}
```

**Output:**
```
Directory listing for /Users/ilya/Documents/projects/gemini-test:
[DIR] __pycache__
[DIR] .pytest_cache
[DIR] agent
[DIR] agent_concept
[DIR] core
[DIR] examples
[DIR] gemini_agent.egg-info
[DIR] tests
[DIR] tool_documentation_test_dir
.env
.gitignore
cli.py
exact_reply_test.txt
main.py
memory.json
raw_api_cli.py
README.md
requirements.txt
tool_output_test.txt

(1 items were git-ignored)
```

## `read_file`

### Scenario 1: Read an existing file

**Tool Call:**
```json
{
  "tool_name": "read_file",
  "parameters": {
    "absolute_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt"
  }
}
```

**Output:**
```
This is a test file for documentation.
It has multiple lines.
```

### Scenario 2: Read a non-existent file

**Tool Call:**
```json
{
  "tool_name": "read_file",
  "parameters": {
    "absolute_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/non_existent_file.txt"
  }
}
```

**Output:**
```
File not found: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/non_existent_file.txt
```

### Scenario 3: Read a directory

**Tool Call:**
```json
{
  "tool_name": "read_file",
  "parameters": {
    "absolute_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir"
  }
}
```

**Output:**
```
Path is a directory, not a file: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir
```

## `write_file`

### Scenario 1: Write to a new file

**Tool Call:**
```json
{
  "tool_name": "write_file",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/new_file.txt",
    "content": "This is a new file."
  }
}
```

**Output:**
```
Successfully created and wrote to new file: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/new_file.txt.
```

### Scenario 2: Overwrite an existing file

**Tool Call:**
```json
{
  "tool_name": "write_file",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt",
    "content": "This is overwritten content."
  }
}
```

**Output:**
```
Successfully overwrote file: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt.
```

### Scenario 3: Write to a path that is a directory

**Tool Call:**
```json
{
  "tool_name": "write_file",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir",
    "content": "This should fail."
  }
}
```

**Output:**
```
Error: Invalid parameters provided. Reason: Path is a directory, not a file: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir
```

### Scenario 4: Write to a path where the directory does not exist

**Tool Call:**
```json
{
  "tool_name": "write_file",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/new_dir/new_file.txt",
    "content": "This should also fail."
  }
}
```

**Output:**
```
Successfully created and wrote to new file: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/new_dir/new_file.txt.
```

## `replace`

### Scenario 1: Replace a single occurrence of a string

**Tool Call:**
```json
{
  "tool_name": "replace",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt",
    "old_string": "line 2",
    "new_string": "line two"
  }
}
```

**Output:**
```
Failed to edit, Expected 1 occurrence but found 2 for old_string in file: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt
```

### Scenario 2: Attempt to replace text in a non-existent file

**Tool Call:**
```json
{
  "tool_name": "replace",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/non_existent_file.txt",
    "old_string": "old text",
    "new_string": "new text"
  }
}
```

**Output:**
```
File not found: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/non_existent_file.txt
```

### Scenario 3: Attempt to replace text that does not exist in the file

**Tool Call:**
```json
{
  "tool_name": "replace",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt",
    "old_string": "line 5",
    "new_string": "line five"
  }
}
```

**Output:**
```
Failed to edit, 0 occurrences found for old_string in /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt. No edits made. The exact text in old_string was not found. Ensure you're not escaping content incorrectly and check whitespace, indentation, and context. Use read_file tool to verify.
```

### Scenario 4: Replace all occurrences of a string

**Tool Call:**
```json
{
  "tool_name": "replace",
  "parameters": {
    "file_path": "/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt",
    "old_string": "line 2",
    "new_string": "line two",
    "expected_replacements": 2
  }
}
```

**Output:**
```
Successfully modified file: /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt (2 replacements).
```

## `run_shell_command`

### Scenario 1: Run a simple command

**Tool Call:**
```json
{
  "tool_name": "run_shell_command",
  "parameters": {
    "command": "ls -l"
  }
}
```

**Output:**
```
Command: ls -l
Directory: (root)
Stdout: total 80
drwxr-xr-x   5 ilya  staff   160 Jul 17 11:30 __pycache__
drwxr-xr-x   7 ilya  staff   224 Jul 17 21:49 agent
drwxr-xr-x  17 ilya  staff   544 Jul 16 23:58 agent_concept
-rw-r--r--   1 ilya  staff  7454 Jul 17 21:45 cli.py
drwxr-xr-x   7 ilya  staff   224 Jul 17 11:36 core
-rw-r--r--   1 ilya  staff    26 Jul 17 22:11 exact_reply_test.txt
drwxr-xr-x   4 ilya  staff   128 Jul 16 22:35 examples
drwxr-xr-x@  7 ilya  staff   224 Jul 16 09:28 gemini_agent.egg-info
-rw-r--r--   1 ilya  staff  4167 Jul 17 01:34 main.py
-rw-r--r--   1 ilya  staff   176 Jul 16 10:51 memory.json
-rw-r--r--   1 ilya  staff  4585 Jul 17 11:00 raw_api_cli.py
-rw-r--r--   1 ilya  staff     0 Jul 15 20:01 README.md
-rw-r--r--   1 ilya  staff  3280 Jul 17 00:10 requirements.txt
drwxr-xr-x   7 ilya  staff   224 Jul 17 10:31 tests
drwxr-xr-x   7 ilya  staff   224 Jul 17 22:34 tool_documentation_test_dir
-rw-r--r--   1 ilya  staff    45 Jul 17 22:05 tool_output_test.txt

Stderr: (empty)
Error: (none)
Exit Code: 0
Signal: (none)
Background PIDs: (none)
Process Group PGID: 79707
```

### Scenario 2: Run a command that produces an error

**Tool Call:**
```json
{
  "tool_name": "run_shell_command",
  "parameters": {
    "command": "ls non_existent_dir"
  }
}
```

**Output:**
```
Command: ls non_existent_dir
Directory: (root)
Stdout: (empty)
Stderr: ls: non_existent_dir: No such file or directory

Error: (none)
Exit Code: 1
Signal: (none)
Background PIDs: (none)
Process Group PGID: 79715
```

### Scenario 3: Run a command with a pipe

**Tool Call:**
```json
{
  "tool_name": "run_shell_command",
  "parameters": {
    "command": "echo \"hello\" | wc -c"
  }
}
```

**Output:**
```
Command: echo "hello" | wc -c
Directory: (root)
Stdout:        6

Stderr: (empty)
Error: (none)
Exit Code: 0
Signal: (none)
Background PIDs: (none)
Process Group PGID: 79723
```

### Scenario 4: Run a command in a specific directory

**Tool Call:**
```json
{
  "tool_name": "run_shell_command",
  "parameters": {
    "command": "ls -l",
    "directory": "tool_documentation_test_dir"
  }
}
```

**Output:**
```
Command: ls -l
Directory: tool_documentation_test_dir
Stdout: total 16
-rw-r--r--  1 ilya  staff  38 Jul 17 22:34 file1.txt
-rw-r--r--  1 ilya  staff   0 Jul 17 22:33 file2.log
drwxr-xr-x  3 ilya  staff  96 Jul 17 22:34 new_dir
-rw-r--r--  1 ilya  staff  19 Jul 17 22:34 new_file.txt
drwxr-xr-x  3 ilya  staff  96 Jul 17 22:33 subdir

Stderr: (empty)
Error: (none)
Exit Code: 0
Signal: (none)
Background PIDs: (none)
Process Group PGID: 79731
```

## `search_file_content`

### Scenario 1: Search for a pattern in a specific file

**Tool Call:**
```json
{
  "tool_name": "search_file_content",
  "parameters": {
    "pattern": "hello",
    "include": "tool_documentation_test_dir/file1.txt"
  }
}
```

**Output:**
```
Found 2 matches for pattern "hello" in path "." (filter: "tool_documentation_test_dir/file1.txt"):
---
File: tool_documentation_test_dir/file1.txt
L1: hello world
L3: hello again
---
```

### Scenario 2: Search for a pattern in a directory

**Tool Call:**
```json
{
  "tool_name": "search_file_content",
  "parameters": {
    "pattern": "hello",
    "path": "tool_documentation_test_dir"
  }
}
```

**Output:**
```
Found 2 matches for pattern "hello" in path "tool_documentation_test_dir":
---
File: file1.txt
L1: hello world
L3: hello again
---
```

### Scenario 3: Search for a pattern that does not exist

**Tool Call:**
```json
{
  "tool_name": "search_file_content",
  "parameters": {
    "pattern": "goodbye",
    "include": "tool_documentation_test_dir/file1.txt"
  }
}
```

**Output:**
```
No matches found for pattern "goodbye" in path "." (filter: "tool_documentation_test_dir/file1.txt").
```

### Scenario 4: Search for a pattern in a non-existent directory

**Tool Call:**
```json
{
  "tool_name": "search_file_content",
  "parameters": {
    "pattern": "hello",
    "path": "non_existent_dir"
  }
}
```

**Output:**
```
Error: Invalid parameters provided. Reason: Failed to access path stats for /Users/ilya/Documents/projects/gemini-test/non_existent_dir: Error: ENOENT: no such file or directory, stat '/Users/ilya/Documents/projects/gemini-test/non_existent_dir'
```

## `glob`

### Scenario 1: Glob for `*.txt` files

**Tool Call:**
```json
{
  "tool_name": "glob",
  "parameters": {
    "pattern": "*.txt",
    "path": "tool_documentation_test_dir"
  }
}
```

**Output:**
```
Found 2 file(s) matching "*.txt" within /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir, sorted by modification time (newest first):
/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt
/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/new_file.txt
```

### Scenario 2: Glob for `*.log` files

**Tool Call:**
```json
{
  "tool_name": "glob",
  "parameters": {
    "pattern": "*.log",
    "path": "tool_documentation_test_dir"
  }
}
```

**Output:**
```
Found 1 file(s) matching "*.log" within /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir, sorted by modification time (newest first):
/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file2.log
```

### Scenario 3: Glob for `*`

**Tool Call:**
```json
{
  "tool_name": "glob",
  "parameters": {
    "pattern": "*",
    "path": "tool_documentation_test_dir"
  }
}
```

**Output:**
```
Found 3 file(s) matching "*" within /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir, sorted by modification time (newest first):
/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file1.txt
/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/new_file.txt
/Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir/file2.log
```

### Scenario 4: Glob for a non-existent pattern

**Tool Call:**
```json
{
  "tool_name": "glob",
  "parameters": {
    "pattern": "*.pdf",
    "path": "tool_documentation_test_dir"
  }
}
```

**Output:**
```
No files found matching pattern "*.pdf" within /Users/ilya/Documents/projects/gemini-test/tool_documentation_test_dir.
```

### Scenario 5: Glob in a non-existent directory

**Tool Call:**
```json
{
  "tool_name": "glob",
  "parameters": {
    "pattern": "*",
    "path": "non_existent_dir"
  }
}
```

**Output:**
```
Error: Invalid parameters provided. Reason: Search path does not exist /Users/ilya/Documents/projects/gemini-test/non_existent_dir
```
