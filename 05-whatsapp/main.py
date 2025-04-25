import os
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from mcp import StdioServerParameters
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()

def main():
    # Initialize the Anthropic client for Claude
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")
    
    # Set up the MCP server parameters for WhatsApp
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # After reorganizing MCP servers, locate WhatsApp MCP under mcp-servers
    whatsapp_mcp_dir = os.path.abspath(
        os.path.join(current_dir, "..", "mcp-servers", "whatsapp-mcp", "whatsapp-mcp-server")
    )
    
    server_parameters = StdioServerParameters(
        command="python",
        args=["main.py"],
        env=os.environ,
        cwd=whatsapp_mcp_dir,
    )

    # Create a tool collection from the MCP server
    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        # Initialize the agent with tools from the MCP server and the client as the model
        agent = CodeAgent(
            tools=[*tool_collection.tools], 
            model=model,
            add_base_tools=True
        )
        
        print("WhatsApp Agent initialized! You can now interact with your WhatsApp.")
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