from smolagents import CodeAgent, InferenceClientModel, GradioUI, tool
import os
from huggingface_hub import HfApi, login, snapshot_download
import requests
from typing import List, Dict
from typing import Optional, Union
from pathlib import Path

# read token from environment
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
if not HF_TOKEN:
    raise RuntimeError("HUGGINGFACE_API_KEY environment variable is not set")

# tell huggingface_hub to use it
login(token=HF_TOKEN)

@tool
def leaderboard_search(query: str) -> str:
    """
    Search Hugging Face Spaces specifically in the model benchmarking category.
    
    Args:
        query: The search query to find relevant model benchmarking spaces
        
    Returns:
        A formatted string containing search results with space names, descriptions, and additional information
    """
    api_url = "https://huggingface.co/api/spaces"
    
    search_words = ["arena", "leaderboard", "benchmark"]
    results = []

    try:
        for word in search_words:
            params = {
                "search": query + " " + word,
                "full": True  # Get full information
            }
            
            response = requests.get(api_url, params=params, headers={"Authorization": f"Bearer {HF_TOKEN}"})
            print(response)
            
            spaces = response.json()
            print(spaces)
            
            if not spaces:
                continue  # Skip if no spaces found for this search word
            
            for space in spaces:
                # Extract relevant information
                space_id = space.get("id", "Unknown")
                author = space_id.split("/")[0] if "/" in space_id else "Unknown"
                space_name = space_id.split("/")[1] if "/" in space_id else space_id
                likes = space.get("likes", 0)
                
                # Try to get detailed information if available
                title = space.get("cardData", {}).get("title") if space.get("cardData") else space_name
                description = space.get("cardData", {}).get("short_description", "No description available") if space.get("cardData") else "No description available"
                
                # Create formatted result string
                result = f"🚀 **{title}** ({space_id})\n"
                result += f"   👤 Author: {author}\n"
                result += f"   📝 {description}\n"
                result += f"   ❤️ Likes: {likes}\n"
                result += f"   🔗 URL: https://huggingface.co/spaces/{space_id}\n"
                
                results.append(result)
        
        if not results:
            return f"No model benchmarking spaces found for query: '{query}'"
        
        return "\n".join(results)
    except requests.exceptions.RequestException as e:
        return f"Error searching Hugging Face Spaces: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
        
    except requests.exceptions.RequestException as e:
        return f"Error searching Hugging Face Spaces: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

@tool
def get_space_content(space_id: str) -> str:
    """
    Fetch the full HTML content of a Hugging Face Space webpage.
    
    Args:
        space_id: The id of the Hugging Face Space (e.g., "owner/my-awesome-space") to view online
    """
    try:
        url = f"https://huggingface.co/spaces/{space_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text  # Return raw HTML
        return f"Failed to fetch page for '{space_id}', status code: {response.status_code}"
    except Exception as e:
        return f"Error fetching content for '{space_id}': {e}"
    
@tool
def download_space_files(
    space_id: str,
    force_download: bool = False,
    max_workers: int = 8
) -> str:
    """
    Download all files from a Hugging Face Space (snapshot).

    Args:
        space_id: e.g. "owner/my-awesome-space"
        force_download: redownload even if cached
        max_workers: parallel downloads

    Returns:
        The local folder path where the space’s files now live.
    """
    try:
        folder = snapshot_download(
            repo_id=space_id,
            repo_type="space",
            force_download=force_download,
            max_workers=max_workers
        )
        # List how many files were downloaded
        files = list(Path(folder).rglob("*"))
        return (
            f"✔️ Downloaded {len(files)} files from space `{space_id}`\n"
            f"📂 Local path: {folder}"
        )
    except Exception as e:
        return f"❌ Failed to download space `{space_id}`: {e}"
    

@tool
def get_file_from_space(space_id: str, file_path: str) -> str:
    """
    Get a specific file from a Hugging Face Space.
    
    Args:
        space_id: The Hugging Face Space ID
        file_path: Path to the file in the space
        
    Returns:
        The file content or error message
    """
    try:
        url = f"https://huggingface.co/spaces/{space_id}/raw/main/{file_path}"
        response = requests.get(url, headers={"Authorization": f"Bearer {HF_TOKEN}"})
        
        if response.status_code == 200:
            return f"Content of {file_path} from {space_id}:\n\n{response.text}"
        else:
            return f"Couldn't retrieve {file_path} from {space_id}"
            
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize the agent with the leaderboard search and space content tools
model = InferenceClientModel()
agent = CodeAgent(
    tools=[leaderboard_search, get_space_content, get_file_from_space, download_space_files],
    additional_authorized_imports=["json", "requests", "pandas"],
    model=model,
    add_base_tools=False,
    description="Your job is to find the best possible model for a given task based on relevant leaderboards or arenas. You will be provided with a task description, and you should use the leaderboard tool to find relevant leaderboards or arenas. If you want to inspect the contents of a particular Space (e.g., README or code), use the space_content_tool. Respond with a list of the top models, including their names, scores, and links to their leaderboard pages.",
)

GradioUI(agent).launch()