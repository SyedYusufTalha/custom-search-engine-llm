"""
Wraps calls to the Gemini API (via the current google-genai SDK) to
summarize and synthesize search results into a readable answer.
"""

import logging
import time
from google import genai

from .config import config
from .search_client import SearchResult

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=config.GEMINI_API_KEY)

_MODEL = "gemini-3.6-flash"  # fast + cheap, good fit for summarization tasks
_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 5

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

    last_exc = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            response = _client.models.generate_content(
                model=_MODEL,
                contents=prompt,
            )
            return response.text
        except Exception as exc:
            last_exc = exc
            logger.warning(
                "Gemini API call attempt %d/%d failed for query %r: %s",
                attempt, _MAX_RETRIES, query, exc,
            )
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY_SECONDS)

    logger.error("Gemini API call failed after %d attempts for query %r: %s",
                 _MAX_RETRIES, query, last_exc)
    raise RuntimeError(f"LLM summarization failed after {_MAX_RETRIES} attempts: {last_exc}") from last_exc