# ArXiv AI Policy Paper Collector

This tool automatically discovers, filters, and stores research papers from arXiv related to AI policy, with a focus on energy policy across governments. Its primary goal is to collect potential research and data in a centralized location where a human team can evaluate alignment or unalignment with specific policy objectives.

## Overview

This script uses the arXiv API to search for papers on specified topics, processes them to identify relevant content, and stores qualifying papers in a Supabase database for human review. The core purpose is to create a repository of research that human teams can analyze to determine alignment or unalignment with specific policy perspectives and objectives.

## How It Was Built

This tool was built by combining several key technologies:

1. **arXiv API Integration**: The script interfaces directly with arXiv's public API to query and retrieve academic papers, allowing access to a vast repository of cutting-edge research without needing to scrape websites.

2. **SmolaAgents Framework**: The intelligent filtering is powered by SmolaAgents, a lightweight agent framework that enables the creation of autonomous workflows. This allows the script to make nuanced judgments about paper relevance that go beyond simple keyword matching.

3. **LLM-Powered Analysis**: By leveraging Claude through LiteLLM, the script can understand complex relationships between AI policy and energy governance, identifying relevant papers even when the connection isn't explicitly stated.

4. **Supabase Integration**: Qualifying papers are stored in a Supabase database, creating a persistent, queryable collection that human teams can access and analyze.

## Features

- Search arXiv for papers based on keywords and topics
- Process papers individually to evaluate their relevance
- Optional integration with Supabase for persistent storage
- Intelligent filtering using LLM-based agents
- Detailed reporting of discovered papers and trends
- Support for visiting linked web pages and extracting content

## Requirements

- Python 3.8+
- Dependencies:
  - `smolagents` - For creating the agent-based workflow
  - `requests` - For making HTTP requests to arXiv
  - `python-dotenv` - For environment variable management
  - `supabase-py` - For Supabase database integration (if using the database feature)
  - `markdownify` - For converting HTML to markdown
  - `litellm` - For LLM model integration with Claude

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd arxiv-ai-policy-collector
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys (if using Supabase):
```
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-supabase-service-key
ANTHROPIC_API_KEY=your-anthropic-api-key
```

## Usage

1. Modify the `user_goal` variable in the `main()` function to specify your research focus:
```python
user_goal = "I want to find recent papers on AI policy as it relates to energy policy across governments."
```

2. Toggle the `include_db_push` variable to enable or disable Supabase integration:
```python
include_db_push = True  # Set to False if you don't want to store papers in a database
```

3. Run the script:
```bash
python arxiv_collector.py
```

## How It Works

The script follows this workflow:

1. Initializes an agent with tools for searching arXiv, parsing papers, visiting webpages, and pushing to Supabase
2. Fetches papers from arXiv based on the specified topic
3. Processes each paper sequentially:
   - Parses the paper's metadata (title, summary, publication date, URL)
   - Evaluates if the paper meets the specified criteria using LLM-powered analysis
   - If relevant, stores the paper in Supabase for human review
4. Provides a summary report with:
   - Total papers reviewed
   - Number of qualifying papers found
   - Trends observed in the research
   
The key innovation is using SmolaAgents to create an intelligent workflow that can understand nuanced relationships between AI policy and other domains. Rather than relying on rigid keyword filtering, the agent can recognize relevant papers even when connections are implicit or require domain knowledge to identify.

## Purpose: Supporting Human Alignment Analysis

The primary goal of this tool is to build a collection of research that human experts can review to:

1. Identify alignment or unalignment with specific policy objectives
2. Track emerging trends in AI policy related to energy governance
3. Support evidence-based policy development with current research
4. Facilitate comparative analysis across different governmental approaches

By automating the collection and initial filtering, the tool allows human experts to focus their time on deeper analysis and synthesis rather than literature discovery.

## Database Schema

If using Supabase, the script expects a table named `policy_papers` with the following structure:

| Column Name     | Data Type      | Description                           |
|----------------|----------------|---------------------------------------|
| id             | uuid           | Primary key                           |
| paper_name     | text           | Title of the paper                    |
| url            | text           | URL to the paper                      |
| summary        | text           | Summary of the paper                  |
| published_date | timestamptz    | Publication date of the paper         |
| created_at     | timestamptz    | When the record was created           |

## Customization

- To use a different LLM model, modify the model initialization in `main()`:
```python
# For example, to use a local model or different API
model = HfApiModel()  # For Hugging Face models
# Or
model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")  # For Claude
```

- To change the maximum number of processing steps, modify:
```python
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=["time", "numpy", "pandas", "json"],
    max_steps=100  # Increase for more processing steps
)
```
