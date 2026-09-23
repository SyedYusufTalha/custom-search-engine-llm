# 🔍 Custom Search Engine with LLM

A command-line search engine that combines real-time web search with LLM-powered summarization. Instead of returning a raw list of links, this tool fetches relevant results via the [Tavily Search API](https://tavily.com) and uses Google's Gemini API to synthesize them into a clear, readable summary tailored to your query.

## Why this exists

Traditional search returns a page of links you have to sift through yourself. This project explores a simple pattern for building **LLM-augmented search tools** — retrieving fresh, real-world information and letting an LLM do the reading for you, rather than relying solely on a model's training data.

## How it works

1. Takes a user query via the command line
2. Retrieves relevant web results using the Tavily Search API
3. Passes those results to Gemini with a summarization/ranking prompt
4. Outputs a clean, LLM-generated summary of the most relevant information, citing which source supports each point

## Tech stack

- **Python** — core application logic
- **Tavily API** — real-time web search
- **Google Gemini API** — LLM summarization and ranking
- **pytest** — unit testing with mocked API calls

## Installation

1. Clone the repo:
```bash
   git clone https://github.com/SyedYusufTalha/custom-search-engine-llm.git
   cd custom-search-engine-llm
```

2. Create a virtual environment and activate it:
```bash
   python -m venv venv
   venv\Scripts\activate       # Windows
   source venv/bin/activate    # macOS/Linux
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Set up your API keys:
   - Copy `.env.example` to `.env`
   - Get a free Tavily API key at [app.tavily.com](https://app.tavily.com)
   - Get a Gemini API key at [Google AI Studio](https://aistudio.google.com)
   - Fill in both values in `.env`

## Usage

Run with a query directly:
```bash
python -m src.search_engine.main "machine learning transformers"
```

Or run without a query for an interactive prompt:
```bash
python -m src.search_engine.main
```

Optionally control how many search results are used:
```bash
python -m src.search_engine.main "your query" --num-results 8
```

### Example output

Query: What is the transformer architecture?

The transformer is a neural network architecture introduced in the
2017 paper "Attention is All You Need" (Vaswani et al.)...
[LLM-generated summary continues, citing sources by title]


## Running tests

```bash
pip install -r requirements.txt
pytest
```

Tests mock all external API calls (Tavily and Gemini), so they run offline, instantly, and at no cost.

## Notes

- The Tavily free tier includes 1,000 API credits/month — plenty for personal use.
- Gemini API calls include automatic retry logic (3 attempts) to handle occasional transient server errors.