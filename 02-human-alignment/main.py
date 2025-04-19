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

# -----------------------------------------------------------------------------
# Tool: Search arXiv API and return papers one at a time
# -----------------------------------------------------------------------------
@tool
def fetch_arxiv_papers(topic: str, max_results: int) -> str:
    """
    Searches the arXiv API for papers on a given topic and returns the raw XML.
    
    Args:
        topic: The research topic or keyword.
        max_results: The number of results to fetch.
        
    Returns:
        The raw XML response from arXiv.
    """
    query = f"search_query=all:{topic}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    url = f"http://export.arxiv.org/api/query?{query}"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error: Received status code {response.status_code} from arXiv API."
    
    return response.text

@tool
def parse_next_paper(xml_data: str, index: int) -> str:
    """
    Parses the XML data from arXiv and returns information about the paper at the given index.
    
    Args:
        xml_data: The raw XML response from arXiv.
        index: The index of the paper to parse.
        
    Returns:
        A JSON string representing the paper information, or a message if no more papers are found.
    """
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        return f"Error parsing XML: {str(e)}"
    
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = root.findall("atom:entry", ns)
    
    if index >= len(entries):
        return json.dumps({"status": "end", "message": "No more papers available."})
    
    entry = entries[index]
    
    title_elem = entry.find("atom:title", ns)
    summary_elem = entry.find("atom:summary", ns)
    published_elem = entry.find("atom:published", ns)
    
    if title_elem is None or summary_elem is None or published_elem is None:
        return json.dumps({"status": "error", "message": "Incomplete paper entry."})
    
    title = title_elem.text.strip()
    summary_text = summary_elem.text.strip()
    published_date = published_elem.text.strip()

    # Find the first <link> element with rel="alternate" for the URL.
    paper_url = None
    for link in entry.findall("atom:link", ns):
        if link.attrib.get("rel") == "alternate":
            paper_url = link.attrib.get("href")
            break
    if paper_url is None:
        return json.dumps({"status": "error", "message": "No URL found for paper."})

    paper = {
        "status": "success",
        "paper_name": title,
        "url": paper_url,
        "published_date": published_date,
        "summary": summary_text,
        "total_papers": len(entries),
        "current_index": index
    }
    
    return json.dumps(paper, indent=2)

@tool
def push_to_supabase(paper_name: str, url: str, published_date: str, summary: str) -> str:
    """
    Pushes the qualifying paper information to the Supabase database (table: policy_papers).
    Checks if the paper already exists before inserting to avoid duplicates.

    Args:
        paper_name: The title of the paper.
        url: The URL to the paper.
        published_date: The published date of the paper (timestampz).
        summary: The paper summary.
    
    Returns:
        A confirmation message or a message if credentials are missing.
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_service_key:
        return "Supabase credentials not found in .env. Skipping database push."

    from supabase import create_client
    client = create_client(supabase_url, supabase_service_key)
    
    # Check if paper already exists by URL (more reliable than title which might have formatting differences)
    existing = client.table("policy_papers").select("*").eq("url", url).execute()
    
    # If paper already exists, return message
    if existing and existing.data and len(existing.data) > 0:
        return f"Paper already exists in database with URL: {url}. Skipping insertion."
    
    # If paper doesn't exist by URL, also check by title for extra safety
    existing = client.table("policy_papers").select("*").eq("paper_name", paper_name).execute()
    
    if existing and existing.data and len(existing.data) > 0:
        return f"Paper already exists in database with title: {paper_name}. Skipping insertion."
    
    # If paper doesn't exist, insert it
    print(f"Inserting record - Paper Name: {paper_name}, URL: {url}, Published Date: {published_date}")
    
    response = client.table("policy_papers").insert({
        "paper_name": paper_name,
        "url": url,
        "summary": summary,
        "published_date": published_date
    }).execute()

    return "Paper pushed to the policy_papers table successfully."

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

# -----------------------------------------------------------------------------
# Main Agent Workflow
# -----------------------------------------------------------------------------
def main():
    # Configuration parameters
    #topic = "AI policy"  # Topic for arXiv query
    user_goal = (
        f"I want to find recent papers on AI policy as it relates to energy policy across governments (it's currently {date.today()})."
    )  # Criteria for a paper to qualify

    # Toggle to include or exclude the database push functionality.
    include_db_push = True

    # Set up the tools list for the agent.
    tools = [fetch_arxiv_papers, parse_next_paper, visit_webpage]
    if include_db_push:
        tools.append(push_to_supabase)
    
    # Initialize the agent with the chosen tools and a basic model.
    #model = HfApiModel()
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")


    agent = CodeAgent(
        tools=tools,
        model=model,
        add_base_tools=True,
        additional_authorized_imports=["time", "numpy", "pandas", "json"],
        max_steps=100
    )
    
    # Construct a task prompt instructing the agent.
    task = f"""
    Your task is to search for research papers that meet the following goal:
    
    "{user_goal}"
    
    Follow these steps:
    
    1. Use the "fetch_arxiv_papers" tool to fetch the raw XML data for papers on the topic, setting an appropriate max_results parameter.
    
    2. Process each paper sequentially:
       a. Call "parse_next_paper" with the XML data and the current index (starting from 0)
       b. Evaluate individually whether the paper meets the goal criteria. Use your logic and understanding based on the title and summary, not just keyword searches.
       c. If the paper qualifies, call the "push_to_supabase" tool with the paper information
       d. Increment the index and repeat until you've processed all papers or tried your best to find at least 5 qualifying papers
    
    3. For each qualifying paper, provide:
       - The paper title
       - Publication date
       - A brief description of how it relates to the goal
    
    4. After processing all papers, provide a summary of your findings, including:
       - The total number of papers reviewed
       - The number of qualifying papers found and stored in the database
       - Any observations about trends in the research
    """
    
    # Run the agent with the task.
    print("Running agent task...")
    result = agent.run(task)
    print("Agent output:")
    print(result)

if __name__ == '__main__':
    main()