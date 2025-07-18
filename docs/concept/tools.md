# Agent Tool Reference

This document provides a reference for the core tools available to the agent. Tools are the agent's interface for interacting with the file system, executing commands, searching the web, and remembering information. They are the fundamental building blocks for accomplishing tasks.

The agent's workflow involves the Language Model deciding which tool to use, the tool being executed, and the result being fed back into the model's context for further reasoning.

---

## File System Interaction

These tools allow the agent to navigate and manipulate the file system. All file paths must be absolute.

### `list_directory`
-   **Description:** Lists the files and subdirectories within a specified directory.
-   **Parameters:**
    -   `path` (str): The absolute path to the directory.
-   **Usage:** Useful for exploring the project structure and finding files.

### `write_file`
-   **Description:** Writes content to a specified file. If the file exists, it will be overwritten. If it does not exist, it will be created.
-   **Parameters:**
    -   `file_path` (str): The absolute path to the file.
    -   `content` (str): The content to write to the file.
-   **Usage:** Creating new source code files, configuration files, or documentation.

### `replace`
-   **Description:** Replaces a specific string of text within a file. This tool requires significant context to ensure it modifies the correct location.
-   **Parameters:**
    -   `file_path` (str): The absolute path to the file.
    -   `old_string` (str): The exact, literal text to be replaced, including surrounding lines for context.
    -   `new_string` (str): The exact, literal text to replace the `old_string` with.
-   **Usage:** Refactoring code, fixing typos, or updating specific values in configuration.

---

## Code & Content Analysis

These tools are used to read and understand the content of files.

### `read_file`
-   **Description:** Reads and returns the content of a single specified file.
-   **Parameters:**
    -   `absolute_path` (str): The absolute path to the file.
-   **Usage:** The primary way the agent "sees" the content of a file to reason about it.

### `read_many_files`
-   **Description:** Reads and concatenates the content of multiple files at once, using glob patterns.
-   **Parameters:**
    -   `paths` (list[str]): A list of glob patterns or file paths.
-   **Usage:** Getting a broad overview of a component or module by reading all its related files in one step.

### `search_file_content`
-   **Description:** Searches for a regular expression pattern within files in a directory.
-   **Parameters:**
    -   `pattern` (str): The regex pattern to search for.
    -   `path` (str, optional): The directory to search within.
-   **Usage:** Quickly locating specific functions, variables, or configuration settings across the codebase.

### `glob`
-   **Description:** Finds all file paths that match a specific glob pattern.
-   **Parameters:**
    -   `pattern` (str): The glob pattern (e.g., `src/**/*.py`).
-   **Usage:** Finding all test files, all markdown documents, or all files of a certain type without needing to list directories manually.

---

## Command Execution

### `run_shell_command`
-   **Description:** Executes a shell command in the terminal.
-   **Parameters:**
    -   `command` (str): The command to execute.
-   **Safety:** This is a powerful tool. The agent's core instructions mandate that it must explain any command that modifies the file system or system state before executing it.
-   **Usage:** Running tests, installing dependencies, running linters, or executing build scripts.

---

## Memory & Knowledge

### `save_memory`
-   **Description:** Saves a specific piece of information to the agent's long-term "Persistent Memory."
-   **Parameters:**
    -   `fact` (str): The clear, self-contained fact to remember.
-   **Usage:** Used when the user explicitly says "remember that..." to provide personalization and long-term context.

---

## Web Interaction

### `google_web_search`
-   **Description:** Performs a web search using Google.
-   **Parameters:**
    -   `query` (str): The search query.
-   **Usage:** Finding up-to-date information, documentation for libraries, or answers to general knowledge questions.

### `web_fetch`
-   **Description:** Fetches the content from a given URL.
-   **Parameters:**
    -   `prompt` (str): A prompt containing the URL and instructions on what to do with the content.
-   **Usage:** Reading articles, documentation pages, or other web-based content directly.
