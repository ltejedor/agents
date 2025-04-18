"""
Interactive CLI agent that uses the local Google Sheets MCP server
via standard I/O and dispatches spreadsheet commands.
"""
import os
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel, ToolCallingAgent
from mcp import StdioServerParameters
import re
from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
from smolagents.tools import tool
import matplotlib.pyplot as plt
import pandas as pd
import time

class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Ensure tool names are valid Python identifiers
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)
 
@tool
def plot_table(rows: list, x: str, y: str, plot_type: str = 'line', title: str = '') -> str:
    """
    Plot a chart from tabular data.

    Args:
        rows: List of rows, first row is header (column names).
        x: Column name for x-axis.
        y: Column name for y-axis.
        plot_type: 'line', 'bar', or 'scatter'.
        title: Optional chart title.

    Returns:
        Filename of the saved chart image.
    """
    df = pd.DataFrame(rows[1:], columns=rows[0])
    fig, ax = plt.subplots()
    if plot_type == 'line':
        df.plot(x=x, y=y, ax=ax)
    elif plot_type == 'bar':
        df.plot.bar(x=x, y=y, ax=ax)
    elif plot_type == 'scatter':
        df.plot.scatter(x=x, y=y, ax=ax)
    else:
        raise ValueError(f"Unsupported plot_type: {plot_type}")
    if title:
        ax.set_title(title)
    filename = f"plot_{int(time.time())}.png"
    fig.savefig(filename)
    plt.close(fig)
    return filename

def main():
    # Load environment variables (e.g., GSHEETS_OAUTH_PATH)
    try:
        load_dotenv()
    except NameError:
        # dotenv not installed or not needed
        pass

    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    # Set up the MCP server parameters for Google Sheets
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_dir = os.path.join(current_dir, "google-sheets-mcp")
    server_parameters = StdioServerParameters(
        command="node",
        args=["dist/index.js"],
        env=os.environ.copy(),
        cwd=mcp_dir,
    )

    # Configure Notion MCP server parameters
    notion_env = os.environ.copy()
    notion_env["OPENAPI_MCP_HEADERS"] = (
        '{"Authorization": "Bearer ' + os.getenv('NOTION_INTEGRATION_ID', '') + '", '
        '"Notion-Version": "2022-06-28"}'
    )
    notion_server_parameters = StdioServerParameters(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        env=notion_env,
    )

    # Build a multi-agent system: cleaner, study, visualization, plus manager
    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as gs_tool_collection, \
         MCPAdapt(notion_server_parameters, SafeNameAdapter()) as notion_tools:
        # Combine Google Sheets and Notion tools
        notion_tool_collection = ToolCollection(notion_tools)
        data_tools = [*gs_tool_collection.tools]

        # Sub-agent: data cleaning
        data_clean_agent = CodeAgent(
            tools=data_tools,
            model=model,
            name="data_clean_agent",
            description="Cleans and normalizes spreadsheet data",
            additional_authorized_imports=["json", "pandas", "numpy", "re", "datetime"],
            add_base_tools=False,
        )

        # Sub-agent: data analysis/study
        study_agent = CodeAgent(
            tools=data_tools,
            model=model,
            name="study_agent",
            description="Analyzes and interprets spreadsheet data",
            additional_authorized_imports=["json", "pandas", "numpy", ],
            add_base_tools=False,
        )

        # Sub-agent: visualization
        viz_agent = CodeAgent(
            tools=[plot_table],
            model=model,
            name="visualization_agent",
            additional_authorized_imports=["json", "pandas", "numpy", "matplotlib.pyplot"],
            description="Creates visualizations from cleaned data",
        )

        # Manager agent orchestrates the workflow
        manager_agent = CodeAgent(
            tools=[],
            model=model,
            managed_agents=[data_clean_agent, study_agent, viz_agent],
            additional_authorized_imports=["time", "pandas", "numpy"],
        )

        #print("Multi-agent system initialized. Sub-agents:", [ag.name for ag in manager_agent.managed_agents])
        # Interactive REPL via manager
        while True:
            task = input("\nEnter task (or 'exit' to quit): ")
            if task.lower() in ['exit', 'quit']:
                break
            try:
                result = manager_agent.run(task)
                print("\nManager response:\n", result)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    main()