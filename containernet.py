import json
import importlib
import inspect
from pathlib import Path
from typing import List, Dict, Optional, Any, Protocol
from abc import ABC, abstractmethod

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


class PluginManager:
    """Manages loading and execution of plugins."""
    
    def __init__(self, plugins_dir: Path = None):
        self.plugins_dir = plugins_dir or Path("plugins")
        self.loaded_plugins = {}
        self.topology_plugins = []
        self.script_plugins = []
        self.component_plugins = {}
        
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
                        obj not in [PluginInterface, TopologyPlugin, ScriptGeneratorPlugin, ComponentPlugin]):
                        
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
            self._write_imports(mn_file, plugin_additions["imports"])
            
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
            mn_file.write(f"\tnet = Containernet(controller={controller_param}, switch={switch_class}, "
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
            
            # CLI and cleanup
            mn_file.write("\tinfo('*** Running CLI\\n')\n")
            mn_file.write("\tCLI(net)\n\n")
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
    
    def _write_imports(self, file, additional_imports):
        file.write(
                "from mininet.net import Containernet\n"
                "from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch, Docker\n"
                "from mininet.cli import CLI\n"
                "from mininet.log import setLogLevel, info\n"
                "from mininet.link import TCLink\n"
        )

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
                    file.write(f"\t{cid} = net.addController('{cid}', controller=Controller, "
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

            file.write(f"\t{host['id']} = net.addDocker({', '.join(params_list)}, dimage=\"ubuntu:trusty\")\n")
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


# ========================== Main Function ==========================

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

    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"❌ Error generating script: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
