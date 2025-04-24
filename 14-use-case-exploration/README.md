# Use Case Exploration Agent

A multi-agent system for exploring and researching software use cases across different industries. This tool leverages Claude 3.7 Sonnet and Google Sheets integration to help product teams understand potential applications and competitors for new software products.

## Overview

This project creates an interactive agent system that can:
- Research competitors and similar products in various markets
- Provide deep knowledge about specific roles and industries
- Analyze use cases for software products
- Store and organize findings in Google Sheets

The system uses a manager-worker architecture with specialized agents that collaborate to provide comprehensive insights about potential software applications.

## Features

- Multi-agent architecture with specialized roles:
  - Research Agent: Finds and analyzes similar products and competitors
  - Persona Agent: Provides deep knowledge about specific roles and industries
  - Manager Agent: Orchestrates the workflow and integrates findings
- Google Sheets integration for data storage and analysis
- Interactive command-line interface for natural language queries
- Comprehensive research capabilities across industries and use cases

## Prerequisites

- Python 3.8+
- Node.js and npm (for Google Sheets MCP server)
- Google Cloud Platform account with OAuth credentials
- API keys for Anthropic Claude

## Installation

1. Clone this repository
```bash
git clone https://github.com/ltejedor/agents.git
cd agents/14-use-case-exploration
```

2. Install Python dependencies
```bash
pip install -r ../requirements.txt
```

3. Set up the Google Sheets MCP server
   The local MCP server is included under `mcp-servers/google-sheets-mcp` at the project root.
   ```bash
   cd ../mcp-servers/google-sheets-mcp
   npm install
   npm run build
   ```

4. Configure Google Sheets OAuth
   - Create OAuth credentials in Google Cloud Console
   - Download the credentials JSON file
   - Set the path to this file in your environment variables:
   ```
   GSHEETS_OAUTH_PATH=/path/to/your/credentials.json
   ```

5. Create a `.env` file in the project root with your API keys
```
ANTHROPIC_API_KEY=your_anthropic_key_here
```

## Usage

Run the main script:
```bash
python main.py
```

Once running, you'll see a prompt where you can enter natural language commands:
```
Enter task (or 'exit' to quit): 
```

### Example Commands

- "Research project management software for construction companies"
- "What software do financial analysts use for data visualization?"
- "Find competitors to Salesforce in the healthcare industry"
- "What are the key features needed for HR software in manufacturing?"
- "Create a spreadsheet comparing top CRM solutions for small businesses"

Enter 'exit' or 'quit' to close the application.

## How It Works

This tool uses a multi-agent system with three specialized components:

1. **Research Agent**: Focuses on finding and analyzing similar products and competitors in the market. It can search for information, analyze trends, and identify key players in specific industries.

2. **Persona Agent**: Provides deep knowledge about specific roles and industries. It understands the workflows, pain points, and software needs of different professional personas.

3. **Manager Agent**: Orchestrates the workflow between the specialized agents, integrates their findings, and presents a cohesive response to the user's query.

The system leverages Google Sheets for data storage and analysis, allowing it to create structured comparisons and maintain persistent records of its findings.

## Architecture

The application is built on several key technologies:

- **smolagents**: Framework for creating AI agents with tool-using capabilities
- **LiteLLM**: To interact with the Claude 3.7 Sonnet model
- **MCP (Machine-Comprehensible Protocol)**: A protocol for AI agents to interact with external tools
- **Google Sheets MCP Server**: Provides MCP-compatible tools for interacting with Google Sheets

The `SafeNameAdapter` class ensures that tool names from the Google Sheets API are compatible with the agent's requirements.

## Troubleshooting

- If you encounter authentication issues with Google Sheets, ensure your OAuth credentials are correctly set up and the GSHEETS_OAUTH_PATH environment variable points to the right file
- For connection issues with the MCP server, verify that the Google Sheets MCP server is properly built and accessible
- If agents fail to respond appropriately, check that your Anthropic API key is valid and properly set in the environment variables
