
"""
A minimal script to debug the exact output of the telegramify-markdown library.
This script does not connect to Telegram.
"""
from telegramify_markdown import markdownify

def main():
    """
    Defines a GFM string, runs it through the converter, and prints the raw output.
    """

    gfm_message = """
# This is a GFM message.

Here is a list:
- Item 1
- Item 2
"""

    print("--- Input GFM String ---")
    print(gfm_message)

    converted_message = markdownify(gfm_message)

    print("\n--- Output from markdownify() ---")
    print(converted_message)

if __name__ == "__main__":
    main()

