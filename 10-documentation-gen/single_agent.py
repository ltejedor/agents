import os
import requests
import xml.etree.ElementTree as ET
import json
import re
from smolagents import CodeAgent, ToolCallingAgent, HfApiModel, tool, LiteLLMModel
from dotenv import load_dotenv
from requests.exceptions import RequestException
from datetime import date

load_dotenv()


@tool
def visit_webpage(url: str) -> str:
    """Visits a webpage at the given URL and returns its content as a markdown string.

    Args:
        url: The URL of the webpage to visit.

    Returns:
        The content of the webpage converted to Markdown, or an error message if the request fails.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Convert the HTML content to Markdown - assuming a markdownify function exists
        # You'll need to add the import for markdownify or implement the conversion
        from markdownify import markdownify
        markdown_content = markdownify(response.text).strip()

        # Remove multiple line breaks
        markdown_content = re.sub(r"\n{3,}", "\n\n", markdown_content)

        return markdown_content

    except RequestException as e:
        return f"Error fetching the webpage: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

@tool
def create_file(path: str, content: str) -> str:
    """
    Creates a file at the specified path with the given content.

    Args:
        path: The filesystem path where the file will be created.
        content: The text content to write into the file.
        Returns a success message or an error description.
    
    Returns: 
        The location and name of the file was created, or an error.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File created at {path}"
    except Exception as e:
        return f"Error creating file: {e}"

# -----------------------------------------------------------------------------
# Main Agent Workflow
# -----------------------------------------------------------------------------
def main():

    # Set up the tools list for the agent.
    tools = [visit_webpage, create_file]
    
    # Initialize the agent with the chosen tools and a basic model.
    #model = HfApiModel()
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    agent = CodeAgent(
        tools=tools,
        model=model,
        add_base_tools=True,
        additional_authorized_imports=["time", "json", "pydoc", "watchdog"],
        max_steps=100
    )
    
    # Construct a task prompt instructing the agent.
    task = f"""
        I'm building out a project that's going to be built on top of the WhatsApp API that you can access
        with a business account. Include instructions on getting set up, and a section on common issues developers
        have run into.
        Additionally, please create an OpenAPI site that lays out all functions of the Meta Cloud
        API. Under each major function, create an interactive code section for testing that API using native 
        OpenAPI features and best practices. Include a section that covers common example workflows, even if each
        individual system call has already been covered. When structuring the OpenAPI site, draw inspiration from
        the Diataxis model of documentation. Under the hood, attempt to use structured data whenever possible, with
        links to all sections that are referenced. Include interactive examples whenever helpful.
        
        Add all files to the folder documentation_single_agent/
    """
    
    # Run the agent with the task.
    print("Running agent task...")
    result = agent.run(task)
    print("Agent output:")
    print(result)

if __name__ == '__main__':
    main()