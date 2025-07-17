# Technical Requirements for Tool Output

This document specifies the exact output requirements for each tool, ensuring consistent and predictable behavior. Developers must replicate these outputs precisely, including all syntax, formatting, and error messages.

## `list_directory`

### Requirements

1.  **Successful Listing:** When listing a valid directory, the output must be a string starting with `Directory listing for {absolute_path}:\n` followed by a newline-separated list of directory entries. Directories must be prefixed with `[DIR] `.
2.  **Non-Existent Directory:** If the specified path does not exist, the tool must return the exact error string: `Error listing directory: ENOENT: no such file or directory, stat '{absolute_path}'`.
3.  **Path is a File:** If the specified path is a file, not a directory, the tool must return the exact error string: `Error: Path is not a directory: {absolute_path}`.
4.  **Ignored Files:** When using the `ignore` parameter, the output should be a successful listing, but without the ignored files.

## `read_file`

### Requirements

1.  **Successful Read:** When reading an existing file, the tool must return the exact content of the file as a string.
2.  **Non-Existent File:** If the specified file does not exist, the tool must return the exact error string: `File not found: {absolute_path}`.
3.  **Path is a Directory:** If the specified path is a directory, the tool must return the exact error string: `Path is a directory, not a file: {absolute_path}`.

## `write_file`

### Requirements

1.  **New File Creation:** When writing to a new file, the tool must return the exact string: `Successfully created and wrote to new file: {absolute_path}.`
2.  **File Overwrite:** When overwriting an existing file, the tool must return the exact string: `Successfully overwrote file: {absolute_path}.`
3.  **Path is a Directory:** If the specified path is a directory, the tool must return the exact error string: `Error: Invalid parameters provided. Reason: Path is a directory, not a file: {absolute_path}`.
4.  **Non-Existent Directory in Path:** If the path contains a non-existent directory, the tool should create it and return the exact string: `Successfully created and wrote to new file: {absolute_path}.`

## `replace`

### Requirements

1.  **Successful Replacement:** When one or more replacements are made successfully, the tool must return the exact string: `Successfully modified file: {absolute_path} ({count} replacements).`
2.  **Incorrect Number of Occurrences:** If the number of occurrences found does not match `expected_replacements`, the tool must return the exact error string: `Failed to edit, Expected {expected_replacements} occurrence but found {actual_occurrences} for old_string in file: {absolute_path}`.
3.  **Non-Existent File:** If the specified file does not exist, the tool must return the exact error string: `File not found: {absolute_path}`.
4.  **String Not Found:** If the `old_string` is not found in the file, the tool must return the exact error string: `Failed to edit, 0 occurrences found for old_string in {absolute_path}. No edits made. The exact text in old_string was not found. Ensure you're not escaping content incorrectly and check whitespace, indentation, and context. Use read_file tool to verify.`

## `run_shell_command`

### Requirements

1.  **Successful Command:** For a successful command, the tool must return a string with the following format:
    ```
    Command: {command}
    Directory: {directory}
    Stdout: {stdout}
    Stderr: {stderr}
    Error: (none)
    Exit Code: 0
    Signal: (none)
    Background PIDs: (none)
    Process Group PGID: {pgid}
    ```
2.  **Command with Error:** For a command that produces an error, the tool must return a string with the same format as a successful command, but with the `Stderr` and `Exit Code` fields populated accordingly.
3.  **Piped Command:** Piped commands should be treated as a single command, and the output should follow the same format as a successful command.
4.  **Command in Directory:** When a directory is specified, the `Directory` field in the output must reflect the specified directory.
5.  **Forbidden Syntax:** If the command contains forbidden syntax (e.g., command substitution), the tool must reject it and return the exact error string: `Command rejected: {command}\nReason: Command substitution using $() is not allowed for security reasons`.

## `search_file_content`
`

### Requirements

1.  **Successful Search with Matches:** When matches are found, the output must be a string with the following format:
    ```
    Found {count} matches for pattern "{pattern}" in path "{path}" (filter: "{filter}"):
    ---
    File: {file_path}
    L{line_number}: {line_content}
    ---
    ```
2.  **Successful Search with No Matches:** If no matches are found, the tool must return the exact string: `No matches found for pattern "{pattern}" in path "{path}" (filter: "{filter}").`
3.  **Non-Existent Directory:** If the specified path does not exist, the tool must return the exact error string: `Error: Invalid parameters provided. Reason: Failed to access path stats for {absolute_path}: Error: ENOENT: no such file or directory, stat '{absolute_path}'`.

## `glob`

### Requirements

1.  **Successful Glob with Matches:** When files are found, the output must be a string with the following format:
    ```
    Found {count} file(s) matching "{pattern}" within {absolute_path}, sorted by modification time (newest first):
    {file_path_1}
    {file_path_2}
    ...
    ```
2.  **Successful Glob with No Matches:** If no files are found, the tool must return the exact string: `No files found matching pattern "{pattern}" within {absolute_path}.`
3.  **Non-Existent Directory:** If the specified path does not exist, the tool must return the exact error string: `Error: Invalid parameters provided. Reason: Search path does not exist {absolute_path}`.

