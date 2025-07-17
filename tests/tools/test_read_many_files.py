import os
import pytest
from agent.tools.file_system import read_many_files

def test_read_many_files_multiple(tmp_path):
    d = tmp_path / "read_many"
    d.mkdir()
    f1 = d / "file1.txt"
    f1.write_text("content1")
    f2 = d / "file2.log"
    f2.write_text("content2")
    
    # Use explicit paths to guarantee order for the assertion
    paths_to_read = [str(f1), str(f2)]
    expected_output = f"--- {f1} ---\n\ncontent1\n\n--- {f2} ---\n\ncontent2"
    result = read_many_files.invoke({"paths": paths_to_read})
    assert repr(result) == repr(expected_output)

def test_read_many_files_single(tmp_path):
    f = tmp_path / "file1.txt"
    f.write_text("content1")
    
    expected_output = f"--- {f} ---\n\ncontent1"
    result = read_many_files.invoke({"paths": [str(f)]})
    assert repr(result) == repr(expected_output)

def test_read_many_files_no_match(tmp_path):
    d = tmp_path / "read_many"
    d.mkdir()
    assert read_many_files.invoke({"paths": [str(d / "*.pdf")]}) == "No files matching the criteria were found or all were skipped."

def test_read_many_files_with_exclude(tmp_path):
    d = tmp_path / "read_many"
    d.mkdir()
    f1 = d / "file1.txt"
    f1.write_text("content1")
    f2 = d / "file2.log"
    f2.write_text("content2")
    
    expected_output = f"--- {f1} ---\n\ncontent1"
    result = read_many_files.invoke({"paths": [str(d / "*")], "exclude": ["**/*.log"]})
    assert repr(result) == repr(expected_output)