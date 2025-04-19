 # Google Sheets Interactive CLI Agent

 An interactive command-line agent that connects to Google Sheets and Notion via local MCP (Model Context Protocol) servers, enabling AI-powered data cleaning, analysis, and visualization.

 ## Overview

 This project demonstrates a multi-agent workflow using the **SmolAgents** framework and MCP connectors:
 - **Google Sheets MCP**: Interact with Google Sheets spreadsheets via a local server.
 - **Notion MCP**: (Optional) Read/write data to Notion databases via an MCP server.
 - **Sub-Agents**:
   - **Data Cleaning Agent**: Normalizes and prepares spreadsheet data.
   - **Study Agent**: Analyzes and interprets the cleaned data.
   - **Visualization Agent**: Generates charts (line, bar, scatter) from tabular data.
   - **Manager Agent**: Orchestrates tasks and dispatches to sub-agents.

 ## Features

 - Interactive REPL: Enter natural language tasks to process and visualize spreadsheet data.
 - Custom Tools: Define plotting tools with the `@tool` decorator (e.g., `plot_table`).
 - Automated Charting: Saves plots as `plot_<timestamp>.png` in the working directory.
 - Extensible: Add new MCP servers, tools, or sub-agents to fit your workflow.

 ## Prerequisites

 - Python 3.8+
 - Node.js 14+ and NPM
 - (Optional) Docker, for containerized MCP servers

 ## Installation

 1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/agents.git
    cd agents/09-google-sheets
    ```

 2. **Install Python dependencies**
    ```bash
    pip install smolagents pocketflow mcpadapt python-dotenv pandas matplotlib
    ```

 3. **Set up the Google Sheets MCP connector**
    Follow the instructions in `../mcp-servers/google-sheets-mcp/README.md` to:
    - Install dependencies (`npm install`)
    - Create Google OAuth credentials
    - Build (`npm run build`) and start the server (`npm run start`)

 4. **(Optional) Set up a local Notion MCP server**
    You can use the public MCP via NPM or run a local copy:
    ```bash
    cd notion-mcp-server
    npm install
    npm run build
    npm run start
    ```

 5. **Configure environment variables**
    Create a `.env` file in this directory with:
    ```bash
    NOTION_INTEGRATION_ID=your_notion_integration_token
    ```

 ## Usage

 Run the interactive CLI:
 ```bash
 python main.py
 ```

 In the CLI, enter natural language tasks such as:
 ```
 Load sheet "Survey Responses"
 Clean and normalize the data
 Plot table with x axis "Experience" and y axis "Volunteer Count" as a bar chart
 ```

 To exit:
 ```
 exit
 quit
 ```

 Generated charts are saved as `plot_<timestamp>.png` in this directory.

 ## Directory Structure

 ```text
 09-google-sheets/
 ├── main.py                 # Entry point for the REPL agent
 ├── *.png                   # Sample and generated chart images
 └── notion-mcp-server/      # (Optional) Local Notion MCP server project
 ```

 ## Customization

 - **Add Tools**: Decorate Python functions with `@tool` for new CLI commands.
 - **Extend Agents**: Modify or add `CodeAgent` definitions in `main.py`.
 - **Integrate MCP Servers**: Update MCP parameters for additional data sources.

 ## License

 This project is licensed under the MIT License. See the [root LICENSE](../LICENSE) for details.