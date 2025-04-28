# api.py
from typing import Dict, List, Any, Optional
import datetime
import json

class LLMProofOfWorkAPI:
    """
    API for the LLM Proof of Work system.
    
    This class provides the interface for interacting with the system,
    including configuration, data access, and visualization.
    """
    
    def __init__(self, 
                config_path: str = "pow_config.json",
                data_store_path: str = "tool_calls_db.json"):
        self.config_path = config_path
        self.data_store_path = data_store_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "tools_to_track": {},  # Tool name -> whether to track
                "visualization": {
                    "default_interval": "hour",
                    "theme": "light"
                },
                "storage": {
                    "path": self.data_store_path,
                    "max_entries": 10000
                }
            }
    
    def _save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def configure_tool_tracking(self, **tool_configs):
        """
        Configure which tools to track.
        
        Args:
            **tool_configs: Tool name -> whether to track
                e.g., configure_tool_tracking(web_search=True, calculator=False)
        """
        self.config["tools_to_track"].update(tool_configs)
        self._save_config()
        
        # Return the updated configuration
        return self.config["tools_to_track"]
    
    def set_visualization_options(self, **options):
        """
        Set visualization options.
        
        Args:
            **options: Visualization options to set
                e.g., set_visualization_options(theme="dark", default_interval="day")
        """
        self.config["visualization"].update(options)
        self._save_config()
        
        # Return the updated visualization options
        return self.config["visualization"]
    
    def set_storage_options(self, **options):
        """
        Set storage options.
        
        Args:
            **options: Storage options to set
                e.g., set_storage_options(max_entries=5000)
        """
        self.config["storage"].update(options)
        self._save_config()
        
        # Return the updated storage options
        return self.config["storage"]
    
    def get_tool_tracking_config(self) -> Dict[str, bool]:
        """
        Get the current tool tracking configuration.
        
        Returns:
            Dictionary mapping tool names to whether they are being tracked
        """
        return self.config["tools_to_track"]
    
    def get_visualization_options(self) -> Dict[str, Any]:
        """
        Get the current visualization options.
        
        Returns:
            Dictionary of visualization options
        """
        return self.config["visualization"]
    
    def get_storage_options(self) -> Dict[str, Any]:
        """
        Get the current storage options.
        
        Returns:
            Dictionary of storage options
        """
        return self.config["storage"]
        
    def get_dashboard_data(self, 
                          time_interval: Optional[str] = None,
                          tool_filter: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get data for the visualization dashboard.
        
        Args:
            time_interval: Optional time interval override
            tool_filter: Optional list of tools to include
            
        Returns:
            Dictionary of dashboard data
        """
        from visualization import DataVisualizer
        
        visualizer = DataVisualizer(data_source=self.data_store_path)
        dashboard_data = visualizer.get_dashboard_data()
        
        # Override time interval if specified
        if time_interval:
            dashboard_data["time_series"] = visualizer.get_tool_usage_time_series(
                interval=time_interval,
                tool_names=tool_filter
            )
        
        return dashboard_data
    
    def export_data(self, 
                   format: str = "csv",
                   output_path: Optional[str] = None) -> str:
        """
        Export tool call data.
        
        Args:
            format: Export format ('csv', 'json')
            output_path: Optional output path
            
        Returns:
            Path to the exported file
        """
        if format not in ["csv", "json"]:
            return f"Unsupported export format: {format}"
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_path = f"tool_calls_export_{timestamp}.{format}"
        output_path = output_path or default_path
        
        if format == "csv":
            from visualization import DataVisualizer
            visualizer = DataVisualizer(data_source=self.data_store_path)
            return visualizer.export_to_csv(output_file=output_path)
        else:  # json
            try:
                with open(self.data_store_path, 'r') as f:
                    data = json.load(f)
                
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2)
                
                return output_path
            except Exception as e:
                return f"Error exporting data: {str(e)}"
