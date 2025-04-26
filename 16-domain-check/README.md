 # Domain Availability Checker

 A smolagents-based script that fetches startup ideas from a Supabase table and checks availability of easy-to-pronounce .com domain names for each idea, using the FastDomainCheck MCP server.

 ## Overview

 This tool automates domain ideation and availability checking for startup ideas.
 You can choose to:
 - Enter a custom idea manually (provide title and description).
 - Select a random idea from your Supabase `startup_ideas` table (id, title, business_idea).
 The script then suggests easy-to-pronounce .com domains and checks their availability via the FastDomainCheck MCP server.

 ## Prerequisites

 - Python 3.8+
 - Go 1.16+ (for the FastDomainCheck MCP server)
 - Supabase project with a `startup_ideas` table
 - Environment variables:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_SERVICE_KEY`: Supabase service role key
   - `ANTHROPIC_API_KEY`: API key for Claude 3.7 Sonnet (or configured LLM provider)

 ## Installation

 1. Clone the repository and navigate to this folder:
    ```bash
    git clone <repo-url>
    cd <repo-root>/16-domain-check
    ```
 2. Install Python dependencies:
    ```bash
    pip install -r ../requirements.txt
    ```
 3. (Optional) Build the FastDomainCheck MCP server:
    ```bash
    cd ../mcp-servers/FastDomainCheck-MCP-Server
    go build -o fastdomaincheck
    ```

 ## Usage

 Run the main script:
 ```bash
 python main.py
 ```

 The script will:
 1. Load environment variables.
 2. Prompt you to choose:
    - Enter a custom startup idea (title & description).
    - Select a random idea from Supabase.
 3. Launch the FastDomainCheck MCP server.
 4. Suggest up to 5 easy-to-pronounce .com domains for the chosen idea.
 5. Check domain availability and print JSON results.

 ## Example Output

 ```json
 {
   "idea_id": 1,
   "domains": {
     "quickfix.com": true,
     "helpmate.com": false
   }
 }
 ```

 ## Troubleshooting

 - Ensure `go run main.go` works in `mcp-servers/FastDomainCheck-MCP-Server`.
 - Verify Supabase environment variables are set correctly.
 - Confirm the `startup_ideas` table exists and contains data.

 ## License

 [Insert license here]