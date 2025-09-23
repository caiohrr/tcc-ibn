import json
import importlib
import inspect
import time
import threading
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Optional, Any, Protocol, Callable
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# ========================== Plugin System ==========================

class PluginInterface(ABC):
    """Base interface for all plugins."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the plugin name."""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Return the plugin version."""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Return the plugin description."""
        pass


class TopologyPlugin(PluginInterface):
    """Base class for topology manipulation plugins."""
    
    @abstractmethod
    def process_topology(self, topology: 'Topology', params: Dict[str, Any]) -> None:
        """Process the topology with given parameters."""
        pass


class ScriptGeneratorPlugin(PluginInterface):
    """Base class for script generation plugins."""
    
    @abstractmethod
    def generate_imports(self) -> List[str]:
        """Generate additional import statements."""
        pass
    
    @abstractmethod
    def generate_pre_network_code(self, topology: 'Topology', params: Dict[str, Any]) -> List[str]:
        """Generate code to be inserted before network creation."""
        pass
    
    @abstractmethod
    def generate_post_network_code(self, topology: 'Topology', params: Dict[str, Any]) -> List[str]:
        """Generate code to be inserted after network creation."""
        pass
    
    @abstractmethod
    def generate_post_start_code(self, topology: 'Topology', params: Dict[str, Any]) -> List[str]:
        """Generate code to be inserted after network start."""
        pass


