# Agent2Agent (A2A) Experiment Planning System

This project implements an Agent2Agent (A2A) system that converts business assumptions into executable Lean experiment plans. The system leverages multiple specialized AI agents that collaborate through a standardized communication protocol to analyze assumptions, conduct research, and generate comprehensive experiment plans ready to run the next morning.

## What is the Agent2Agent (A2A) Protocol?

The Agent2Agent (A2A) protocol is an open standard developed by Google that enables seamless communication and interoperability between AI agents built on different frameworks, by different teams, or even different vendors. It provides a standardized communication layer that allows agents to:

- **Discover** each other's capabilities
- **Communicate** through structured messages
- **Coordinate** complex tasks
- **Exchange** various types of data
- **Work together** securely and effectively

A2A addresses the challenge of enabling diverse and often opaque agentic applications to collaborate on sophisticated problems. It acts as a lingua franca for AI agents, allowing them to work together regardless of their underlying implementation.

## System Architecture

This implementation follows the A2A protocol's principles with a manager-worker architecture:

### Components

1. **Manager Agent**: Coordinates the workflow and delegates tasks to specialized agents
2. **Specialized Agents**:
   - **Trend Analysis Agent**: Identifies patterns in data using sentence embeddings and clustering
   - **Research Agent**: Gathers information about markets, competitors, and customers using Google Sheets
   - **Domain Check Agent**: Verifies domain availability for potential product names
   - **Experiment Design Agent**: Creates structured Lean experiment plans

### Key Classes

- `AgentCard`: Represents an agent's capabilities, skills, and metadata
- `Task`: Manages the lifecycle of tasks with status tracking, history, and artifacts
- `SafeNameAdapter`: Ensures tool names are valid Python identifiers for compatibility

### Custom Tools

- `cluster_trends`: Clusters items based on their titles using sentence embeddings
- `create_experiment_plan`: Generates structured experiment plans with all required components
- `format_experiment_plan_markdown`: Formats plans as Markdown documents for readability

## Installation and Setup

### Prerequisites

- Python 3.10+
- Go (for the FastDomainCheck MCP server)
- Node.js (for the Google Sheets MCP server)
- Access to the MCP servers in the `mcp-servers` directory

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ltejedor/agents.git
   cd agents
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file to include:
   - `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` for LLM access
   - `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` for database access
   - Any other required API keys

4. Ensure the MCP servers are properly set up:
   - FastDomainCheck MCP Server (for domain checking)
   - Google Sheets MCP (for research and data analysis)

## Usage

Run the A2A Experiment Planning System:

```bash
python 17-a2a-test/main.py
```

The system will:

1. Initialize the specialized agents
2. Connect to the required MCP servers
3. Present an interactive prompt where you can enter your business assumptions

### Workflow

1. Enter a business assumption when prompted
2. The system creates a task and assigns it a unique ID
3. The manager agent coordinates the specialized agents to:
   - Analyze market trends related to the assumption
   - Research competitors and market information
   - Check domain availability for potential product names
   - Design a comprehensive Lean experiment plan
4. The final experiment plan is displayed in Markdown format
5. You can choose to save the plan to a file for future reference

### Example Input

```
Enter your assumption (or 'exit' to quit): Users will pay a monthly subscription for an AI-powered meal planning service that reduces food waste.
```

### Example Output

The system will generate a comprehensive Lean experiment plan in Markdown format, including:

- Core assumption and hypothesis
- Metrics to track
- Test method
- Required resources
- Timeline for execution
- Success criteria
- Fallback plan

## Technical Details

### A2A Protocol Implementation

This system implements key concepts from the A2A protocol:

1. **Agent Cards**: Each agent has a card that describes its capabilities, skills, and metadata
2. **Tasks**: Work units with lifecycle management, status tracking, and artifact collection
3. **Messages**: Structured communication between agents
4. **Artifacts**: Outputs generated during task execution

### Integration with MCP Servers

The system connects to Machine-Callable Program (MCP) servers to extend its capabilities:

1. **FastDomainCheck MCP Server**: Provides domain availability checking tools
2. **Google Sheets MCP**: Enables data storage, retrieval, and analysis

### Specialized Agent Capabilities

- **Trend Analysis Agent**: Uses sentence-transformers and HDBSCAN for semantic clustering
- **Research Agent**: Leverages Google Sheets for structured data analysis
- **Domain Check Agent**: Interfaces with the FastDomainCheck MCP server
- **Experiment Design Agent**: Creates structured experiment plans with standardized components

### Task Lifecycle

Tasks progress through defined states:
- `submitted`: Initial state when a task is created
- `working`: The system is actively processing the task
- `completed`: The task has been successfully completed
- `failed`: The task encountered an error

Each state transition is recorded in the task history for traceability.

## Benefits of the A2A Approach

This implementation demonstrates several key advantages of the A2A protocol:

1. **Modularity**: Specialized agents can be developed and improved independently
2. **Interoperability**: Agents built with different frameworks can work together seamlessly
3. **Scalability**: New agents can be added to the system without disrupting existing functionality
4. **Traceability**: Task history and artifacts provide a complete record of the system's operations
5. **Flexibility**: The system can be extended with new capabilities through additional agents or tools

## Future Enhancements

Potential improvements to this system include:

- Adding more specialized agents for different domains
- Implementing streaming responses for real-time updates
- Supporting push notifications for long-running tasks
- Enhancing the user interface with a web-based dashboard
- Adding authentication and authorization mechanisms
