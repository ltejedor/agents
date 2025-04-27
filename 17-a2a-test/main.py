import os
import json
import time
from typing import List, Dict, Any, Optional
from uuid import uuid4
from dotenv import load_dotenv

# Import smolagents for agent creation
from smolagents import ToolCollection, CodeAgent, LiteLLMModel
from smolagents.tools import tool

# Import MCP-related components
from mcp import StdioServerParameters
from mcpadapt.core import MCPAdapt
from mcpadapt.smolagents_adapter import SmolAgentsAdapter

# Import components from other modules
import re
import pandas as pd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import hdbscan


class SafeNameAdapter(SmolAgentsAdapter):
    """Ensures tool names are valid Python identifiers."""
    def adapt(self, func, tool):
        # Sanitize tool names by replacing non-identifier characters with underscores
        safe_name = re.sub(r'\W|^(?=\d)', '_', tool.name)
        tool.name = safe_name
        return super().adapt(func, tool)


# Custom tools for the A2A system

@tool
def cluster_trends(items: List[Dict[str, str]], min_cluster_size: int = 2) -> str:
    """
    Cluster items based on their titles using sentence embeddings.
    
    Args:
        items: List of dictionaries with at least a "title" key
        min_cluster_size: Minimum number of items to form a cluster
        
    Returns:
        String representation of the clusters
    """
    texts = [item["title"] for item in items]
    if not texts:
        return "No items to cluster."

    # Load the sentence transformer model
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Generate embeddings and cluster
    embeddings = model.encode(texts)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, metric="euclidean")
    labels = clusterer.fit_predict(embeddings)

    # Organize items into clusters
    clusters = {}
    for label, text in zip(labels, texts):
        if label == -1:  # Skip noise points
            continue
        clusters.setdefault(label, []).append(text)

    # Format the clusters as text
    cluster_text = []
    for i, titles in clusters.items():
        cluster_text.append(f"🔸 Cluster {i} ({len(titles)} items):")
        cluster_text.extend(f"- {t}" for t in titles)
        cluster_text.append("")  # add space between clusters

    return "\n".join(cluster_text) or "No meaningful clusters found."

@tool
def create_experiment_plan(
    assumption: str,
    hypothesis: str,
    metrics: List[str],
    test_method: str,
    resources_needed: List[str],
    timeline: Dict[str, str],
    success_criteria: str,
    fallback_plan: str
) -> Dict[str, Any]:
    """
    Create a structured Lean experiment plan.
    
    Args:
        assumption: The core assumption being tested
        hypothesis: The testable hypothesis statement
        metrics: List of metrics to track
        test_method: Description of how the experiment will be conducted
        resources_needed: List of resources required
        timeline: Dictionary mapping timeline stages to dates/times
        success_criteria: Description of what constitutes success
        fallback_plan: What to do if the experiment fails
        
    Returns:
        A dictionary containing the structured experiment plan
    """
    plan = {
        "experiment_id": f"exp-{uuid4().hex[:8]}",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "assumption": assumption,
        "hypothesis": hypothesis,
        "metrics": metrics,
        "test_method": test_method,
        "resources_needed": resources_needed,
        "timeline": timeline,
        "success_criteria": success_criteria,
        "fallback_plan": fallback_plan,
        "status": "ready"
    }
    return plan

@tool
def format_experiment_plan_markdown(plan: Dict[str, Any]) -> str:
    """
    Format an experiment plan as a Markdown document.
    
    Args:
        plan: The experiment plan dictionary
        
    Returns:
        Markdown formatted string
    """
    md = f"""# Lean Experiment Plan: {plan['experiment_id']}

*Created: {plan['created_at']}*

## Core Assumption
{plan['assumption']}

## Hypothesis
{plan['hypothesis']}

## Metrics to Track
"""
    
    for metric in plan['metrics']:
        md += f"- {metric}\n"
    
    md += f"""
## Test Method
{plan['test_method']}

## Resources Needed
"""
    
    for resource in plan['resources_needed']:
        md += f"- {resource}\n"
    
    md += f"""
## Timeline
"""
    
    for stage, time in plan['timeline'].items():
        md += f"- **{stage}**: {time}\n"
    
    md += f"""
## Success Criteria
{plan['success_criteria']}

## Fallback Plan
{plan['fallback_plan']}

## Status
**{plan['status'].upper()}**
"""
    
    return md


