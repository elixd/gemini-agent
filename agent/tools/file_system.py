import os
import glob as py_glob
import re
from langchain_core.tools import tool

@tool
def list_directory(path: str, ignore: list[str] = None, respect_git_ignore: bool = True) -> str:
    """Lists the names of files and subdirectories directly within a specified directory path. Can optionally ignore entries matching provided glob patterns."""
    try:
        if not os.path.isdir(path):
            if os.path.exists(path):
                return f"Error: Path is not a directory: {path}"
            else:
                return f"Error listing directory: ENOENT: no such file or directory, stat '{path}'"

        items = os.listdir(path)
        if ignore:
            items = [item for item in items if not any(py_glob.fnmatch.fnmatch(item, pattern) for pattern in ignore)]

        output = f"Directory listing for {path}:\n"
        for item in sorted(items):
            if os.path.isdir(os.path.join(path, item)):
                output += f"[DIR] {item}\n"
            else:
                output += f"{item}\n"
        return output.strip()
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def read_file(absolute_path: str, offset: int = None, limit: int = None) -> str:
    """Reads and returns the raw content of a specified file. For text files, it can read specific line ranges."""
    if not os.path.isabs(absolute_path):
        return f"Error: Invalid parameters provided. Reason: File path must be absolute, but was relative: {absolute_path}. You must provide an absolute path."
    if os.path.isdir(absolute_path):
        return f"Path is a directory, not a file: {absolute_path}"
    try:
        with open(absolute_path, "r", errors='ignore') as f:
            # A more robust version would handle offset and limit for large files.
            content = f.read()
        return content
    except FileNotFoundError:
        return f"File not found: {absolute_path}"
    except Exception as e:
        return f"An unexpected error occurred while reading {absolute_path}: {e}"

@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to a specified file in the local filesystem."""
    if os.path.isdir(file_path):
        return f"Error: Invalid parameters provided. Reason: Path is a directory, not a file: {file_path}"
    try:
        was_present = os.path.exists(file_path)
        
        # Create directory if it doesn't exist
        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_path, "w") as f:
            f.write(content)
        
        if was_present:
            return f"Successfully overwrote file: {file_path}."
        else:
            return f"Successfully created and wrote to new file: {file_path}."
            
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def search_file_content(pattern: str, path: str = None, include: str = None) -> str:
    """Searches for a regular expression pattern within the content of files in a specified directory (or current working directory). Can filter files by a glob pattern. Returns the lines containing matches, along with their file paths and line numbers."""
    if path is None:
        path = os.getcwd()

    if not os.path.exists(path):
        return f"Error: Invalid parameters provided. Reason: Failed to access path stats for {os.path.join(os.getcwd(), path)}: Error: ENOENT: no such file or directory, stat '{os.path.join(os.getcwd(), path)}'"

    matches = []
    default_excludes = ['.git', '__pycache__', 'node_modules', '.pytest_cache']
    
    # If include is a specific file, just search that file
    if include and os.path.isfile(os.path.join(path, include)):
        files_to_search = [os.path.join(path, include)]
    # Otherwise, walk the directory
    else:
        files_to_search = []
        for root, dirs, files in os.walk(path):
            # Exclude common directories
            dirs[:] = [d for d in dirs if d not in default_excludes]
            
            for file in files:
                if include and not py_glob.fnmatch.fnmatch(file, include):
                    continue
                files_to_search.append(os.path.join(root, file))

    for file_path in files_to_search:
        try:
            with open(file_path, 'r', errors='ignore') as f:
                file_matches = []
                for line_num, line in enumerate(f, 1):
                    if re.search(pattern, line):
                        file_matches.append(f"L{line_num}: {line.strip()}")
                if file_matches:
                    relative_path = os.path.relpath(file_path, start=os.getcwd())
                    matches.append(f"File: {relative_path}\n" + "\n".join(file_matches))
        except (IOError, OSError):
            continue
            
    if not matches:
        filter_str = f' (filter: "{include}")' if include else ""
        return f'No matches found for pattern "{pattern}" in path "{path}"{filter_str}.'

    # Construct the final output string
    filter_str = f' (filter: "{include}")' if include else ""
    header = f'Found {len(matches)} matches for pattern "{pattern}" in path "{path}"{filter_str}:\n---\n'
    
    # Join matches with a separator
    match_content = "\n---\n".join(matches)
    
    return header + match_content + "\n---"
@tool
def glob(pattern: str, path: str = None, case_sensitive: bool = False, respect_git_ignore: bool = True) -> str:
    """Efficiently finds files matching specific glob patterns (e.g., `src/**/*.ts`, `**/*.md`), returning absolute paths sorted by modification time (newest first). Ideal for quickly locating files based on their name or path structure, especially in large codebases."""
    if path is None:
        path = os.getcwd()
    
    if not os.path.exists(path):
        return f"Error: Invalid parameters provided. Reason: Search path does not exist {os.path.join(os.getcwd(), path)}"

    # This is a simplified implementation. A real one would handle respect_git_ignore.
    recursive = '**' in pattern
    glob_path = os.path.join(path, pattern)
    
    # Perform the glob search
    files = py_glob.glob(glob_path, recursive=recursive)
    
    # Sort by modification time, newest first
    try:
        files.sort(key=os.path.getmtime, reverse=True)
    except FileNotFoundError:
        # Handle cases where a file disappears between glob and getmtime
        pass

    if not files:
        return f'No files found matching pattern "{pattern}" within {os.path.join(os.getcwd(), path)}.'

    header = f'Found {len(files)} file(s) matching "{pattern}" within {os.path.join(os.getcwd(), path)}, sorted by modification time (newest first):\n'
    
    return header + "\n".join(files)

@tool
def replace(file_path: str, old_string: str, new_string: str, expected_replacements: int = 1) -> str:
    """Replaces text within a file. By default, replaces a single occurrence, but can replace multiple occurrences when `expected_replacements` is specified."""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        actual_replacements = content.count(old_string)
        if actual_replacements == 0:
            return f"Failed to edit, 0 occurrences found for old_string in {file_path}. No edits made. The exact text in old_string was not found. Ensure you're not escaping content incorrectly and check whitespace, indentation, and context. Use read_file tool to verify."
        
        if actual_replacements != expected_replacements:
            return f"Failed to edit, Expected {expected_replacements} occurrence but found {actual_replacements} for old_string in file: {file_path}"
        
        content = content.replace(old_string, new_string, expected_replacements)
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        return f"Successfully modified file: {file_path} ({expected_replacements} replacements)."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def read_many_files(paths: list[str], exclude: list[str] = None, include: list[str] = None, recursive: bool = True, respect_git_ignore: bool = True, useDefaultExcludes: bool = True) -> str:
    """Reads content from multiple files specified by paths or glob patterns within a configured target directory."""
    all_content = ""
    files_read = []
    
    # Collect all files that match the include patterns
    for path_pattern in paths:
        for file_path in py_glob.glob(path_pattern, recursive=recursive):
            files_read.append(file_path)
            
    # Filter out files that match the exclude patterns
    if exclude:
        files_to_read = []
        for file_path in files_read:
            if not any(py_glob.fnmatch.fnmatch(file_path, pattern) for pattern in exclude):
                files_to_read.append(file_path)
    else:
        files_to_read = files_read

    if not files_to_read:
        return "No files matching the criteria were found or all were skipped."

    for file_path in files_to_read:
        try:
            with open(file_path, 'r', errors='ignore') as f:
                all_content += f"--- {file_path} ---\n\n{f.read()}\n\n"
        except (IOError, OSError):
            continue
            
    return all_content.strip()
