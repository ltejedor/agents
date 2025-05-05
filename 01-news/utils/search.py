import re
from typing import List, Any

def is_valid_url(url: str) -> bool:
    # A simple regex to match http(s) URLs.
    regex = re.compile(
        r'^(?:http|https)://'
        r'\w+(?:\.\w+)+'
    )
    return re.match(regex, url) is not None

def search_web(query: str, max_results: int = 10, raw: bool = False) -> Any:
    """
    Perform a DuckDuckGo web search.
    
    Args:
        query (str): The search query to perform.
        max_results (int): Maximum number of search results (default: 10).
        raw (bool): If True, return the raw search results (list of dicts);
                    otherwise, return a list of validated URLs.
    
    Returns:
        Any: A list of raw result dictionaries if raw is True;
             otherwise, a list of URLs (strings).
    
    Raises:
        ImportError: If duckduckgo_search is not installed.
        Exception: If no results are found.
    """
    try:
        from duckduckgo_search import DDGS
    except ImportError as e:
        raise ImportError(
            "You must install the `duckduckgo_search` package to run this tool. "
            "Try installing it with `pip install duckduckgo-search`."
        ) from e

    ddgs = DDGS()
    results = ddgs.text(query, max_results=max_results)
    if not results:
        raise Exception("No results found! Try a less restrictive query.")
    if raw:
        return results
    # Otherwise, extract and validate URLs.
    urls = [result.get("href", "") for result in results if result.get("href", "")]
    valid_urls = [url for url in urls if is_valid_url(url)]
    return valid_urls

if __name__ == "__main__":
    query = "startup competitors"
    print("Raw search results:")
    print(search_web(query, raw=True))
    print("Filtered URLs:")
    print(search_web(query, raw=False))
