import os
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from langchain_core.tools import tool
from googleapiclient.discovery import build

@tool
def google_web_search(query: str) -> str:
    """
    Performs a web search using Google Search (via the Gemini API) and returns the results. This tool is useful for finding information on the internet based on a query.
    """
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        cse_id = os.getenv("GOOGLE_CSE_ID")
        if not api_key or not cse_id:
            return "Error: Google API key or CSE ID not found in environment variables."

        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=cse_id, num=5).execute()
        
        if "items" not in res:
            return f"No results found for '{query}'."

        snippets = [item["snippet"] for item in res["items"]]
        return f"Search results for '{query}':\n\n" + "\n\n".join(snippets)

    except Exception as e:
        return f"An unexpected error occurred during web search: {e}"

@tool
def web_fetch(prompt: str) -> str:
    """Processes content from URL(s), including local and private network addresses (e.g., localhost), embedded in a prompt. Include up to 20 URLs and instructions (e.g., summarize, extract specific data) directly in the 'prompt' parameter."""
    url_match = re.search(r'https?://\S+', prompt)
    if not url_match:
        return "Error: No URL found in the prompt."
    url = url_match.group(0)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=30000)
            html_content = page.content()
            browser.close()

        soup = BeautifulSoup(html_content, 'html.parser')
        main_content = soup.find('article') or soup.find('main') or soup.body

        for element in main_content(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()

        content_parts = []
        for element in main_content.find_all(['h1', 'h2', 'h3', 'p', 'li', 'a', 'table']):
            if element.name == 'a' and element.get('href'):
                text = element.get_text(strip=True)
                href = element.get('href')
                if not href.startswith('http'):
                    href = urljoin(url, href)
                if text:
                    content_parts.append(f"[{text}]({href})")
            elif element.name == 'table':
                table_md = ""
                for row in element.find_all('tr'):
                    cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                    table_md += "| " + " | ".join(cells) + " |\n"
                content_parts.append(table_md + '\n')
            else:
                content_parts.append(element.get_text(strip=True) + '\n')
        
        clean_text = re.sub(r'\n\s*\n', '\n\n', "".join(content_parts)).strip()
        return clean_text

    except Exception as e:
        return f"An unexpected error occurred: {e}"