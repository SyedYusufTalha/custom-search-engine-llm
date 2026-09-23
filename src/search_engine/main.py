"""
Entry point for the custom search engine.
Orchestrates: config validation -> search -> summarize -> display.
"""

import logging
import sys

from .cli import display_summary, get_query, parse_args
from .config import config
from .llm_client import summarize
from .search_client import search

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def run() -> None:
    """Run the full search + summarize pipeline."""
    try:
        config.validate()
    except EnvironmentError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    args = parse_args()
    query = get_query(args)

    if not query:
        print("No query provided. Exiting.", file=sys.stderr)
        sys.exit(1)

    try:
        results = search(query, num_results=args.num_results)
        summary = summarize(query, results)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    display_summary(query, summary)


if __name__ == "__main__":
    run()