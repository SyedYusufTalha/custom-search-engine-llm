"""
Handles command-line argument parsing and output formatting.
Keeps user-facing I/O separate from the core orchestration logic.
"""

import argparse


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the search engine CLI."""
    parser = argparse.ArgumentParser(
        description="A custom search engine with LLM-powered summarization."
    )
    parser.add_argument(
        "query",
        type=str,
        nargs="?",
        help="The search query. If omitted, you'll be prompted interactively.",
    )
    parser.add_argument(
        "--num-results",
        type=int,
        default=5,
        help="Number of search results to retrieve (default: 5).",
    )
    return parser.parse_args()


def get_query(args: argparse.Namespace) -> str:
    """Return the query from args, or prompt the user if not provided."""
    if args.query:
        return args.query
    return input("Enter your search query: ").strip()


def display_summary(query: str, summary: str) -> None:
    """Print the final summary in a readable format."""
    print(f"\n{'=' * 60}")
    print(f"Query: {query}")
    print(f"{'=' * 60}\n")
    print(summary)
    print()