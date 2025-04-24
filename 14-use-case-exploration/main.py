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
    # After reorganizing MCP servers, locate Google Sheets MCP under mcp-servers
    mcp_dir = os.path.abspath(
        os.path.join(current_dir, "..", "mcp-servers", "google-sheets-mcp")
    )
    server_parameters = StdioServerParameters(
        command="node",
        args=["dist/index.js"],
        env=os.environ.copy(),
        cwd=mcp_dir,
    )



    # Build a multi-agent system: cleaner, study, visualization, plus manager
    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as gs_tool_collection:
        data_tools = [*gs_tool_collection.tools]

        research_agent=CodeAgent(
            tools=data_tools,
            model=model,
            add_base_tools=True,
            name="research_agent",
            description="does competitor research to find similar products to what your manager requests"
        )

        persona_agent=CodeAgent(
            tools=[],
            model=model,
            add_base_tools=True,
            name="persona_agent",
            description="have deep knowledge and understanding of specific roles in niche indusries and their software"
        )

        # Manager agent orchestrates the workflow
        manager_agent = CodeAgent(
            tools=data_tools,
            model=model,
            add_base_tools=True,
            managed_agents=[research_agent, persona_agent],
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

