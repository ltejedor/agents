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
├── news/
├── 02-human-alignment/
├── 03-agent-name/
├── ...
├── mcp-servers/          # Backend MCP connectors (WhatsApp, Notion, Google Sheets, etc.)
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

Each numbered agent workflow includes a Python entry point (`main.py`). From the repository root, you can run any workflow directly without changing directories. For example:
```bash
# Research
python 02-human-alignment/main.py
python news/main.py

# Project Management
python 07-project-management/main.py

# Whiteboarding (FigJam)
python 08-whiteboarding/main.py

# Google Sheets CLI
python 09-google-sheets/main.py
```

Before running, install root dependencies:
```bash
pip install -r requirements.txt
# For workflows with extra dependencies, see each folder’s README.
```

## Follow Along

- Follow [#30daysofagents @leeps.bsky.social](https://bsky.app/hashtag/30daysofagents?author=leeps.bsky.social) on Bluesky for daily updates
- Visit [agents.mechifact.com](https://agents.mechifact.com/) for interactive demos
