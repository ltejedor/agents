"""
Interactive CLI agent that uses HTTP to talk to the local MCP server
(FastAPI) endpoints and dispatches create_sticky commands via HTTP.
"""
import os
import requests
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from smolagents.tools import tool

load_dotenv()

@tool
def create_sticky(text: str, x: int = 0, y: int = 0) -> str:
    """
    Enqueue a 'create_sticky' command via the MCP HTTP endpoint.

    Args:
        text: The text content to display on the sticky note.
        x: The x-coordinate where the sticky note should be placed.
        y: The y-coordinate where the sticky note should be placed.

    Returns:
        str: A status message, typically "queued".
    """
    resp = requests.get(
        "http://localhost:8787/mcp/create_sticky",
        params={"text": text, "x": x, "y": y},
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", "")

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    # Collect HTTP-backed MCP tools
    tool_collection = ToolCollection([create_sticky])
    print("Available tools:", [t.name for t in tool_collection.tools])

    # Create the agent with discovered tools
    agent = CodeAgent(
        tools=[*tool_collection.tools],
        model=model,
        additional_authorized_imports=["time", "numpy", "pandas", "json"],
        add_base_tools=False,
    )
    print("Agent initialized. Ready to accept commands.")

    # Interactive REPL loop
    while True:
        user_input = input("\nEnter command (or 'exit' to quit): ")
        if user_input.lower() in ['exit', 'quit']:
            break
        try:
            response = agent.run(user_input)
            print("\nAgent response:\n", response)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()