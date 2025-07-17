# Remaining Tool Behavior Documentation

This document outlines the behavior of the `save_memory`, `google_web_search`, `web_fetch`, and `read_many_files` tools.

## `save_memory`

### Scenario 1: Save a new fact

**Tool Call:**
```json
{
  "tool_name": "save_memory",
  "parameters": {
    "fact": "The user's favorite color is blue."
  }
}
```

**Output:**
```json
{"success":true,"message":"Okay, I've remembered that: \"The user's favorite color is blue.\""}
```

### Scenario 2: Save an existing fact

**Tool Call:**
```json
{
  "tool_name": "save_memory",
  "parameters": {
    "fact": "The user's favorite color is blue."
  }
}
```

**Output:**
```json
{"success":true,"message":"Okay, I've remembered that: \"The user's favorite color is blue.\""}
```

### Scenario 3: Save an empty fact

**Tool Call:**
```json
{
  "tool_name": "save_memory",
  "parameters": {
    "fact": ""
  }
}
```

**Output:**
```json
{"success":false,"error":"Parameter \"fact\" must be a non-empty string."}
```

## `google_web_search`

### Scenario 1: Standard search query

**Tool Call:**
```json
{
  "tool_name": "google_web_search",
  "parameters": {
    "query": "What is the capital of France?"
  }
}
```

**Output:**
```
Web search results for "What is the capital of France?":

The capital of France is Paris.[1][2][3] Situated on the Seine River in the northern part of the country, Paris is the nation's most populous city.[1]

Known by nicknames such as the "City of Light" and the "City of Love," Paris is a global center for art, fashion, culture, and gastronomy.[4][3] It is home to iconic landmarks and has a rich history dating back over 2,000 years.[2][4] While Paris has been the capital for most of its history, other cities like Versailles and Tours have temporarily held the title.[2][5]

Sources:
[1] coe.int (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGnPtq5NkltmiA5tzQqn27nrnOmStN2kdQ13WlZqUwIei0Cggyu32A26hy0x__b2oiBX_pTke61R7EP-Q9xOoUyxb00vMjrpHV9K3ATjlGzEefWFB3z1UqoQ9u9Fo3FAyWVzViz4xZp5BS2nLHkdi8=)
[2] adelphi.edu (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHsEG1P7u5yQb7M7O0Q1CBJ8KW_SmX4Q9lpD6Kkf8uqhbFewJiXYe50zqxyAwXaTLWXvv6di14PlhF6egbDVYARUtILGdMEtxHILwIx8fUQYUifH66d3W_4Q15J5rNeKv5HfWUaEGYWbEul)
[3] mappr.co (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFHxbfNysjWGMtmUlMb6mBdZGOl91AGDowiF-xWsKOgfhi8QNlV2foRdj0EMMp5Eq7wjgSibPrMrkf-wKoM9axb_y03DdjWB9oiwNorzGFFqcnpjojaYyEFQANEVOU1201PfLRSohk=)
[4] iroamly.com (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFaXHoh1bPq-1Yzp_8qlST5Ry7SETgdtwj_iIDzz3Y2DVLYaUG5p3_7Wnq_4QLb9cpb4Ms3vaBwQiFkFaHkK3dIlqrDWeRSiVwPX-oD0fg_h_thVPOlQr3tzsT7HnxtJIZOXsQf6cmKuIpX4uqzkyLFP7XZ8o5oiQtgFTuZG9ESMlGv-w==)
[5] wikipedia.org (https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGW-dE7dqBz9VVK_KR6hXgq2JZsJHM9NDIG4Cjm2FH_07lZeS6OWMzj62XmSYJtcEAkrNnsJ7iQpzGLCDmRu88FpdmukJJi9_lh7v2-p1M46Gc2L4lb4OKorSHqV_tlMeAUeTEO-oJiYJuK6veo6pHXrtsa)
```

### Scenario 2: Query with no results

**Tool Call:**
```json
{
  "tool_name": "google_web_search",
  "parameters": {
    "query": "asdfqwertylkjhgfdsazxcvbnm"
  }
}
```

