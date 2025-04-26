import os
import json
from dotenv import load_dotenv
from supabase import create_client
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from mcp import StdioServerParameters

def main():
    # Load environment variables
    try:
        load_dotenv()
    except Exception:
        pass

    # Initialize Supabase client (for random selection)
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
    SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in the environment.")
        return
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    # Ask user for input method
    choice = input("Select input method:\n1) Enter a custom startup idea\n2) Use a random idea from Supabase\n> ").strip()
    if choice == "1":
        # Manual entry
        title = input("Enter idea title: ").strip()
        desc = input("Enter idea description: ").strip()
        ideas = [{"id": None, "title": title, "business_idea": desc}]
    elif choice == "2":
        # Random selection from Supabase
        import random
        print("Fetching startup ideas from Supabase...")
        resp = supabase.table("startup_ideas").select("id, title, business_idea").execute()
        all_ideas = resp.data or []
        if not all_ideas:
            print("No ideas found in database.")
            return
        chosen = random.choice(all_ideas)
        ideas = [chosen]
        print(f"Selected idea ID {chosen.get('id')}: {chosen.get('title')}")
    else:
        print("Invalid choice. Exiting.")
        return

    # Configure the FastDomainCheck MCP server
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_dir = os.path.abspath(os.path.join(current_dir, "..", "mcp-servers", "FastDomainCheck-MCP-Server"))
    print(f"Starting FastDomainCheck MCP server from {mcp_dir}...")
    server_params = StdioServerParameters(
        command="go",
        args=["run", "main.go"],
        cwd=mcp_dir,
        env=os.environ.copy(),
    )

    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")

    # Load MCP tools and run agent
    with ToolCollection.from_mcp(server_params, trust_remote_code=True) as tool_collection:
        print("Loaded tools:", [t.name for t in tool_collection.tools])
        agent = CodeAgent(
            tools=tool_collection.tools,
            model=model,
            add_base_tools=True,
            additional_authorized_imports=["json"],
            name="domain_agent",
            description="Suggest and check domain availability for startup ideas",
        )

        # Process each idea
        for idea in ideas:
            idea_id = idea.get("id")
            title = idea.get("title", "")
            desc = idea.get("business_idea", "")

            # Construct prompt: suggest only easy-to-pronounce .com domains and check availability
            prompt = f"""You are a helpful assistant. Given the following startup idea, do the following:

1. Propose up to 5 short, one-word, catchy, and relevant .com domain names for this idea.
   Only include names that are easy to pronounce (i.e., someone can hear them and repeat them correctly).
2. Use the `check_domains` tool to check availability of each proposed .com name.
3. Return the result in JSON format with the structure:
   {{
     "idea_id": {idea_id},
     "domains": {{
       "name1.com": true,
       "name2.com": false,
       ...
     }}
   }}

If no suitable .com names exist, return an empty domains object.

Startup Idea:
Title: {title}
Description: {desc}
"""
            print(f"Processing idea {idea_id}: {title}")
            try:
                result = agent.run(prompt)
                # Attempt to parse JSON
                try:
                    parsed = json.loads(result)
                    print(json.dumps(parsed, indent=2))
                except json.JSONDecodeError:
                    print("Agent output (non-JSON):", result)
            except Exception as e:
                print(f"Error processing idea {idea_id}: {e}")

if __name__ == "__main__":
    main()