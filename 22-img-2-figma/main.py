"""
Interactive CLI agent that uses HTTP to talk to the local MCP server
(FastAPI) endpoints and dispatches create_sticky commands via HTTP.
"""
import os
import requests
from dotenv import load_dotenv
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from smolagents.tools import tool
from image_to_data import parse_whiteboard

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
    
@tool
def create_text(text: str, x: int = 0, y: int = 0) -> str:
    """
    Enqueue a 'create_text' command via the MCP HTTP endpoint.

    Args:
        text: The text content to render.
        x: The x-coordinate where the text should be placed.
        y: The y-coordinate where the text should be placed.

    Returns:
        str: A status message, typically "queued".
    """
    resp = requests.get(
        "http://localhost:8787/mcp/create_text",
        params={"text": text, "x": x, "y": y},
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", "")
@tool
def move_node(id: str, x: int = 0, y: int = 0) -> str:
    """
    Enqueue a 'move_node' command via the MCP HTTP endpoint.

    Args:
        id: The ID of the node to move.
        x: The new x-coordinate.
        y: The new y-coordinate.

    Returns:
        str: A status message, typically "queued".
    """
    resp = requests.get(
        "http://localhost:8787/mcp/move_node",
        params={"id": id, "x": x, "y": y},
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", "")

@tool
def start_timer(seconds: int) -> str:
    """
    Enqueue a 'start_timer' command via the MCP HTTP endpoint.

    Args:
        seconds: The timer duration in seconds.

    Returns:
        str: A status message, typically "queued".
    """
    resp = requests.get(
        "http://localhost:8787/mcp/start_timer",
        params={"seconds": seconds},
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", "")

@tool
def create_connector(start_id: str | None = None, end_id: str | None = None) -> str:
    """
    Enqueue a 'create_connector' command via the MCP HTTP endpoint.

    Args:
        start_id: Optional start node ID to connect.
        end_id: Optional end node ID to connect.

    Returns:
        str: A status message, typically "queued".
    """
    params = {}
    if start_id is not None:
        params["start_id"] = start_id
    if end_id is not None:
        params["end_id"] = end_id
    resp = requests.get(
        "http://localhost:8787/mcp/create_connector",
        params=params,
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("result", "")
    
@tool
def read_txt_file(filepath: str = "whiteboard.txt") -> str:
    """
    Reads the contents of the text file.

    Args:
        filepath: file

    Returns:
        The full contents of the file as a string
    """
    with open(filepath, "r") as f:
        return f.read()


# @tool
# def ingest_whiteboard(image_path: str) -> str:
#     """
#     Parse a whiteboard image and enqueue commands to recreate it in FigJam.

#     Args:
#         image_path: Local file path to the whiteboard image.

#     Returns:
#         str: Summary of queued operations.
#     """
#     elements = parse_whiteboard(image_path)
#     print(elements)
#     count = 0
#     # Maps temporary indices to created node IDs if available
#     for el in elements:
#         typ = el.get('type')
#         if typ == 'sticky':
#             create_sticky(el.get('text', ''), el.get('x', 0), el.get('y', 0))
#             count += 1
#         elif typ == 'connector':
#             create_connector(el.get('start_id'), el.get('end_id'))
#             count += 1
#         elif typ == 'text':
#             create_text(el.get('text', ''), el.get('x', 0), el.get('y', 0))
#             count += 1
#         # Add other element types here as needed
#     return f"Queued {count} elements from {image_path}"

def main():
    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    # Collect HTTP-backed MCP tools
    tool_collection = ToolCollection([
        create_sticky,
        create_text,
        move_node,
        start_timer,
        create_connector,
        read_txt_file
        #ingest_whiteboard,
    ])
    print("Available tools:", [t.name for t in tool_collection.tools])

    # Create the agent with discovered tools
    agent = CodeAgent(
        tools=[*tool_collection.tools],
        model=model,
        additional_authorized_imports=["time", "numpy", "pandas", "json", "os", "posixpath"],
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