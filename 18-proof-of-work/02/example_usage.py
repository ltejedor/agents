# example_usage.py
import json
import datetime
import random
import time

# Import our modules
from tool_tracker import ToolTracker
from data_store import DataStore
from visualization import DataVisualizer
from api import LLMProofOfWorkAPI

# EXAMPLE 1: Basic Tool Tracking
def example_1_basic_tracking():
    print("\n=== Example 1: Basic Tool Tracking ===")
    
    # Create a tool tracker
    tracker = ToolTracker(save_path="example_tool_calls.json")
    
    # Define some example tools
    @tracker.track_tool
    def web_search(query):
        # Simulated web search tool
        time.sleep(random.uniform(0.1, 0.3))  # Simulate network latency
        return [f"Result for {query}: {random.randint(1, 100)}"]
    
    @tracker.track_tool
    def calculator(operation, a, b):
        # Simulated calculator tool
        time.sleep(random.uniform(0.05, 0.1))  # Simulate calculation time
        if operation == "add":
            return a + b
        elif operation == "multiply":
            return a * b
        else:
            return None  # Simulated failure
    
    # Use the tools
    print("Running web searches...")
    for query in ["weather", "news", "sports", "technology"]:
        result = web_search(query)
        print(f"  Search '{query}': {result}")
    
    print("\nRunning calculations...")
    operations = ["add", "multiply", "divide", "add", "multiply"]
    for op in operations:
        a, b = random.randint(1, 10), random.randint(1, 10)
        result = calculator(op, a, b)
        print(f"  {op}({a}, {b}) = {result}")
    
    # Show statistics
    stats = tracker.get_tool_usage_stats()
    print("\nTool Usage Statistics:")
    for tool_name, tool_stats in stats.items():
        print(f"  {tool_name}:")
        print(f"    Count: {tool_stats['count']}")
        print(f"    Avg. Execution Time: {tool_stats['avg_execution_time']:.4f}s")
        print(f"    Success Rate: {tool_stats['success_rate']:.2%}")

# Main function to run examples
if __name__ == "__main__":
    print("LLM Proof of Work System - Basic Example")
    example_1_basic_tracking()
    print("\nExample completed!")
