# visualization.py
import json
import datetime
from typing import Dict, List, Any, Optional

class DataVisualizer:
    """
    Provides visualization capabilities for tool call data.
    
    This class contains methods to generate various visualization formats
    like JSON for charts, CSV data, and more.
    """
    
    def __init__(self, data_source: str = "tool_calls_db.json"):
        self.data_source = data_source
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from the source file"""
        try:
            with open(self.data_source, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"tool_calls": [], "metadata": {}}
    
    def refresh(self):
        """Reload data from the source"""
        self.data = self._load_data()
    
    def get_tool_usage_time_series(self, 
                                  interval: str = "hour",
                                  tool_names: Optional[List[str]] = None) -> Dict[str, List]:
        """
        Generate time series data for tool usage.
        
        Args:
            interval: Time grouping interval ('minute', 'hour', 'day')
            tool_names: Optional list of tool names to include (all if None)
            
        Returns:
            Dictionary with labels and datasets for time series visualization
        """
        if not self.data.get("tool_calls"):
            return {"labels": [], "datasets": []}
        
        # Filter tool calls if needed
        tool_calls = self.data["tool_calls"]
        if tool_names:
            tool_calls = [call for call in tool_calls if call["tool_name"] in tool_names]
        
        # Group by time interval
        time_buckets = {}
        tool_sets = {}
        
        for call in tool_calls:
            try:
                timestamp = datetime.datetime.fromisoformat(call["timestamp"])
                
                # Format the timestamp according to the interval
                if interval == "minute":
                    time_key = timestamp.strftime("%Y-%m-%d %H:%M")
                elif interval == "hour":
                    time_key = timestamp.strftime("%Y-%m-%d %H:00")
                else:  # day
                    time_key = timestamp.strftime("%Y-%m-%d")
                
                # Initialize the time bucket if needed
                if time_key not in time_buckets:
                    time_buckets[time_key] = {}
                
                # Initialize the tool count for this time bucket
                tool_name = call["tool_name"]
                if tool_name not in time_buckets[time_key]:
                    time_buckets[time_key][tool_name] = 0
                
                # Add to the count
                time_buckets[time_key][tool_name] += 1
                
                # Track unique tools
                tool_sets[tool_name] = True
            except (ValueError, KeyError):
                # Skip invalid entries
                continue
        
        # Sort time keys
        sorted_time_keys = sorted(time_buckets.keys())
        
        # Prepare the result
        unique_tools = sorted(tool_sets.keys())
        datasets = []
        
        for tool in unique_tools:
            data_points = []
            for time_key in sorted_time_keys:
                data_points.append(time_buckets[time_key].get(tool, 0))
            
            datasets.append({
                "label": tool,
                "data": data_points
            })
        
        return {
            "labels": sorted_time_keys,
            "datasets": datasets
        }
    
    def get_tool_execution_time_data(self) -> Dict[str, Any]:
        """
        Generate data for tool execution time visualization.
        
        Returns:
            Dictionary with labels and values for execution time visualization
        """
        if not self.data.get("tool_calls"):
            return {"labels": [], "values": []}
        
        # Calculate average execution time by tool
        execution_times = {}
        
        for call in self.data["tool_calls"]:
            if "execution_time" not in call:
                continue
                
            tool_name = call["tool_name"]
            if tool_name not in execution_times:
                execution_times[tool_name] = {"total": 0, "count": 0}
            
            execution_times[tool_name]["total"] += call["execution_time"]
            execution_times[tool_name]["count"] += 1
        
        # Calculate averages
        averages = {
            tool: data["total"] / data["count"]
            for tool, data in execution_times.items()
        }
        
        # Sort by average execution time
        sorted_tools = sorted(averages.keys(), key=lambda t: averages[t], reverse=True)
        
        return {
            "labels": sorted_tools,
            "values": [averages[tool] for tool in sorted_tools]
        }
    
    def get_tool_success_rate_data(self) -> Dict[str, Any]:
        """
        Generate data for tool success rate visualization.
        
        Returns:
            Dictionary with labels and values for success rate visualization
        """
        if not self.data.get("tool_calls"):
            return {"labels": [], "success": [], "failure": []}
        
        # Calculate success/failure counts by tool
        results = {}
        
        for call in self.data["tool_calls"]:
            tool_name = call["tool_name"]
            
            if tool_name not in results:
                results[tool_name] = {"success": 0, "failure": 0}
            
            # Assuming None results indicate failure
            if call.get("result") is None:
                results[tool_name]["failure"] += 1
            else:
                results[tool_name]["success"] += 1
        
        # Sort by success rate
        def success_rate(tool):
            tool_data = results[tool]
            total = tool_data["success"] + tool_data["failure"]
            return tool_data["success"] / total if total > 0 else 0
        
        sorted_tools = sorted(results.keys(), key=success_rate, reverse=True)
        
        return {
            "labels": sorted_tools,
            "success": [results[tool]["success"] for tool in sorted_tools],
            "failure": [results[tool]["failure"] for tool in sorted_tools]
        }
    
    def export_to_csv(self, output_file: str = "tool_calls_export.csv") -> str:
        """
        Export tool call data to CSV format.
        
        Args:
            output_file: Path to the output CSV file
            
        Returns:
            Path to the created CSV file
        """
        if not self.data.get("tool_calls"):
            return "No data to export"
        
        # Create CSV content
        csv_lines = ["timestamp,tool_name,execution_time,success"]
        
        for call in self.data["tool_calls"]:
            timestamp = call.get("timestamp", "")
            tool_name = call.get("tool_name", "")
            execution_time = call.get("execution_time", "")
            success = "true" if call.get("result") is not None else "false"
            
            csv_lines.append(f"{timestamp},{tool_name},{execution_time},{success}")
        
        # Write to file
        csv_content = "\n".join(csv_lines)
        with open(output_file, 'w') as f:
            f.write(csv_content)
        
        return output_file
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Generate a complete dashboard data set.
        
        Returns:
            Dictionary with all visualization data for a dashboard
        """
        return {
            "time_series": self.get_tool_usage_time_series(),
            "execution_times": self.get_tool_execution_time_data(),
            "success_rates": self.get_tool_success_rate_data(),
            "metadata": self.data.get("metadata", {}),
            "total_calls": len(self.data.get("tool_calls", []))
        }
