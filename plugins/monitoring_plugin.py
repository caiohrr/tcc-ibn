"""
Network Monitoring Plugin for Mininet Topology Generator
This plugin adds monitoring capabilities to the network.
"""

from typing import Dict, Any, List
import sys
import os

# Add parent directory to path to import base classes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import ScriptGeneratorPlugin, Topology
except ImportError:
    # If main.py is not accessible, define minimal interface
    class ScriptGeneratorPlugin:
        def get_name(self): pass
        def get_version(self): pass
        def get_description(self): pass
        def generate_imports(self): pass
        def generate_pre_network_code(self, topology, params): pass
        def generate_post_network_code(self, topology, params): pass
        def generate_post_start_code(self, topology, params): pass


class NetworkMonitoringPlugin(ScriptGeneratorPlugin):
    """Plugin to add network monitoring capabilities."""
    
    def get_name(self) -> str:
        return "NetworkMonitoring"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Adds network monitoring and statistics collection capabilities"
    
    def generate_imports(self) -> List[str]:
        """Generate additional imports for monitoring."""
        return [
            "import threading",
            "import time",
            "from datetime import datetime"
        ]
    
    def generate_pre_network_code(self, topology: 'Topology', params: Dict[str, Any]) -> List[str]:
        """Generate monitoring setup code."""
        code = []
        
        if params.get("enable_monitoring", True):
            code.append("# Network Monitoring Plugin: Setup")
            code.append("monitoring_data = {'start_time': None, 'stats': {}}")
