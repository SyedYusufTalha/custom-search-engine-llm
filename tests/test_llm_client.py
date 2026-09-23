"""Unit tests for llm_client.py, using mocked Gemini responses."""

from unittest.mock import MagicMock, patch
import time
from src.search_engine.llm_client import summarize
from src.search_engine.search_client import SearchResult


def _sample_results() -> list[SearchResult]:
    return [
        SearchResult(
            title="Example Title",
            link="https://example.com",
            snippet="Example snippet content.",
        )
    ]


def test_summarize_returns_message_when_no_results():
    result = summarize("empty query", [])
    assert result == "No search results were found for this query."


@patch("src.search_engine.llm_client._client")
def test_summarize_returns_gemini_response_text(mock_client):
    mock_response = MagicMock()
    mock_response.text = "This is a summary."
    mock_client.models.generate_content.return_value = mock_response

    result = summarize("test query", _sample_results())

    assert result == "This is a summary."


@patch("src.search_engine.llm_client._client")
@patch("src.search_engine.llm_client.time.sleep", return_value=None)
def test_summarize_raises_after_max_retries(mock_sleep, mock_client):
    mock_client.models.generate_content.side_effect = Exception("API down")

    try:
        summarize("failing query", _sample_results())
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as exc:
        assert "LLM summarization failed after" in str(exc)

    assert mock_client.models.generate_content.call_count == 3