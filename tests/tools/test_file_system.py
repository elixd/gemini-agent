from unittest.mock import patch, mock_open

from agent.tools.file_system import list_directory, read_file, write_file


def test_list_directory_success():
    """
    Tests that list_directory returns a newline-separated list of files.
    """
    with patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = ["file1.txt", "file2.txt", "subdir"]

        result = list_directory.invoke({"path": "/fake/path"})

        assert result == "file1.txt\nfile2.txt\nsubdir"
        mock_listdir.assert_called_once_with("/fake/path")


def test_list_directory_not_found():
    """
    Tests that list_directory returns an error if the path does not exist.
    """
    with patch("os.listdir") as mock_listdir:
        mock_listdir.side_effect = FileNotFoundError

        result = list_directory.invoke({"path": "/non/existent/path"})

        assert "Error: Directory not found" in result


def test_read_file_success():
    """
    Tests that read_file returns the content of a file.
    """
    with patch("builtins.open", mock_open(read_data="file content")) as mock_file:
        result = read_file.invoke({"file_path": "/fake/file.txt"})

        assert result == "file content"
        mock_file.assert_called_once_with("/fake/file.txt", "r")


def test_read_file_not_found():
    """
    Tests that read_file returns an error if the file does not exist.
    """
    with patch("builtins.open", mock_open()) as mock_file:
        mock_file.side_effect = FileNotFoundError

        result = read_file.invoke({"file_path": "/non/existent/file.txt"})

        assert "Error: File not found" in result


def test_write_file_success():
    """
    Tests that write_file successfully writes to a file.
    """
    with patch("builtins.open", mock_open()) as mock_file:
        result = write_file.invoke(
            {"file_path": "/fake/file.txt", "content": "new content"}
        )

        assert "Successfully wrote" in result
        mock_file.assert_called_once_with("/fake/file.txt", "w")
        mock_file().write.assert_called_once_with("new content")