class ComponentPlugin(PluginInterface):
    """Base class for custom network component plugins."""
    
    @abstractmethod
    def parse_component(self, component_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse custom component data."""
        pass
    
    @abstractmethod
    def generate_component_code(self, component: Dict[str, Any]) -> List[str]:
        """Generate Mininet code for the custom component."""
        pass


# ========================== Monitoring Plugin System ==========================

class MetricCollectorPlugin(PluginInterface):
    """Base class for metric collection plugins."""
    
    @abstractmethod
    def get_metric_name(self) -> str:
        """Return the name of the metric this plugin collects."""
        pass
    
    @abstractmethod
    def get_supported_intent_params(self) -> List[str]:
        """Return list of intent parameters this plugin can monitor."""
        pass
    
    @abstractmethod
    def collect_metric(self, topology: 'Topology', **kwargs) -> Dict[str, Any]:
        """Collect the metric from the network."""
        pass
    
    @abstractmethod
    def check_intent_compliance(self, metric_data: Dict[str, Any], 
                               intent_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if metric complies with intent parameters. Returns list of violations."""
        pass
    
    def get_collection_interval(self) -> int:
        """Return collection interval in seconds. Default: 30 seconds."""
        return 30


class ViolationAlert:
    """Represents a violation of network intent."""
    
    def __init__(self, violation_type: str, severity: str, description: str, 
                 metric_name: str, current_value: Any, expected_value: Any,
                 affected_components: List[str] = None, timestamp: datetime = None):
        self.violation_type = violation_type
        self.severity = severity  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
        self.description = description
        self.metric_name = metric_name
        self.current_value = current_value
        self.expected_value = expected_value
        self.affected_components = affected_components or []
        self.timestamp = timestamp or datetime.now()
        self.resolved = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'violation_type': self.violation_type,
            'severity': self.severity,
            'description': self.description,
            'metric_name': self.metric_name,
            'current_value': self.current_value,
            'expected_value': self.expected_value,
            'affected_components': self.affected_components,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class MonitoringManager:
    """Core monitoring system that coordinates metric collection and violation detection."""
    
    def __init__(self, plugin_manager: 'PluginManager', topology: 'Topology'):
        self.plugin_manager = plugin_manager
        self.topology = topology
        self.monitoring_plugins = []
        self.metrics_cache = {}
        self.violations = []
        self.monitoring_active = False
        self.monitoring_thread = None
        self.violation_callbacks = []
        
        # Load monitoring plugins
        self._load_monitoring_plugins()
    
    def _load_monitoring_plugins(self):
        """Load all available monitoring plugins."""
        for plugin in self.plugin_manager.loaded_plugins.values():
            if isinstance(plugin, MetricCollectorPlugin):
                self.monitoring_plugins.append(plugin)
                print(f"✓ Loaded monitoring plugin: {plugin.get_name()}")
    
    def add_violation_callback(self, callback: Callable[[ViolationAlert], None]):
        """Add callback function to be called when violations are detected."""
        self.violation_callbacks.append(callback)
    
    def start_monitoring(self, intent_params: Dict[str, Any] = None):
        """Start continuous monitoring of the network."""
        if self.monitoring_active:
            print("⚠️  Monitoring is already active.")
            return
        
        self.monitoring_active = True
        self.intent_params = intent_params or {}
        
        print(f"🔍 Starting network monitoring with {len(self.monitoring_plugins)} plugins...")
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        print("✓ Network monitoring started successfully.")
    
    def stop_monitoring(self):
        """Stop network monitoring."""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        print("🛑 Network monitoring stopped.")
    
    def _monitoring_loop(self):
        """Main monitoring loop running in separate thread."""
        plugin_timers = {plugin: time.time() for plugin in self.monitoring_plugins}
        
        while self.monitoring_active:
            current_time = time.time()
            
            for plugin in self.monitoring_plugins:
                # Check if it's time to collect metrics from this plugin
                if current_time - plugin_timers[plugin] >= plugin.get_collection_interval():
                    try:
                        # Collect metrics
                        metrics = plugin.collect_metric(self.topology)
                        metric_name = plugin.get_metric_name()
                        
                        # Update cache
                        self.metrics_cache[metric_name] = {
                            'data': metrics,
                            'timestamp': datetime.now(),
                            'plugin': plugin.get_name()
                        }
                        
                        # Check for violations
                        violations = plugin.check_intent_compliance(metrics, self.intent_params)
                        for violation_data in violations:
                            violation = ViolationAlert(**violation_data)
                            self.violations.append(violation)
                            
                            # Notify callbacks
                            for callback in self.violation_callbacks:
                                callback(violation)
                        
                        plugin_timers[plugin] = current_time
                        
                    except Exception as e:
                        print(f"❌ Error collecting metrics from {plugin.get_name()}: {e}")
            
            # Sleep for 1 second before next iteration
            time.sleep(1)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get all current cached metrics."""
        return self.metrics_cache.copy()
    
    def get_violations(self, severity_filter: str = None, resolved: bool = None) -> List[ViolationAlert]:
        """Get violations, optionally filtered by severity and resolution status."""
        filtered_violations = self.violations
        
        if severity_filter:
            filtered_violations = [v for v in filtered_violations if v.severity == severity_filter]
        
        if resolved is not None:
            filtered_violations = [v for v in filtered_violations if v.resolved == resolved]
        
        return filtered_violations
    
    def get_network_health_summary(self) -> Dict[str, Any]:
        """Get overall network health summary."""
        active_violations = [v for v in self.violations if not v.resolved]
        
        severity_counts = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0, 'CRITICAL': 0}
        for violation in active_violations:
            severity_counts[violation.severity] += 1
        
        # Calculate health score (0-100)
        critical_weight = severity_counts['CRITICAL'] * 25
        high_weight = severity_counts['HIGH'] * 15
        medium_weight = severity_counts['MEDIUM'] * 8
        low_weight = severity_counts['LOW'] * 3
        
        total_penalty = critical_weight + high_weight + medium_weight + low_weight
        health_score = max(0, 100 - total_penalty)
        
        return {
            'health_score': health_score,
            'total_violations': len(active_violations),
            'severity_breakdown': severity_counts,
            'monitoring_plugins': len(self.monitoring_plugins),
            'last_update': datetime.now().isoformat()
        }


class PluginManager:
    """Manages loading and execution of plugins."""
    
    def __init__(self, plugins_dir: Path = None):
        self.plugins_dir = plugins_dir or Path("plugins")
        self.loaded_plugins = {}
        self.topology_plugins = []
        self.script_plugins = []
        self.component_plugins = {}
        self.monitoring_plugins = []
        
        # Ensure plugins directory exists
        self.plugins_dir.mkdir(exist_ok=True)
        
        # Load all available plugins
        self._load_all_plugins()
    
    def _load_all_plugins(self):
        """Load all plugins from the plugins directory."""
        if not self.plugins_dir.exists():
            return
        
        # Add plugins directory to path
        import sys
        if str(self.plugins_dir) not in sys.path:
            sys.path.insert(0, str(self.plugins_dir))
        
        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            try:
                module_name = plugin_file.stem
                module = importlib.import_module(module_name)
                
                # Find all plugin classes in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, PluginInterface) and 
                        obj not in [PluginInterface, TopologyPlugin, ScriptGeneratorPlugin, 
                                   ComponentPlugin, MetricCollectorPlugin]):
                        
                        plugin_instance = obj()
                        plugin_name = plugin_instance.get_name()
                        self.loaded_plugins[plugin_name] = plugin_instance
                        
                        # Categorize plugin
                        if isinstance(plugin_instance, TopologyPlugin):
                            self.topology_plugins.append(plugin_instance)
                        elif isinstance(plugin_instance, ScriptGeneratorPlugin):
                            self.script_plugins.append(plugin_instance)
                        elif isinstance(plugin_instance, ComponentPlugin):
                            self.component_plugins[plugin_name] = plugin_instance
                        elif isinstance(plugin_instance, MetricCollectorPlugin):
                            self.monitoring_plugins.append(plugin_instance)
                        
                        print(f"✓ Loaded plugin: {plugin_name} v{plugin_instance.get_version()}")
            
            except Exception as e:
                print(f"✗ Failed to load plugin from {plugin_file.name}: {e}")
    
    def get_plugin(self, name: str) -> Optional[PluginInterface]:
        """Get a specific plugin by name."""
        return self.loaded_plugins.get(name)
    
    def execute_topology_plugins(self, topology: 'Topology', plugin_configs: List[Dict[str, Any]]):
        """Execute topology plugins based on configuration."""
        for config in plugin_configs:
            plugin_name = config.get("name")
            plugin_params = config.get("params", {})
            
            plugin = self.get_plugin(plugin_name)
            if plugin and isinstance(plugin, TopologyPlugin):
                print(f"  Executing topology plugin: {plugin_name}")
                plugin.process_topology(topology, plugin_params)
            else:
                print(f"  Warning: Topology plugin '{plugin_name}' not found or invalid")
    
    def get_script_generator_additions(self, topology: 'Topology', plugin_configs: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Get code additions from script generator plugins."""
        additions = {
            "imports": [],
            "pre_network": [],
            "post_network": [],
            "post_start": []
        }
        
        for config in plugin_configs:
            plugin_name = config.get("name")
            plugin_params = config.get("params", {})
            
            plugin = self.get_plugin(plugin_name)
            if plugin and isinstance(plugin, ScriptGeneratorPlugin):
                additions["imports"].extend(plugin.generate_imports())
                additions["pre_network"].extend(plugin.generate_pre_network_code(topology, plugin_params))
                additions["post_network"].extend(plugin.generate_post_network_code(topology, plugin_params))
                additions["post_start"].extend(plugin.generate_post_start_code(topology, plugin_params))
        
        return additions


# ========================== Core Topology Class ==========================

class Topology:
    """Represents the network topology, read from a JSON file."""
    
    def __init__(self, json_data: Dict[str, Any], plugin_manager: PluginManager = None):
        self._json_data = json_data
        self.plugin_manager = plugin_manager or PluginManager()
        
        components = self._json_data.get("COMPONENTS", {})
        
        self.id = self._json_data.get("ID", "unknown_topology").lower()
        self.version = self._json_data.get("VERSION", "N/A")
        self.description = self._json_data.get("DESCRIPTION", "No description provided.")
        
        # Parse standard components
        self.hosts = self._parse_hosts(components)
        self.switches = self._parse_switches(components)
        self.controllers = self._parse_controllers(components)
        self.connections = self._parse_connections()
        
        # Parse custom components via plugins
        self.custom_components = self._parse_custom_components(components)
        
        # Get plugin configurations
        self.plugins_config = self._json_data.get("PLUGINS", [])
        
        # Get monitoring/intent configurations
        self.intent_params = self._json_data.get("INTENT", {})
        
        # Initialize monitoring manager
        self.monitoring_manager = None
        
        # Execute topology plugins
        if self.plugins_config:
            print("\nExecuting topology plugins...")
            self.plugin_manager.execute_topology_plugins(self, self.plugins_config)
    
    def _parse_hosts(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        parsed_hosts = []
        hosts_data = components.get("HOSTS", [])
        for host in hosts_data:
            host_info = {
                "id": host.get("ID"),
                "ip": host.get("IP"),
                "mac": host.get("MAC")
            }
            # Include any additional parameters
            for key, value in host.items():
                if key not in ["ID", "IP", "MAC"]:
                    host_info[key.lower()] = value
            
            if host_info["id"]:
                parsed_hosts.append(host_info)
        return parsed_hosts
    
    def _parse_switches(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        return components.get("SWITCHES", [])
    
    def _parse_controllers(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        return components.get("CONTROLLERS", [])
    
    def _parse_connections(self) -> List[Dict[str, Any]]:
        return self._json_data.get("CONNECTIONS", [])
    
    def _parse_custom_components(self, components: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Parse custom components using registered plugins."""
        custom_components = {}
        
        for component_type, component_data in components.items():
            if component_type not in ["HOSTS", "SWITCHES", "CONTROLLERS"]:
                # Check if there's a plugin for this component type
                if component_type in self.plugin_manager.component_plugins:
                    plugin = self.plugin_manager.component_plugins[component_type]
                    custom_components[component_type] = []
                    
                    if isinstance(component_data, list):
                        for item in component_data:
                            parsed = plugin.parse_component(item)
                            custom_components[component_type].append(parsed)
                    else:
                        parsed = plugin.parse_component(component_data)
                        custom_components[component_type].append(parsed)
        
        return custom_components
    
    def initialize_monitoring(self):
        """Initialize the monitoring system for this topology."""
        if self.monitoring_manager is None:
            self.monitoring_manager = MonitoringManager(self.plugin_manager, self)
            print("✓ Monitoring system initialized.")
        return self.monitoring_manager
    
    def start_monitoring(self):
        """Start monitoring this topology."""
        if self.monitoring_manager is None:
            self.initialize_monitoring()
        
        self.monitoring_manager.start_monitoring(self.intent_params)
    
    def stop_monitoring(self):
        """Stop monitoring this topology."""
        if self.monitoring_manager:
            self.monitoring_manager.stop_monitoring()
    
    def print_details(self):
        """Print topology details in an organized manner."""
        print(f"\n--- Topology Details: {self.id.capitalize()} (v{self.version}) ---")
        print(f"Description: {self.description}\n")
        
        print("Hosts:")
        if not self.hosts:
            print("  None")
        for host in self.hosts:
            ip_info = f", IP: {host['ip']}" if host.get('ip') else ""
            mac_info = f", MAC: {host['mac']}" if host.get('mac') else ""
            extra_info = ", ".join([f"{k.upper()}: {v}" for k, v in host.items() 
                                   if k not in ['id', 'ip', 'mac']])
            if extra_info:
                extra_info = f", {extra_info}"
            print(f"  - ID: {host['id']}{ip_info}{mac_info}{extra_info}")
        
        print("\nSwitches:")
        if not self.switches:
            print("  None")
        for switch in self.switches:
            params_info = f", PARAMS: {switch.get('PARAMS', {})}"
            print(f"  - ID: {switch.get('ID')}, TYPE: {switch.get('TYPE', 'Default')}{params_info}")
        
        print("\nControllers:")
        if not self.controllers:
            print("  None")
        for controller in self.controllers:
            params_info = f", PARAMS: {controller.get('PARAMS', {})}"
            print(f"  - ID: {controller.get('ID')}, TYPE: {controller.get('TYPE', 'Default')}{params_info}")
        
        print("\nConnections:")
        if not self.connections:
            print("  None")
        for conn in self.connections:
            endpoints = conn.get('ENDPOINTS', ['N/A', 'N/A'])
            params_info = f", PARAMS: {conn.get('PARAMS', {})}"
            print(f"  - ENDPOINTS: {endpoints[0]} <--> {endpoints[1]}{params_info}")
        
        # Print custom components
        for component_type, components in self.custom_components.items():
            print(f"\n{component_type}:")
            if not components:
                print("  None")
            for component in components:
                print(f"  - {component}")
        
        # Print plugin configurations
        if self.plugins_config:
            print("\nConfigured Plugins:")
            for plugin in self.plugins_config:
                print(f"  - {plugin.get('name')} with params: {plugin.get('params', {})}")
        
        # Print intent parameters
        if self.intent_params:
            print("\nIntent Parameters:")
            for param, value in self.intent_params.items():
                print(f"  - {param}: {value}")
        
        print("\n" + "-" * 40)


# ========================== Script Generator ==========================

class MininetScriptGenerator:
    """Generates Mininet Python scripts from topology."""
    
    def __init__(self, plugin_manager: PluginManager = None):
        self.plugin_manager = plugin_manager or PluginManager()
    
    def generate(self, topology: Topology, output_file: str = "topology.py"):
        """Generate a Mininet Python script based on the provided topology."""
        
        # Default to OVSKernelSwitch for compatibility
        switch_class = "OVSKernelSwitch"
        has_controllers = bool(topology.controllers)
        has_monitoring = bool(topology.intent_params)
        
        # Validate switch types
        for switch in topology.switches:
            s_type = switch.get("TYPE")
            if s_type and s_type not in ["OVSKernelSwitch", "UserSwitch"]:
                print(f"Warning: Switch type '{s_type}' will be ignored. Using '{switch_class}' as default.")
        
        # Get plugin additions
        plugin_additions = self.plugin_manager.get_script_generator_additions(
            topology, topology.plugins_config
        )
        
        with open(output_file, "w+", encoding='utf-8') as mn_file:
            # Write header and imports
            self._write_header(mn_file, topology)
            self._write_imports(mn_file, plugin_additions["imports"], has_monitoring)
            
            # Write topology function
            mn_file.write(f"def {topology.id}_topology():\n\n")
            mn_file.write("\t'Creates and configures the network topology.'\n")
            
            # Pre-network plugin code
            for line in plugin_additions["pre_network"]:
                mn_file.write(f"\t{line}\n")
            if plugin_additions["pre_network"]:
                mn_file.write("\n")
            
            # Network initialization
            controller_param = "Controller" if has_controllers else "None"
            wait_connected_param = "True" if has_controllers else "False"
            mn_file.write(f"\tnet = Mininet(controller={controller_param}, switch={switch_class}, "
                         f"link=TCLink, waitConnected={wait_connected_param})\n\n")
            
            # Post-network plugin code
            for line in plugin_additions["post_network"]:
                mn_file.write(f"\t{line}\n")
            if plugin_additions["post_network"]:
                mn_file.write("\n")
            
            # Add standard components
            self._write_controllers(mn_file, topology)
            self._write_hosts(mn_file, topology)
            self._write_switches(mn_file, topology)
            self._write_links(mn_file, topology)
            
            # Add custom components via plugins
            self._write_custom_components(mn_file, topology)
            
            # Start network
            mn_file.write("\tinfo('*** Starting network\\n')\n")
            mn_file.write("\tnet.start()\n\n")
            
            # Post-start plugin code
            for line in plugin_additions["post_start"]:
                mn_file.write(f"\t{line}\n")
            if plugin_additions["post_start"]:
                mn_file.write("\n")
            
            # Configure OVS for standalone mode if no controller
            if not has_controllers:
                self._write_standalone_config(mn_file, topology)
            
            # Add monitoring initialization if intent parameters are present
            if has_monitoring:
                self._write_monitoring_initialization(mn_file, topology)
            
            # CLI and cleanup
            mn_file.write("\tinfo('*** Running CLI\\n')\n")
            mn_file.write("\tCLI(net)\n\n")
            
            # Stop monitoring before stopping network
            if has_monitoring:
                mn_file.write("\tinfo('*** Stopping monitoring\\n')\n")
                mn_file.write("\tif 'monitoring_manager' in locals():\n")
                mn_file.write("\t\tmonitoring_manager.stop_monitoring()\n\n")
            
            mn_file.write("\tinfo('*** Stopping network\\n')\n")
            mn_file.write("\tnet.stop()\n\n")
            
            # Main block
            mn_file.write("if __name__ == '__main__':\n")
            mn_file.write("\tsetLogLevel('info')\n")
            mn_file.write(f"\t{topology.id}_topology()\n")
    
    def _write_header(self, file, topology):
        file.write(
            '"""\n'
            'Mininet script generated automatically.\n'
            f'Topology: {topology.id.capitalize()}\n'
            f'Version: {topology.version}\n'
            f'Description: {topology.description}\n'
            '"""\n'
        )
    
    def _write_imports(self, file, additional_imports, has_monitoring):
        file.write(
            "from mininet.net import Mininet\n"
            "from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch\n"
            "from mininet.cli import CLI\n"
            "from mininet.log import setLogLevel, info\n"
            "from mininet.link import TCLink\n"
        )
        
        # Add monitoring imports if needed
        if has_monitoring:
            file.write("import sys\n")
            file.write("import os\n")
            file.write("import threading\n")
            file.write("import time\n")
            file.write("# Note: You'll need to ensure monitoring modules are available\n")
            file.write("# from monitoring_system import MonitoringManager, PluginManager\n")
        
        # Add plugin imports
        for import_stmt in additional_imports:
            file.write(f"{import_stmt}\n")
        
        file.write("\n")
    
    def _write_controllers(self, file, topology):
        if topology.controllers:
            file.write(f"\tinfo('*** Adding {len(topology.controllers)} controllers\\n')\n")
            for controller in topology.controllers:
                cid = controller.get('ID', 'c0')
                ctype = controller.get('TYPE', 'Controller')
                params = controller.get('PARAMS', {})
                
                if ctype == 'RemoteController':
                    ip = params.get('IP', '127.0.0.1')
                    port = params.get('PORT', 6653)
                    file.write(f"\t{cid} = net.addController('{cid}', controller=RemoteController, "
                             f"ip='{ip}', port={port})\n")
                else:
                    file.write(f"\t{cid} = net.addController('{cid}')\n")
            file.write("\n")
        else:
            file.write("\tinfo('*** No controller defined. OVS will be configured for standalone mode.\\n')\n\n")
    
    def _write_hosts(self, file, topology):
        file.write(f"\tinfo('*** Adding {len(topology.hosts)} hosts\\n')\n")
        for host in topology.hosts:
            params_list = [f"'{host['id']}'"]
            if host.get('ip'):
                params_list.append(f"ip='{host['ip']}'")
            if host.get('mac'):
                params_list.append(f"mac='{host['mac']}'")
            
            # Add any additional parameters
            for key, value in host.items():
                if key not in ['id', 'ip', 'mac']:
                    if isinstance(value, str):
                        params_list.append(f"{key}='{value}'")
                    else:
                        params_list.append(f"{key}={value}")
            
            file.write(f"\t{host['id']} = net.addHost({', '.join(params_list)})\n")
        file.write("\n")
    
    def _write_switches(self, file, topology):
        file.write(f"\tinfo('*** Adding {len(topology.switches)} switches\\n')\n")
        for switch in topology.switches:
            sid = switch.get('ID', 's1')
            file.write(f"\t{sid} = net.addSwitch('{sid}')\n")
        file.write("\n")
    
    def _write_links(self, file, topology):
        file.write(f"\tinfo('*** Creating {len(topology.connections)} links\\n')\n")
        param_map = {'bandwidth': 'bw'}
        
        for conn in topology.connections:
            endpoints = conn.get('ENDPOINTS')
            params = conn.get('PARAMS', {})
            
            if endpoints and len(endpoints) == 2:
                param_list = []
                for k, v in params.items():
                    param_name = param_map.get(k.lower(), k.lower())
                    if isinstance(v, str):
                        param_list.append(f"{param_name}='{v}'")
                    else:
                        param_list.append(f"{param_name}={v}")
                
                link_params_str = ", ".join(param_list)
                if link_params_str:
                    file.write(f"\tnet.addLink({endpoints[0]}, {endpoints[1]}, {link_params_str})\n")
                else:
                    file.write(f"\tnet.addLink({endpoints[0]}, {endpoints[1]})\n")
        file.write("\n")
    
    def _write_custom_components(self, file, topology):
        """Write custom components using plugins."""
        for component_type, components in topology.custom_components.items():
            if component_type in self.plugin_manager.component_plugins:
                plugin = self.plugin_manager.component_plugins[component_type]
                
                file.write(f"\tinfo('*** Adding {len(components)} {component_type}\\n')\n")
                for component in components:
                    code_lines = plugin.generate_component_code(component)
                    for line in code_lines:
                        file.write(f"\t{line}\n")
                file.write("\n")
    
    def _write_standalone_config(self, file, topology):
        file.write("\tinfo('*** Configuring switches for standalone mode\\n')\n")
        for switch in topology.switches:
            sid = switch.get('ID', 's1')
            file.write(f"\tnet.get('{sid}').cmd('ovs-ofctl add-flow {sid} \"priority=0,actions=normal\"')\n")
        file.write("\n")
    
    def _write_monitoring_initialization(self, file, topology):
        """Write monitoring system initialization code."""
        file.write("\t# Initialize monitoring system (if available)\n")
        file.write("\ttry:\n")
        file.write("\t\t# This requires the monitoring system to be available\n")
        file.write("\t\t# Uncomment the next lines if you have the monitoring system installed\n")
        file.write("\t\t# from main import PluginManager, MonitoringManager, Topology\n")
        file.write("\t\t# import json\n")
        file.write("\t\t\n")
        file.write("\t\t# topology_data = {...}  # Your topology JSON data\n")
        file.write("\t\t# plugin_manager = PluginManager()\n")
        file.write("\t\t# topology_obj = Topology(topology_data, plugin_manager)\n")
        file.write("\t\t# monitoring_manager = MonitoringManager(plugin_manager, topology_obj)\n")
        file.write("\t\t\n")
        
        # Write intent parameters as comments for reference
        if topology.intent_params:
            file.write("\t\t# Intent parameters defined:\n")
            for param, value in topology.intent_params.items():
                file.write(f"\t\t# {param}: {value}\n")
        
        file.write("\t\t\n")
        file.write("\t\t# monitoring_manager.start_monitoring(intent_params)\n")
        file.write("\t\tinfo('*** Monitoring system would be initialized here\\n')\n")
        file.write("\texcept ImportError:\n")
        file.write("\t\tinfo('*** Monitoring system not available\\n')\n")
        file.write("\n")


# ========================== Utility Functions ==========================

def find_matching_file(dir_path: Path, prefix: str) -> Optional[Path]:
    """Find the first file in the directory that starts with the prefix."""
    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    matching_file = next((f for f in files if f.name.lower().startswith(prefix.lower())), None)
    if matching_file is None:
        raise FileNotFoundError(f"No file found starting with '{prefix}' in {dir_path}")
    return matching_file


def load_json_file(file_path: Path) -> Dict:
    """Load data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def violation_alert_handler(violation: ViolationAlert):
    """Default violation alert handler."""
    severity_icons = {
        'LOW': '🟡',
        'MEDIUM': '🟠', 
        'HIGH': '🔴',
        'CRITICAL': '🚨'
    }
    
    icon = severity_icons.get(violation.severity, '❓')
    print(f"{icon} {violation.severity} VIOLATION: {violation.description}")
    print(f"   Metric: {violation.metric_name}")
    print(f"   Current: {violation.current_value}, Expected: {violation.expected_value}")
    print(f"   Affected: {', '.join(violation.affected_components)}")
    print(f"   Time: {violation.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)


# ========================== Enhanced Main Function ==========================

def main():
    """Main function to execute the script."""
    try:
        # Initialize plugin manager
        plugin_manager = PluginManager()
        
        # Get topology file
        dir_path = Path() / "topologies"
        prefix = input("Enter topology name: ")
        
        matching_file = find_matching_file(dir_path, prefix)
        print(f"Found file: {matching_file}\n")
        
        # Load and parse topology
        json_data = load_json_file(matching_file)
        topology = Topology(json_data, plugin_manager)
        topology.print_details()
        
        # Generate Mininet script
        generator = MininetScriptGenerator(plugin_manager)
        output_filename = f"{topology.id}_net.py"
        generator.generate(topology, output_filename)
        
        print(f"\n✅ Mininet script successfully generated: '{output_filename}'")
        
        # Ask if user wants to start monitoring
        if topology.intent_params:
            start_monitoring = input("\nStart monitoring system? (y/n): ").lower().strip()
            
            if start_monitoring == 'y':
                print("\n" + "=" * 60)
                print("STARTING MONITORING SYSTEM")
                print("=" * 60)
                
                # Initialize monitoring
                monitoring_manager = topology.initialize_monitoring()
                monitoring_manager.add_violation_callback(violation_alert_handler)
                
                # Start monitoring
                topology.start_monitoring()
                
                try:
                    print("🔍 Monitoring active. Press Ctrl+C to stop monitoring and continue...")
                    print("💡 TIP: Run 'sudo python {}' in another terminal to test the network".format(output_filename))
                    
                    # Keep monitoring until user stops it
                    while True:
                        time.sleep(5)
                        
                        # Print health summary every 30 seconds
                        if int(time.time()) % 30 == 0:
                            health = monitoring_manager.get_network_health_summary()
                            print(f"\n📊 Network Health: {health['health_score']}/100 | "
                                  f"Violations: {health['total_violations']} | "
                                  f"Time: {datetime.now().strftime('%H:%M:%S')}")
                
                except KeyboardInterrupt:
                    print("\n\n🛑 Monitoring stopped by user.")
                    topology.stop_monitoring()
                    
                    # Show final summary
                    violations = monitoring_manager.get_violations(resolved=False)
                    if violations:
                        print(f"\n📋 Final Summary: {len(violations)} unresolved violations")
                        for i, violation in enumerate(violations[-5:], 1):  # Show last 5
                            print(f"  {i}. {violation.severity}: {violation.description}")
                    else:
                        print("\n✅ No active violations detected.")
        
        else:
            print("\n💡 No intent parameters defined. Add an 'INTENT' section to your topology JSON to enable monitoring.")
        
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"⚠️ Error generating script: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
