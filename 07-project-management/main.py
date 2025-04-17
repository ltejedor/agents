import os
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from mcp import StdioServerParameters
from anthropic import Anthropic
from dotenv import load_dotenv
import os
from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter
import re

load_dotenv()



class SafeNameAdapter(SmolAgentsAdapter):
    def adapt(self, func, tool):
        # Replace any non-identifier characters with underscores
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)


def main():
    # Initialize the model for Claude
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")
    
    # Create environment variables with your Notion integration secret
    notion_env = os.environ.copy()
    notion_env["OPENAPI_MCP_HEADERS"] = '{"Authorization": "Bearer ' + os.getenv('NOTION_INTEGRATION_ID') + '", "Notion-Version": "2022-06-28"}'
    
    # Set up the MCP server parameters for Notion
    server_parameters = StdioServerParameters(
        command="npx",
        args=["-y", "@notionhq/notion-mcp-server"],
        env=notion_env
    )

    print(server_parameters)

    

    
    # Create a tool collection from the MCP server
    with MCPAdapt(server_parameters, SafeNameAdapter()) as tools:
            tool_collection = ToolCollection(tools)

            print("Available tools:", [tool.name for tool in tool_collection.tools])

            # Initialize the agent with tools from the MCP server
            agent = CodeAgent(
                tools=[*tool_collection.tools], 
                model=model,
                add_base_tools=False
            )
            
            print("Notion Agent initialized!")
            print("Available tools:", [tool.name for tool in tool_collection.tools])
            
            # Start an interactive loop
            while True:
                user_input = input("\nEnter your command (or 'exit' to quit): ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                
                try:
                    # Run the agent with the user's input
                    response = agent.run(user_input)
                    print("\nAgent response:")
                    print(response)
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    main()