class AgentCard:
    """Represents an agent's capabilities in the A2A protocol."""
    
    def __init__(self, name, description, skills, capabilities=None):
        self.name = name
        self.description = description
        self.skills = skills
        self.capabilities = capabilities or {}
    
    def to_dict(self):
        """Convert the agent card to a dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "skills": self.skills,
            "capabilities": self.capabilities
        }


class Task:
    """Represents a task in the A2A protocol."""
    
    def __init__(self, task_id, session_id=None, status="submitted", message=None):
        self.id = task_id
        self.session_id = session_id or f"session-{uuid4().hex[:8]}"
        self.status = status
        self.message = message
        self.artifacts = []
        self.history = []
        self.metadata = {}
        self.created_at = time.time()
        self.updated_at = time.time()
    
    def update_status(self, new_status, message=None):
        """Update the task status and timestamp."""
        self.status = new_status
        if message:
            self.message = message
        self.updated_at = time.time()
        self.history.append({
            "timestamp": self.updated_at,
            "status": new_status,
            "message": message
        })
    
    def add_artifact(self, name, content, description=None):
        """Add an artifact to the task."""
        artifact = {
            "name": name,
            "content": content,
            "description": description,
            "created_at": time.time()
        }
        self.artifacts.append(artifact)
        self.updated_at = time.time()
    
    def to_dict(self):
        """Convert the task to a dictionary."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "status": self.status,
            "message": self.message,
            "artifacts": self.artifacts,
            "history": self.history,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


def create_trend_analysis_agent(model):
    """Create an agent specialized in trend analysis."""
    return CodeAgent(
        tools=[cluster_trends],
        model=model,
        name="trend_analysis_agent",
        description="Analyzes market trends and identifies patterns in data",
        additional_authorized_imports=["json", "pandas", "numpy", "re"],
        add_base_tools=True
    )


def create_research_agent(model, tools=None):
    """Create an agent specialized in research."""
    return CodeAgent(
        tools=tools or [],
        model=model,
        name="research_agent",
        description="Conducts research on topics, competitors, and markets",
        additional_authorized_imports=["json", "requests", "bs4"],
        add_base_tools=True
    )


def create_experiment_design_agent(model):
    """Create an agent specialized in designing experiments."""
    return CodeAgent(
        tools=[create_experiment_plan, format_experiment_plan_markdown],
        model=model,
        name="experiment_design_agent",
        description="Designs Lean experiments based on assumptions and research",
        additional_authorized_imports=["json", "time", "uuid"],
        add_base_tools=True
    )


def create_domain_check_agent(model, domain_tools=None):
    """Create an agent specialized in domain checking."""
    return CodeAgent(
        tools=domain_tools or [],
        model=model,
        name="domain_check_agent",
        description="Checks domain availability for potential product names",
        additional_authorized_imports=["json"],
        add_base_tools=True
    )


def create_manager_agent(model, managed_agents):
    """Create a manager agent that coordinates other agents."""
    return CodeAgent(
        tools=[],
        model=model,
        managed_agents=managed_agents,
        name="manager_agent",
        description="Coordinates specialized agents to process assumptions and create experiment plans",
        additional_authorized_imports=["json", "time", "uuid"],
        add_base_tools=True
    )


