import os
import pytest
from agent.tools.file_system import list_directory

def test_list_directory_existing(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    f = d / "file.txt"
    f.write_text("content")
    s = d / "subdir"
    s.mkdir()
    
    result = list_directory.invoke({"path": str(d)})
    header, *items = result.split('\n')
    
    assert header == f"Directory listing for {d}:"
    assert sorted(items) == ["[DIR] subdir", "file.txt"]

def test_list_directory_non_existent():
    expected_output = "Error listing directory: ENOENT: no such file or directory, stat '/non_existent_dir'"
    assert list_directory.invoke({"path": "/non_existent_dir"}) == expected_output

from agent.tools.file_system import list_directory, read_file
def test_list_directory_with_file(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("content")
    expected_output = f"Error: Path is not a directory: {f}"
    assert list_directory.invoke({"path": str(f)}) == expected_output

def test_read_file_existing(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello world")
    assert read_file.invoke({"absolute_path": str(f)}) == "hello world"

def test_read_file_non_existent():
    assert read_file.invoke({"absolute_path": "/non_existent_file.txt"}) == "File not found: /non_existent_file.txt"

from agent.tools.file_system import list_directory, read_file, write_file
def test_read_file_with_directory(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    assert read_file.invoke({"absolute_path": str(d)}) == f"Path is a directory, not a file: {d}"

def test_read_file_relative_path_error():
    relative_path = "memory.json"
    expected_error = f"Error: Invalid parameters provided. Reason: File path must be absolute, but was relative: {relative_path}. You must provide an absolute path."
    assert read_file.invoke({"absolute_path": relative_path}) == expected_error


def test_write_file_new(tmp_path):
    f = tmp_path / "new_file.txt"
    assert write_file.invoke({"file_path": str(f), "content": "new content"}) == f"Successfully created and wrote to new file: {f}."
    assert f.read_text() == "new content"

def test_write_file_overwrite(tmp_path):
    f = tmp_path / "existing_file.txt"
    f.write_text("old content")
    assert write_file.invoke({"file_path": str(f), "content": "new content"}) == f"Successfully overwrote file: {f}."
    assert f.read_text() == "new content"

def test_write_file_to_directory(tmp_path):
    d = tmp_path / "test_dir"
    d.mkdir()
    assert write_file.invoke({"file_path": str(d), "content": "content"}) == f"Error: Invalid parameters provided. Reason: Path is a directory, not a file: {d}"

from agent.tools.file_system import list_directory, read_file, write_file, replace
def test_write_file_to_non_existent_dir(tmp_path):
    f = tmp_path / "new_dir" / "new_file.txt"
    assert write_file.invoke({"file_path": str(f), "content": "content"}) == f"Successfully created and wrote to new file: {f}."
    assert f.read_text() == "content"

def test_replace_success(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello world")
    assert replace.invoke({"file_path": str(f), "old_string": "world", "new_string": "pytest"}) == f"Successfully modified file: {f} (1 replacements)."
    assert f.read_text() == "hello pytest"

def test_replace_file_not_found():
    assert replace.invoke({"file_path": "/non_existent_file.txt", "old_string": "a", "new_string": "b"}) == "File not found: /non_existent_file.txt"

def test_replace_string_not_found(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello world")
    expected_output = f"Failed to edit, 0 occurrences found for old_string in {f}. No edits made. The exact text in old_string was not found. Ensure you're not escaping content incorrectly and check whitespace, indentation, and context. Use read_file tool to verify."
    assert replace.invoke({"file_path": str(f), "old_string": "pytest", "new_string": "world"}) == expected_output

from agent.tools.file_system import list_directory, read_file, write_file, replace, search_file_content
def test_replace_incorrect_occurrences(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello hello world")
    expected_output = f"Failed to edit, Expected 1 occurrence but found 2 for old_string in file: {f}"
    assert replace.invoke({"file_path": str(f), "old_string": "hello", "new_string": "hi"}) == expected_output

def test_search_file_content_with_matches(tmp_path):
    d = tmp_path / "search_dir"
    d.mkdir()
    f = d / "file.txt"
    f.write_text("hello world\nhello pytest")
    expected_output = f'Found 1 matches for pattern "hello" in path "{d}" (filter: "file.txt"):\n---\nFile: {os.path.relpath(f, os.getcwd())}\nL1: hello world\nL2: hello pytest\n---'
    assert search_file_content.invoke({"pattern": "hello", "path": str(d), "include": "file.txt"}) == expected_output

def test_search_file_content_no_matches(tmp_path):
    d = tmp_path / "search_dir"
    d.mkdir()
    f = d / "file.txt"
    f.write_text("hello world")
    expected_output = f'No matches found for pattern "goodbye" in path "{d}" (filter: "file.txt").'
    assert search_file_content.invoke({"pattern": "goodbye", "path": str(d), "include": "file.txt"}) == expected_output

from agent.tools.file_system import list_directory, read_file, write_file, replace, search_file_content, glob
def test_search_file_content_non_existent_dir():
    expected_output = f"Error: Invalid parameters provided. Reason: Failed to access path stats for {os.path.join(os.getcwd(), 'non_existent_dir')}: Error: ENOENT: no such file or directory, stat '{os.path.join(os.getcwd(), 'non_existent_dir')}'"
    assert search_file_content.invoke({"pattern": "hello", "path": "non_existent_dir"}) == expected_output

def test_glob_with_matches(tmp_path):
    d = tmp_path / "glob_dir"
    d.mkdir()
    f1 = d / "file1.txt"
    f1.write_text("a")
    f2 = d / "file2.txt"
    f2.write_text("b")
    
    expected_header = f'Found 2 file(s) matching "*.txt" within {d}, sorted by modification time (newest first):\n'
    actual_output = glob.invoke({"pattern": "*.txt", "path": str(d)})
    assert actual_output.startswith(expected_header)
    assert str(f1) in actual_output
    assert str(f2) in actual_output

def test_glob_no_matches(tmp_path):
    d = tmp_path / "glob_dir"
    d.mkdir()
    expected_output = f'No files found matching pattern "*.pdf" within {os.path.join(os.getcwd(), str(d))}.'
    assert glob.invoke({"pattern": "*.pdf", "path": str(d)}) == expected_output

def test_glob_non_existent_dir():
    expected_output = f"Error: Invalid parameters provided. Reason: Search path does not exist {os.path.join(os.getcwd(), 'non_existent_dir')}"
    assert glob.invoke({"pattern": "*", "path": "non_existent_dir"}) == expected_output


