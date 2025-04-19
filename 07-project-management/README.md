# Notion Project Management Agent

A command-line tool that enables AI-powered project management using Notion as a backend. This tool leverages Claude 3.7 Sonnet and the Notion API to help you manage projects through natural language commands.

## Overview

This project creates an interactive agent that can:
- Connect to your Notion workspace via the Notion API
- Process natural language commands and queries
- Perform actions in your Notion workspace through an AI agent

The agent runs locally on your machine and maintains a continuous conversation, allowing you to manage your projects efficiently through simple text commands.

## Prerequisites

- Node.js and npm installed
- Python 3.8+ installed
- A Notion integration with appropriate permissions
- API keys for Anthropic Claude

## Installation

1. Clone this repository
```bash
git clone https://github.com/ltejedor/agents.git
cd agents/07-project-management
```

2. Install Python dependencies
```bash
pip install smolagents litellm mcp anthropic python-dotenv mcpadapt
```

3. Set up the Notion MCP server
   The local MCP server is included under `mcp-servers/notion-mcp-server` at the project root.
   ```bash
   cd ../mcp-servers/notion-mcp-server
   npm install
   npm run build
   npm run start
   ```

4. Create a `.env` file in the project root with your API keys
```
ANTHROPIC_API_KEY=your_anthropic_key_here
NOTION_INTEGRATION_ID=your_notion_integration_token_here
```

## Notion Integration Setup

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the "Internal Integration Token"
4. Add this token to your `.env` file as `NOTION_INTEGRATION_ID`
5. Share the Notion pages/databases you want to manage with your integration

Detailed instructions for setting up a Notion integration can be found at: [https://github.com/makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server)

## Usage

Run the main script:
```bash
python main.py
```

Once running, you'll see a prompt where you can enter natural language commands:
```
Notion Agent initialized!
Available tools: [list of available tools]

Enter your command (or 'exit' to quit): 
```

### Example Commands

- "Create a new task called 'Research competitors' with a high priority"
- "Show me all tasks due this week"
- "Update the status of 'Design mockups' to 'Completed'"
- "List all projects in my workspace"
- "Add a comment to the 'Marketing campaign' task"

Enter 'exit' or 'quit' to close the application.

## How It Works

This tool uses:
- **smolagents**: Framework for creating AI agents with tool-using capabilities
- **LiteLLM**: To interact with the Claude 3.7 Sonnet model
- **MCP (Machine-Comprehensible Protocol)**: A protocol for AI agents to interact with external tools
- **notion-mcp-server**: Provides MCP-compatible tools for interacting with Notion

The `SafeNameAdapter` class ensures that tool names from the Notion API are compatible with the agent's requirements.

## Troubleshooting

- Ensure your Notion integration has been properly shared with the pages you want to access
- Check that all environment variables are correctly set in your `.env` file
- If you encounter permission errors, verify that your Notion integration has the necessary capabilities enabled
- For connection issues, ensure you have a stable internet connection and that the Notion API is operational

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

