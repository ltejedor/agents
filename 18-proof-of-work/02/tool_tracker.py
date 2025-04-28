# tool_tracker.py
import json
import datetime
from typing import Dict, List, Any, Optional, Callable

class ToolCall:
    """Represents a single tool call made by an LLM."""
    
    def __init__(self, 
                 tool_name: str, 
                 arguments: Dict[str, Any], 
                 result: Any = None, 
                 timestamp: Optional[datetime.datetime] = None):
        self.tool_name = tool_name
        self.arguments = arguments
        self.result = result
        self.timestamp = timestamp or datetime.datetime.now()
        self.execution_time = None  # Will be set when result is received
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "tool_name": self.tool_name,
            "arguments": self.arguments,
            "result": self.result,
            "timestamp": self.timestamp.isoformat(),
            "execution_time": self.execution_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ToolCall':
        """Create a ToolCall instance from a dictionary"""
        instance = cls(
            tool_name=data["tool_name"],
            arguments=data["arguments"],
            result=data.get("result"),
            timestamp=datetime.datetime.fromisoformat(data["timestamp"])
        )
        instance.execution_time = data.get("execution_time")
        return instance

class ToolTracker:
    """
    Tracks tool calls made by an LLM.
    
    This class provides middleware functionality to intercept tool calls,
    log them, and allow for analysis and visualization.
    """
    
    def __init__(self, save_path: str = "tool_calls.json"):
        self.tool_calls: List[ToolCall] = []
        self.save_path = save_path
        self.filters: Dict[str, bool] = {}  # Tool name -> whether to track
        
    def track_tool(self, func: Callable) -> Callable:
        """
        Decorator to track tool calls.
        
        Usage:
            @tracker.track_tool
            def my_tool(arg1, arg2):
                return result
        """
        def wrapper(*args, **kwargs):
            # Create a tool call record
            tool_name = func.__name__
            
            # Skip if this tool is filtered out
            if tool_name in self.filters and not self.filters[tool_name]:
                return func(*args, **kwargs)
            
            arguments = {
                **{f"arg{i}": arg for i, arg in enumerate(args)},
                **kwargs
            }
            
            tool_call = ToolCall(tool_name, arguments)
            start_time = datetime.datetime.now()
            
            try:
                # Execute the actual tool function
                result = func(*args, **kwargs)
                tool_call.result = result
                return result
            finally:
                # Record execution time
                end_time = datetime.datetime.now()
                tool_call.execution_time = (end_time - start_time).total_seconds()
                
                # Store the tool call
                self.tool_calls.append(tool_call)
                self.save()
        
        return wrapper
    
    def filter_tools(self, **filters: Dict[str, bool]):
        """
        Set which tools to track.
        
        Args:
            **filters: Tool name -> whether to track
                e.g., filter_tools(web_search=True, calculator=False)
        """
        self.filters.update(filters)
    
    def save(self):
        """Save the current tool calls to a file"""
        data = [tool_call.to_dict() for tool_call in self.tool_calls]
        with open(self.save_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load tool calls from a file"""
        try:
            with open(self.save_path, 'r') as f:
                data = json.load(f)
            self.tool_calls = [ToolCall.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tool_calls = []
    
    def get_tool_usage_stats(self) -> Dict[str, Dict[str, Any]]:
        """
        Get statistics about tool usage.
        
        Returns:
            Dictionary mapping tool names to statistics about their usage.
        """
        stats = {}
        
        for tool_call in self.tool_calls:
            tool_name = tool_call.tool_name
            
            if tool_name not in stats:
                stats[tool_name] = {
                    "count": 0,
                    "avg_execution_time": 0,
                    "total_execution_time": 0,
                    "success_rate": 0,
                    "failures": 0
                }
            
            stats[tool_name]["count"] += 1
            
            if tool_call.execution_time is not None:
                stats[tool_name]["total_execution_time"] += tool_call.execution_time
                stats[tool_name]["avg_execution_time"] = (
                    stats[tool_name]["total_execution_time"] / stats[tool_name]["count"]
                )
            
            # Assuming None results indicate failure
            if tool_call.result is None:
                stats[tool_name]["failures"] += 1
            
            stats[tool_name]["success_rate"] = (
                (stats[tool_name]["count"] - stats[tool_name]["failures"]) / 
                stats[tool_name]["count"]
            )
            
        return stats
