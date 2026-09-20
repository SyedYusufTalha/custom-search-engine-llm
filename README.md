# Custom Search Engine with LLM

A command-line search engine that combines real-time web search with LLM-powered summarization. Instead of returning a raw list of links, this tool fetches relevant results via the Tavily Search API and uses Google's Gemini API to synthesize them into a clear, readable summary tailored to your query.

# Why this exists

Traditional search returns a page of links you have to sift through yourself. This project explores a simple pattern for building LLM-augmented search tools — retrieving fresh, real-world information and letting an LLM do the reading for you, rather than relying solely on a model's training data.

# How it works
Takes a user query via the command line
Retrieves relevant web results using the Tavily Search API
Passes those results to Gemini with a summarization/ranking prompt
Outputs a clean, LLM-generated summary of the most relevant information
# Tech stack
Python — core application logic
Tavily API — real-time web search
Google Gemini API — LLM summarization and ranking