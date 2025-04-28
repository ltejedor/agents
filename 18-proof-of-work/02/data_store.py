# data_store.py
import json
import datetime
from typing import Dict, List, Any, Optional

class DataStore:
    """
    Handles the storage and retrieval of tool call data.
    
    This class provides an abstraction over the storage mechanism,
    allowing for different backends to be used.
    """
    
    def __init__(self, storage_path: str = "tool_calls_db.json"):
        self.storage_path = storage_path
        self.data = self._load()
        
    def _load(self) -> Dict[str, Any]:
        """Load data from storage"""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "tool_calls": [],
                "metadata": {
                    "created_at": datetime.datetime.now().isoformat(),
                    "updated_at": datetime.datetime.now().isoformat(),
                    "version": "1.0.0"
                }
            }
    
    def _save(self):
        """Save data to storage"""
        self.data["metadata"]["updated_at"] = datetime.datetime.now().isoformat()
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_tool_call(self, tool_call_data: Dict[str, Any]):
        """
        Add a tool call to the data store.
        
        Args:
            tool_call_data: Dictionary containing tool call data
        """
        self.data["tool_calls"].append({
            **tool_call_data,
            "id": len(self.data["tool_calls"]) + 1
        })
        self._save()
    
    def get_tool_calls(self, 
                      tool_name: Optional[str] = None, 
                      start_time: Optional[datetime.datetime] = None,
                      end_time: Optional[datetime.datetime] = None,
                      limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Retrieve tool calls from the data store with optional filtering.
        
        Args:
            tool_name: Filter by tool name
            start_time: Filter by start time
            end_time: Filter by end time
            limit: Maximum number of results to return
            
        Returns:
            List of tool call dictionaries
        """
        results = self.data["tool_calls"]
        
        if tool_name:
            results = [r for r in results if r["tool_name"] == tool_name]
        
        if start_time:
            start_str = start_time.isoformat()
            results = [r for r in results if r["timestamp"] >= start_str]
        
        if end_time:
            end_str = end_time.isoformat()
            results = [r for r in results if r["timestamp"] <= end_str]
        
        if limit:
            results = results[:limit]
        
        return results
    
    def clear(self):
        """Clear all data from the store"""
        self.data["tool_calls"] = []
        self._save()
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the data in the store.
        
        Returns:
            Dictionary of statistics
        """
        tool_calls = self.data["tool_calls"]
        
        # Count by tool name
        tool_counts = {}
        for call in tool_calls:
            tool_name = call["tool_name"]
            if tool_name not in tool_counts:
                tool_counts[tool_name] = 0
            tool_counts[tool_name] += 1
        
        # Calculate average execution time by tool
        execution_times = {}
        for call in tool_calls:
            if "execution_time" not in call:
                continue
                
            tool_name = call["tool_name"]
            if tool_name not in execution_times:
                execution_times[tool_name] = {"total": 0, "count": 0, "avg": 0}
            
            execution_times[tool_name]["total"] += call["execution_time"]
            execution_times[tool_name]["count"] += 1
            execution_times[tool_name]["avg"] = (
                execution_times[tool_name]["total"] / execution_times[tool_name]["count"]
            )
        
        return {
            "total_calls": len(tool_calls),
            "tool_counts": tool_counts,
            "execution_times": {k: v["avg"] for k, v in execution_times.items()}
        }
