 # Domain Availability Checker

 A tutorial-driven smolagents example to suggest and verify easy-to-pronounce .com domains for startup ideas using the FastDomainCheck MCP server.

## Overview

This tutorial-driven script uses an LLM to suggest easy-to-pronounce .com names for startup ideas, then verifies availability via the FastDomainCheck MCP server. You can:
- Enter a custom idea manually (provide title & description).
- Fetch a random idea from your Supabase `startup_ideas` table (`id`, `title`, `business_idea`).

Workflow:
1. Prompt for idea input.
2. Generate domain suggestions via LLM.
3. Use the `check_domains` tool on the MCP server.
4. Output JSON results mapping each domain to availability.

 ## Prerequisites

 - Python 3.8+
 - Go 1.16+ (for the FastDomainCheck MCP server)
 - Supabase project with a `startup_ideas` table
 - Environment variables:
   - `SUPABASE_URL`: Your Supabase project URL
   - `SUPABASE_SERVICE_KEY`: Supabase service role key
   - `ANTHROPIC_API_KEY`: API key for Claude 3.7 Sonnet (or configured LLM provider)

## Setup Tutorial

1. Clone the repository and navigate to this folder:
   ```bash
   git clone https://github.com/ltejedor/agents.git
   cd agents/16-domain-check
   ```
 2. Install Python dependencies:
    ```bash
    pip install -r ../requirements.txt
    ```
3. Build the FastDomainCheck MCP server:
   ```bash
   cd ../mcp-servers/FastDomainCheck-MCP-Server
   go mod download
   go build -o fastdomaincheck main.go
   ```
4. Test the MCP server manually:
   ```bash
   echo '{"domains":["example.com","nonexistent12345.com"]}' | ./fastdomaincheck
   ```
   You should see a JSON response with `registered: true/false`.

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

 MIT (see main repo for details)