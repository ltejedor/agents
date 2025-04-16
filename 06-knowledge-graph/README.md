# Knowledge Graph Project README

## Overview

This project creates an interactive knowledge graph visualization from RSS feeds. It extracts entities and relationships from news articles using NLP and LLM-based techniques, then visualizes the connections in an interactive graph.

## Features

- Fetches and aggregates content from multiple RSS news feeds
- Processes text using LLM-based knowledge extraction
- Builds a directed graph of entities and their relationships
- Provides an interactive visualization using Plotly
- Allows selection of specific news sources

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the required spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the Gradio interface:
```bash
python interface.py
```

The interface allows you to:
1. Select which news sources to include
2. Generate a knowledge graph from the selected sources
3. View the aggregated feed content and interactive graph visualization

## Project Structure

- `interface.py`: Main Gradio application with the UI and visualization logic
- `fetch.py`: Functions for retrieving and parsing RSS feeds
- `sources.py`: List of available RSS feed URLs
- `requirements.txt`: Required Python packages
- `tutorials/`: Example notebooks showing the knowledge graph extraction process

## How It Works

1. The application fetches recent articles from selected RSS feeds
2. Content is processed and split into manageable chunks
3. An LLM (GPT-4o) extracts entities and relationships from the text
4. A directed graph is constructed from these relationships
5. The graph is visualized using Plotly with interactive features

## Dependencies

- spaCy: For NLP processing
- Gradio: For the web interface
- NetworkX: For graph data structures
- Plotly: For interactive visualizations
- LangChain: For LLM-based graph transformations
- OpenAI API: Powers the LLM graph transformer

## Acknowledgements

This project was inspired by techniques from:
- [Analytics Vidhya: How to Build Knowledge Graph from Text using spaCy](https://www.analyticsvidhya.com/blog/2019/10/how-to-build-knowledge-graph-text-using-spacy/)
- [DataCamp: Knowledge Graph RAG Tutorial](https://www.datacamp.com/tutorial/knowledge-graph-rag)

## Part of 30 Agents in 30 Days

This project is #6 in the **30 Agents in 30 Days** series, which provides practical AI agent workflows for different stages of product development including research, development, testing, marketing, and sales.