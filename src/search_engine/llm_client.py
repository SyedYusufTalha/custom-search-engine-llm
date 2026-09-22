"""
Wraps calls to the Gemini API (via the current google-genai SDK) to
summarize and synthesize search results into a readable answer.
"""

import logging

from google import genai

from .config import config
from .search_client import SearchResult

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=config.GEMINI_API_KEY)

_MODEL = "gemini-3.6-flash"  # fast + cheap, good fit for summarization tasks


def _build_prompt(query: str, results: list[SearchResult]) -> str:
    """Format search results into a prompt for Gemini to synthesize."""
    formatted_results = "\n\n".join(
        f"Title: {r['title']}\nSnippet: {r['snippet']}\nLink: {r['link']}"
        for r in results
    )
    return (
        f"You are a research assistant. A user searched for: \"{query}\"\n\n"
        f"Here are the top search results:\n\n{formatted_results}\n\n"
        "Using only the information above, write a clear, concise summary "
        "that directly answers the user's query. Mention which source "
        "(by title) supports each key point. If the results don't fully "
        "answer the query, say so explicitly rather than guessing."
    )


def summarize(query: str, results: list[SearchResult]) -> str:
    """
    Send search results to Gemini and return a synthesized summary.

    Args:
        query: The user's original search query.
        results: Search results from search_client.search().

    Returns:
        A summarized answer string.

    Raises:
        RuntimeError: If the LLM API call fails for any reason.
    """
    if not results:
        return "No search results were found for this query."

    prompt = _build_prompt(query, results)

    try:
        response = _client.models.generate_content(
            model=_MODEL,
            contents=prompt,
        )
    except Exception as exc:
        logger.error("Gemini API call failed for query %r: %s", query, exc)
        raise RuntimeError(f"LLM summarization failed: {exc}") from exc

    return response.text

if __name__ == "__main__":
    from .search_client import search

    query = "machine learning transformers"
    results = search(query)
    print(summarize(query, results))