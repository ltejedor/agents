# Proof of Work LLM System

This repository demonstrates an LLM-driven development workflow using the `smolagents` library. An interactive agent in the `01/` folder generates a tool tracking system in the `02/` folder, and all agent actions are recorded as proof-of-work logs.

## Repository Structure

- `01/` Agent Orchestrator
  - `main.py`: Interactive LLM agent that generates code files based on user prompts.
  - `proof_of_work.py`: Utilities to extract and save all tool call steps to JSON.
  - `output/`: Proof-of-work logs (`*.json`) recording every agent tool call and file operation.
- `02/` Generated Tool Tracking System
  - `README.md`: Overview of the generated system.
  - `tool_tracker.py`: Middleware to intercept and log LLM tool calls.
  - `data_store.py`: Persistent storage for recorded tool calls.
  - `visualization.py`: Data visualization and export utilities (time series, execution times, success rates).
  - `api.py`: Simple programmatic interface for configuration and dashboard data retrieval.
  - `example_usage.py`: Example script demonstrating how to use the generated system.
- `smolagents-ref/`: Reference implementation, docs, and examples for the `smolagents` library.

## Getting Started

### Prerequisites
- Python 3.8 or newer
- pip

### Installation
Install required Python packages:
```bash
pip install smolagents requests python-dotenv markdownify
```
> Optionally, install additional libs for visualization in `02/`:
> ```bash
> pip install pandas plotly
> ```

Create a `.env` file in `01/` (if using hosted LLMs) to set API keys:
```dotenv
ANTHROPIC_API_KEY=your_anthropic_api_key
# OPENAI_API_KEY=your_openai_api_key
```

### Running the Agent
```bash
cd 01
python main.py
```
Enter tasks at the prompt; when you exit, a proof-of-work JSON will be saved in `01/output/`.

### Exploring the Generated System
After running the agent, navigate to the `02/` folder (the generated output) and run:
```bash
python example_usage.py
```
This will execute example tools with tracking enabled and print usage statistics.

## Proof of Work
All agent actions—tool invocations and file creations—are logged in the JSON files under `01/output/`. Inspect these logs to verify how the system was built step by step.
