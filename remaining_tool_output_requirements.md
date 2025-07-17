# Remaining Tool Output Requirements

This document specifies the exact output requirements for the `save_memory`, `google_web_search`, `web_fetch`, and `read_many_files` tools.

## `save_memory`

### Requirements

1.  **Successful Save:** When a new fact is saved, the tool must return a JSON object with the following structure: `{"success":true,"message":"Okay, I've remembered that: \"{fact}\""}`.
2.  **Duplicate Fact:** When attempting to save a duplicate fact, the tool should return the same success message as a new fact.
3.  **Empty Fact:** If the `fact` parameter is an empty string, the tool must return a JSON object with the following structure: `{"success":false,"error":"Parameter \"fact\" must be a non-empty string."}`.

## `google_web_search`

### Requirements

1.  **Successful Search:** For a successful search, the tool must return a string starting with `Web search results for "{query}":\n\n` followed by the search results.
2.  **No Results:** If no results are found, the tool should return a user-friendly message indicating that it could not find any information.
3.  **Empty Query:** If the `query` parameter is an empty string, the tool should return a user-friendly message asking for clarification.

## `web_fetch`

### Requirements

1.  **Successful Fetch:** For a successful fetch of an HTML page, the tool must return a string containing the cleaned and summarized text content of the page.
2.  **Invalid URL:** If the URL is invalid or cannot be reached, the tool must return the exact string: `I was unable to fetch the content from the provided URL, as it appears to be an invalid address. Please provide a valid URL.`
3.  **Non-HTML Resource:** If the URL points to a non-HTML resource like a PDF, the tool should attempt to extract the text content and return it as a string. The output should indicate the steps taken to extract the text.

## `read_many_files`

### Requirements

1.  **Successful Read:** When one or more files are read, the tool must return a string with the content of each file, separated by `--- {file_path} ---\n\n`.
2.  **No Files Found:** If no files are found that match the provided patterns, the tool must return the exact string: `No files matching the criteria were found or all were skipped.`
3.  **Exclusion:** When using the `exclude` parameter, the output should be a successful read, but without the excluded files.

