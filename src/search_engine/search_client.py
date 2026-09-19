"""
Wraps calls to the Tavily Search API.
Keeps all search-provider-specific logic isolated here, so swapping
providers later only requires changes in this one file.
"""

import logging
from typing import TypedDict

from tavily import TavilyClient

from .config import config

logger = logging.getLogger(__name__)

_client = TavilyClient(api_key=config.TAVILY_API_KEY)


class SearchResult(TypedDict):
    title: str
    link: str
    snippet: str


def search(query: str, num_results: int = 5) -> list[SearchResult]:
    """
    Run a search query against Tavily.

    Args:
        query: The search query string.
        num_results: Number of results to fetch.

    Returns:
        A list of SearchResult dicts with title, link, and snippet.

    Raises:
        RuntimeError: If the API call fails for any reason.
    """
    try:
        response = _client.search(query=query, max_results=num_results)
    except Exception as exc:
        logger.error("Search API call failed for query %r: %s", query, exc)
        raise RuntimeError(f"Search request failed: {exc}") from exc

    results = response.get("results", [])
    if not results:
        logger.info("No search results found for query: %r", query)
        return []

    return [
        SearchResult(
            title=item.get("title", ""),
            link=item.get("url", ""),
            snippet=item.get("content", ""),
        )
        for item in results
    ]

if __name__ == "__main__":
    results = search("machine learning transformers")
    for r in results:
        print(r["title"], "-", r["link"])