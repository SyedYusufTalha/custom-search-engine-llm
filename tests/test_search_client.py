"""Unit tests for search_client.py, using mocked Tavily responses."""

from unittest.mock import MagicMock, patch

from src.search_engine.search_client import search


@patch("src.search_engine.search_client._client")
def test_search_returns_parsed_results(mock_client):
    mock_client.search.return_value = {
        "results": [
            {
                "title": "Example Title",
                "url": "https://example.com",
                "content": "Example snippet content.",
            }
        ]
    }

    results = search("test query")

    assert len(results) == 1
    assert results[0]["title"] == "Example Title"
    assert results[0]["link"] == "https://example.com"
    assert results[0]["snippet"] == "Example snippet content."


@patch("src.search_engine.search_client._client")
def test_search_returns_empty_list_when_no_results(mock_client):
    mock_client.search.return_value = {"results": []}

    results = search("no results query")

    assert results == []


@patch("src.search_engine.search_client._client")
def test_search_raises_runtime_error_on_api_failure(mock_client):
    mock_client.search.side_effect = Exception("API down")

    try:
        search("failing query")
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as exc:
        assert "Search request failed" in str(exc)