def main():
    """Main function to run the A2A system."""
    # Load environment variables
    try:
        load_dotenv()
    except Exception:
        pass
    
    print("🚀 Starting Agent2Agent (A2A) Experiment Planning System")
    print("=" * 70)
    
    # Initialize the LLM model (Anthropic Claude)
    model = LiteLLMModel(model_id="anthropic/claude-3-7-sonnet-latest")
    
    # Set up the MCP server parameters for domain checking
    current_dir = os.path.dirname(os.path.abspath(__file__))
    domain_mcp_dir = os.path.abspath(
        os.path.join(current_dir, "..", "mcp-servers", "FastDomainCheck-MCP-Server")
    )
    domain_server_params = StdioServerParameters(
        command="go",
        args=["run", "main.go"],
        cwd=domain_mcp_dir,
        env=os.environ.copy(),
    )
    
    # Set up the MCP server parameters for Google Sheets
    sheets_mcp_dir = os.path.abspath(
        os.path.join(current_dir, "..", "mcp-servers", "google-sheets-mcp")
    )
    sheets_server_params = StdioServerParameters(
        command="node",
        args=["dist/index.js"],
        env=os.environ.copy(),
        cwd=sheets_mcp_dir,
    )
    
    print("Initializing specialized agents...")
    
    # Create the specialized agents
    trend_agent = create_trend_analysis_agent(model)
    experiment_agent = create_experiment_design_agent(model)
    
    # Load domain check tools
    with ToolCollection.from_mcp(domain_server_params, trust_remote_code=True) as domain_tools, \
         ToolCollection.from_mcp(sheets_server_params, trust_remote_code=True) as sheets_tools:
        
        # Create agents with MCP tools
        domain_agent = create_domain_check_agent(model, domain_tools.tools)
        research_agent = create_research_agent(model, sheets_tools.tools)
        
        # Create the manager agent
        manager = create_manager_agent(
            model, 
            [trend_agent, research_agent, domain_agent, experiment_agent]
        )
        
        print("Agent2Agent system initialized with the following agents:")
        print(f"- {trend_agent.name}: {trend_agent.description}")
        print(f"- {research_agent.name}: {research_agent.description}")
        print(f"- {domain_agent.name}: {domain_agent.description}")
        print(f"- {experiment_agent.name}: {experiment_agent.description}")
        print(f"- {manager.name}: {manager.description}")
        print("=" * 70)
        
        # Interactive REPL
        while True:
            assumption = input("\nEnter your assumption (or 'exit' to quit): ")
            if assumption.lower() in ['exit', 'quit']:
                break
            
            # Create a task
            task_id = f"task-{uuid4().hex[:8]}"
            task = Task(task_id)
            
            print(f"\nProcessing assumption... (Task ID: {task_id})")
            task.update_status("working", "Processing your assumption")
            
            # Construct the prompt for the manager agent
            prompt = f"""You are the coordinator of a multi-agent system designed to create Lean experiment plans.

A user has provided the following assumption that needs to be tested:

"{assumption}"

Your task is to:

1. Use the trend_analysis_agent to identify relevant market trends
2. Use the research_agent to gather information about the market, competitors, and potential customers
3. Use the domain_check_agent to check availability of potential domain names for this experiment
4. Use the experiment_design_agent to create a comprehensive Lean experiment plan

The final output should be a structured Lean experiment plan that can be executed the next morning.
The plan should include:
- A clear hypothesis derived from the assumption
- Specific metrics to track
- A detailed test method
- Required resources
- A timeline for execution (starting tomorrow morning)
- Success criteria
- A fallback plan

Format the final output as a Markdown document using the format_experiment_plan_markdown tool.
"""
            
            try:
                # Run the manager agent
                result = manager.run(prompt)
                
                # Update the task
                task.update_status("completed", "Experiment plan generated")
                task.add_artifact("experiment_plan", result, "Lean experiment plan in Markdown format")
                
                # Display the result
                print("\n" + "=" * 70)
                print("LEAN EXPERIMENT PLAN")
                print("=" * 70)
                print(result)
                print("=" * 70)
                
                # Ask if the user wants to save the plan
                save_option = input("\nSave this experiment plan to a file? (y/n): ")
                if save_option.lower() == 'y':
                    filename = f"experiment_plan_{task_id}.md"
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"Plan saved to {filename}")
                
            except Exception as e:
                task.update_status("failed", f"Error: {str(e)}")
                print(f"Error generating experiment plan: {e}")


if __name__ == "__main__":
    main()