**Output:**
```
Web search results for "asdfqwertylkjhgfdsazxcvbnm":

I'm sorry, I don't understand that. How can I help you?
```

### Scenario 3: Empty query

**Tool Call:**
```json
{
  "tool_name": "google_web_search",
  "parameters": {
    "query": ""
  }
}
```

**Output:**
```
Web search results for "":

I will start by running `git diff` to review the changes. Then, I will stage, and commit them. After that, I will push the changes to the remote repository. Bfore I do so, what is the remote repository URL?
```

## `web_fetch`

### Scenario 1: Fetch a valid URL

**Tool Call:**
```json
{
  "tool_name": "web_fetch",
  "parameters": {
    "prompt": "Please summarize the content of https://gemini.google.com/"
  }
}
```

**Output:**
```
Based on the content provided, the page is for "Google Gemini" and includes a "Sign in" link.
```

### Scenario 2: Fetch an invalid URL

**Tool Call:**
```json
{
  "tool_name": "web_fetch",
  "parameters": {
    "prompt": "Please fetch https://this-is-not-a-real-domain-12345.com"
  }
}
```

**Output:**
```
I was unable to fetch the content from the provided URL, as it appears to be an invalid address. Please provide a valid URL.
```

### Scenario 3: Fetch a non-HTML resource (PDF)

**Tool Call:**
```json
{
  "tool_name": "web_fetch",
  "parameters": {
    "prompt": "Can you get the text from this PDF? https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
  }
}
```

**Output:**
```
I will save the provided content to a temporary PDF file and then attempt to extract the text from it.I will save the provided content to a temporary PDF file and then attempt to extract the text from it.
A new file, `/tmp/dummy.pdf`, will be created with the provided content.
I will then run `pdftotext /tmp/dummy.pdf -` to extract text from the newly created file.
Finally, I will run `rm /tmp/dummy.pdf` to remove the temporary file.
Okay, proceeding with the plan. I will first save the content to a temporary file.
A new file, `/tmp/dummy.pdf`, will be created with the provided content.
I will then run `pdftotext /tmp/dummy.pdf -` to extract text from the newly created file.
Finally, I will run `rm /tmp/dummy.pdf` to remove the temporary file.
File created. Now, I will attempt to extract the text.
I will then run `pdftotext /tmp/dummy.pdf -` to extract text from the newly created file.
Finally, I will run `rm /tmp/dummy.pdf` to remove the temporary file.
Dummy PDF file
I will now remove the temporary file.
I will then run `rm /tmp/dummy.pdf` to remove the temporary file.
I have extracted the text from the PDF and cleaned up the temporary file.
```

## `read_many_files`

### Scenario 1: Read multiple existing files

**Tool Call:**
```json
{
  "tool_name": "read_many_files",
  "parameters": {
    "paths": [
      "read_many_test_dir/*.txt",
      "read_many_test_dir/*.log"
    ]
  }
}
```

**Output:**
```
--- read_many_test_dir/file1.txt ---

content1


--- read_many_test_dir/file2.log ---

content2


```

### Scenario 2: Read a single file

**Tool Call:**
```json
{
  "tool_name": "read_many_files",
  "parameters": {
    "paths": [
      "read_many_test_dir/file1.txt"
    ]
  }
}
```

**Output:**
```
--- read_many_test_dir/file1.txt ---

content1


```

### Scenario 3: Read non-existent file pattern

**Tool Call:**
```json
{
  "tool_name": "read_many_files",
  "parameters": {
    "paths": [
      "read_many_test_dir/*.pdf"
    ]
  }
}
```

**Output:**
```
No files matching the criteria were found or all were skipped.
```

### Scenario 4: Read with exclusion

**Tool Call:**
```json
{
  "tool_name": "read_many_files",
  "parameters": {
    "paths": [
      "read_many_test_dir/*"
    ],
    "exclude": [
      "**/*.log"
    ]
  }
}
```

**Output:**
```
--- read_many_test_dir/file1.txt ---

content1


--- read_many_test_dir/file3.md ---

content3


```