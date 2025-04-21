# 30 Agents in 30 Days

[![Follow along on Bluesky](https://img.shields.io/badge/Follow-Bluesky-blue)](https://bsky.app/hashtag/30daysofagents?author=leeps.bsky.social)
[![Website](https://img.shields.io/badge/Website-agents.mechifact.com-green)](https://agents.mechifact.com/)

AI agent workflows designed to save you time when developing products - across research, development, testing, marketing, and sales.

## About the Project

**30 Agents in 30 Days** is a challenge to create and share 30 practical AI agent workflows that help product builders save time and improve their process. Each day, a new agent workflow is released to help with different aspects of the product development lifecycle.

## Project Structure

Each agent workflow is contained in its own folder with complete documentation, code, and instructions for implementation.

```
/ 
├── news/                        # Day 01: News summarization (PocketFlow)
├── 02-human-alignment/          # Day 02: Human alignment (SmolAgents)
├── 03-ai-vs-ai-benchmark/       # Day 03: AI vs AI Benchmark (optional)
├── 04-trends/                   # Day 04: Trend detection (Gradio)
├── 05-whatsapp/                 # Day 05: WhatsApp multi-agent (SmolAgents)
├── 06-knowledge-graph/          # Day 06: Knowledge graph explorer (SmolAgents)
├── 07-project-management/       # Day 07: Project management with Notion (SmolAgents)
├── 08-whiteboarding/            # Day 08: Whiteboarding with FigJam (SmolAgents)
├── 09-google-sheets/            # Day 09: Google Sheets integration (SmolAgents)
├── 10-documentation-gen/        # Day 10: Documentation generation (SmolAgents)
├── 11-ui/                       # Day 11: No-code multi-agent builder (Streamlit)
├── 12-whatsapp-api/             # Day 12: WhatsApp Business API integration (advanced)
├── mcp-servers/                 # Backend MCP connectors (WhatsApp, Notion, Google Sheets, etc.)
└── assets/                      # Shared assets
```


## What's Coming

Every day for 30 days, I'm releasing a new AI agent workflow to help you build better products faster. The agents are organized into four main categories:

### Research
Agents that help you gather insights and analyze data, including:
- Market research automation
- Competitive analysis
- User feedback processing
- Trend identification

### Development
Agents that accelerate your coding and development workflow, such as:
- Code generation and refactoring
- Architecture planning
- Documentation creation
- Feature prioritization

### Testing
Agents that help you test your products thoroughly, including:
- Automated QA workflows
- User journey simulation
- Performance testing
- Security assessment

### Marketing & Sales
Agents that help you promote and sell your products, such as:
- Content generation
- Ad copy optimization
- Lead qualification
- Sales outreach automation

## How to Use This Project

Each agent workflow folder includes a README.md tutorial with step-by-step instructions and examples.

1. **Browse**: Explore the different agent workflows organized by category
2. **Implement**: Follow the instructions in each agent's README to set up the workflow
3. **Customize**: Adapt the agents to your specific product needs
4. **Contribute**: Share your improvements or ideas by opening issues or PRs

## Recommended Exploration Path

To help you dive in, here’s a suggested order for exploring the workflows:

- **Day 11: No-Code Multi-Agent Builder** (`11-ui`)
  Try the live demo at https://mechifact.streamlit.app/ or run locally:
  ```bash
  pip install -r requirements.txt streamlit
  streamlit run 11-ui/main.py
  ```
- **Day 01: News Summarization with PocketFlow** (`news`)
  ```bash
  python news/main.py
  ```
- **Day 02: Human Alignment** (`02-human-alignment`)
  Uses SmolAgents and the arXiv API:
  ```bash
  python 02-human-alignment/main.py
  ```
- **Day 03: AI vs AI Benchmark** (`03-ai-vs-ai-benchmark`) *Optional*
  A conceptual hackathon project—explore at your leisure.
- **Day 04: Trend Detection (Gradio)** (`04-trends`)
  ```bash
  pip install -r 04-trends/requirements.txt
  python 04-trends/interface.py
  ```
- **Day 05: WhatsApp Multi-Agent** (`05-whatsapp`)
  Requires setup (see folder README):
  ```bash
  python 05-whatsapp/main.py
  ```
- **Day 06: Knowledge Graph Explorer** (`06-knowledge-graph`)
  ```bash
  python 06-knowledge-graph/interface.py
  ```
- **Day 07: Project Management with Notion** (`07-project-management`)
  ```bash
  python 07-project-management/main.py
  ```
- **Day 08: Whiteboarding with FigJam** (`08-whiteboarding`)
  Requires FigJam plugin and local server (see folder README):
  ```bash
  python 08-whiteboarding/main.py
  ```
- **Day 09: Google Sheets Integration** (`09-google-sheets`)
  ```bash
  python 09-google-sheets/main.py
  ```
- **Day 10: Documentation Generation** (`10-documentation-gen`)
  Compare single vs multi-agent:
  ```bash
  python 10-documentation-gen/single_agent.py
  python 10-documentation-gen/multi_agent.py
  ```
- **Day 12: WhatsApp Business API Integration** (`12-whatsapp-api`) *Advanced*
  Requires a WhatsApp Business account and setup.
  See [12-whatsapp-api/README.md](12-whatsapp-api/README.md) for details.

## Cloning with Submodules

To ensure you also clone all MCP server backends (Notion, Google Sheets, WhatsApp), use the `--recursive` flag when cloning:
```bash
git clone --recursive https://github.com/yourusername/agents.git
```
If you've already cloned without `--recursive`, initialize and fetch the submodules with:
```bash
git submodule update --init --recursive
```

## Running Agents Locally

Each workflow includes entry points (e.g., `main.py`, `interface.py`). From the repository root, install dependencies and run any workflow:
```bash
# Install root dependencies
pip install -r requirements.txt
# (For Trend detection)
pip install -r 04-trends/requirements.txt
# (For Streamlit UI)
pip install streamlit

# Day 01: News Summarization (PocketFlow)
python news/main.py

# Day 02: Human Alignment (SmolAgents)
python 02-human-alignment/main.py

# Day 03: AI vs AI Benchmark (optional)
python 03-ai-vs-ai-benchmark/main.py

# Day 04: Trend Detection (Gradio)
python 04-trends/interface.py

# Day 05: WhatsApp Multi-Agent (SmolAgents)
python 05-whatsapp/main.py

# Day 06: Knowledge Graph Explorer (SmolAgents)
python 06-knowledge-graph/interface.py

# Day 07: Project Management with Notion (SmolAgents)
python 07-project-management/main.py

# Day 08: Whiteboarding with FigJam (SmolAgents)
python 08-whiteboarding/main.py

# Day 09: Google Sheets Integration (SmolAgents)
python 09-google-sheets/main.py

# Day 10: Documentation Generation (SmolAgents)
python 10-documentation-gen/single_agent.py
python 10-documentation-gen/multi_agent.py

# Day 11: No-Code Multi-Agent Builder (Streamlit)
streamlit run 11-ui/main.py

# Day 12: WhatsApp Business API Integration (advanced)
# See 12-whatsapp-api/README.md for setup instructions
```

## Follow Along

- Follow [#30daysofagents @leeps.bsky.social](https://bsky.app/hashtag/30daysofagents?author=leeps.bsky.social) on Bluesky for daily updates
- Visit [agents.mechifact.com](https://agents.mechifact.com/) for interactive demos
