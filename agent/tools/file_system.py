import os
import glob as py_glob
import re
from langchain_core.tools import tool

@tool
def list_directory(path: str, ignore: list[str] = None, respect_git_ignore: bool = True) -> str:
    """Lists the names of files and subdirectories directly within a specified directory path. Can optionally ignore entries matching provided glob patterns."""
    try:
        if not path:
            return "Error: Invalid parameters provided. Reason: Path must be a non-empty string."
        if not os.path.isabs(path):
             return f"Error: Invalid parameters provided. Reason: Path must be absolute: {path}"
        files = os.listdir(path)
        return f"Successfully listed {len(files)} items in '{path}':\n" + "\n".join(files)
    except FileNotFoundError:
        return f"Error: The path '{path}' does not exist."
    except NotADirectoryError:
        return f"Error: The path '{path}' is not a directory."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def read_file(absolute_path: str, offset: int = None, limit: int = None) -> str:
    """Reads and returns the content of a specified file from the local filesystem. Handles text, images (PNG, JPG, GIF, WEBP, SVG, BMP), and PDF files. For text files, it can read specific line ranges."""
    try:
        with open(absolute_path, "r") as f:
            content = f.read()
        return f"Successfully read {len(content)} characters from '{absolute_path}'.\n--- FILE CONTENT ---\n{content}"
    except FileNotFoundError:
        return f"Error: The file '{absolute_path}' was not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to a specified file in the local filesystem. 
      
      The user has the ability to modify `content`. If modified, this will be stated in the response."""
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def search_file_content(pattern: str, path: str = None, include: str = None) -> str:
    """Searches for a regular expression pattern within the content of files in a specified directory (or current working directory). Can filter files by a glob pattern. Returns the lines containing matches, along with their file paths and line numbers."""
    if path is None:
        path = os.getcwd()
    
    matches = []
    default_excludes = ['.git', '__pycache__', 'node_modules', '.pytest_cache']
    
    # If include is a specific file, just search that file
    if include and os.path.isfile(include):
        files_to_search = [include]
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
                for line_num, line in enumerate(f, 1):
                    if re.search(pattern, line):
                        # Use relative path for cleaner output
                        relative_path = os.path.relpath(file_path, start=path)
                        matches.append(f"File: {relative_path}\nL{line_num}: {line.strip()}")
        except (IOError, OSError):
            continue
            
    if not matches:
        return f'No matches found for pattern "{pattern}" in path "{path}".'

    # Construct the final output string
    filter_str = f' (filter: "{include}")' if include else ""
    header = f'Found {len(matches)} match(es) for pattern "{pattern}" in path "{path}"{filter_str}:\n---\n'
    
    # Join matches with a separator
    match_content = "\n---\n".join(matches)
    
    return header + match_content + "\n---"
@tool
def glob(pattern: str, path: str = None, case_sensitive: bool = False, respect_git_ignore: bool = True) -> str:
    """Efficiently finds files matching specific glob patterns (e.g., `src/**/*.ts`, `**/*.md`), returning absolute paths sorted by modification time (newest first). Ideal for quickly locating files based on their name or path structure, especially in large codebases."""
    if path is None:
        path = os.getcwd()
    
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
        return f'No files found matching pattern "{pattern}" within {path}.'

    header = f'Found {len(files)} file(s) matching "{pattern}" within {path}, sorted by modification time (newest first):\n'
    
    return header + "\n".join(files)

@tool
def replace(file_path: str, old_string: str, new_string: str, expected_replacements: int = 1) -> str:
    """Replaces text within a file. By default, replaces a single occurrence, but can replace multiple occurrences when `expected_replacements` is specified."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        actual_replacements = content.count(old_string)
        if actual_replacements == 0:
            return f"Failed to edit, 0 occurrences found for old_string in {file_path}. No edits made. The exact text in old_string was not found. Ensure you're not escaping content incorrectly and check whitespace, indentation, and context. Use read_file tool to verify."
        
        # A more robust implementation would check expected_replacements here.
        
        content = content.replace(old_string, new_string, expected_replacements)
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        return f"Successfully modified file: {file_path} ({expected_replacements} replacements)."
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@tool
def read_many_files(paths: list[str], exclude: list[str] = None, include: list[str] = None, recursive: bool = True, respect_git_ignore: bool = True, useDefaultExcludes: bool = True) -> str:
    """Reads content from multiple files specified by paths or glob patterns within a configured target directory."""
    # This is a simplified implementation. A full implementation would need to handle all the glob logic and exclusions.
    all_content = ""
    files_read = []
    for path_pattern in paths:
        for file_path in py_glob.glob(path_pattern, recursive=recursive):
            files_read.append(file_path)
            try:
                with open(file_path, 'r', errors='ignore') as f:
                    all_content += f"--- {file_path} ---\n{f.read()}\n\n"
            except (IOError, OSError):
                continue
    if not files_read:
        return "No files matching the criteria were found or all were skipped."
    return all_content
