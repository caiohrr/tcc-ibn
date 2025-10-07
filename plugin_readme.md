# Mininet Topology Generator - Plugin System Documentation

## Overview

The refactored Mininet Topology Generator now supports a powerful plugin-based architecture that allows you to extend functionality without modifying the core code. Plugins can add new features, custom components, and modify the generated Mininet scripts.

## Directory Structure

```
project/
├── main.py                 # Core application with plugin system
├── topologies/            # JSON topology files
│   └── *.json
└── plugins/               # Plugin directory (auto-created)
    ├── qos_plugin.py
    ├── monitoring_plugin.py
    └── nat_plugin.py
```

## Plugin Types

### 1. **Topology Plugins** (`TopologyPlugin`)
- Modify the topology object after it's loaded
- Add computed values or transform existing data
- Example use cases: Auto-IP assignment, topology validation

### 2. **Script Generator Plugins** (`ScriptGeneratorPlugin`)
- Add custom code to the generated Mininet script
- Insert imports, functions, and configuration code
- Example use cases: QoS configuration, monitoring, custom protocols

### 3. **Component Plugins** (`ComponentPlugin`)
- Add support for custom network components
- Parse custom component types from JSON
- Generate Mininet code for custom components
- Example use cases: NAT devices, firewalls, load balancers

## Creating a Plugin

### Basic Plugin Structure

```python
from typing import Dict, Any, List
from main import ScriptGeneratorPlugin, Topology

class MyCustomPlugin(ScriptGeneratorPlugin):
    def get_name(self) -> str:
        return "MyPlugin"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def get_description(self) -> str:
        return "Description of what my plugin does"
    
    def generate_imports(self) -> List[str]:
        return ["import some_module"]
    
    def generate_pre_network_code(self, topology: Topology, params: Dict[str, Any]) -> List[str]:
        # Code to insert before network creation
        return ["# Pre-network code"]
    
    def generate_post_network_code(self, topology: Topology, params: Dict[str, Any]) -> List[str]:
        # Code to insert after network creation
        return ["# Post-network code"]
    
    def generate_post_start_code(self, topology: Topology, params: Dict[str, Any]) -> List[str]:
        # Code to insert after network starts
        return ["# Post-start code"]
```

## Using Plugins in JSON Topology

### Adding Plugin Configuration

In your topology JSON file, add a `PLUGINS` section:

```json
{
    "ID": "MyTopology",
    "VERSION": "1.0",
    "DESCRIPTION": "Topology with plugins",
    
    "PLUGINS": [
        {
            "name": "QoS",
            "params": {
                "enable_htb": true,
                "default_queue_size": 2000,
                "enable_ecn": true,
                "rules": [...]
            }
        },
        {
            "name": "NetworkMonitoring",
            "params": {
                "enable_monitoring": true,
                "interval": 10,
                "duration": 300
            }
        }
    ],
    
    "COMPONENTS": {
        ...
    }
}
```

### Adding Custom Components

For component plugins, add new component types directly to the `COMPONENTS` section:

```json
{
    "COMPONENTS": {
        "HOSTS": [...],
        "SWITCHES": [...],
        "CONTROLLERS": [...],
        
        "NAT_DEVICES": [
            {
                "ID": "nat1",
                "INTERNAL_IP": "10.0.0.254/24",
                "EXTERNAL_IP": "192.168.1.1/24",
                ...
            }
        ],
        
        "FIREWALLS": [
            {
                "ID": "fw1",
                "RULES": [...]
            }
        ]
    }
}
```

## Plugin Examples

### QoS Plugin
- **Purpose**: Add Quality of Service configuration
- **Features**: 
  - Configure queue sizes
  - Enable ECN (Explicit Congestion Notification)
  - Apply traffic shaping rules
  - Set bandwidth limits per connection

### Network Monitoring Plugin
- **Purpose**: Add monitoring and statistics collection
- **Features**:
  - Periodic statistics collection
  - Save stats to JSON file
  - Configurable monitoring interval and duration
  - Background monitoring thread

### NAT Component Plugin
- **Purpose**: Add NAT device support
- **Features**:
  - Create NAT hosts
  - Configure iptables rules
  - Support for DHCP
  - Multiple NAT devices per topology

## Plugin Development Best Practices

1. **Namespace Isolation**: Use unique plugin names to avoid conflicts
2. **Parameter Validation**: Validate parameters in your plugin code
3. **Error Handling**: Handle missing or invalid parameters gracefully
4. **Documentation**: Include docstrings and comments in your plugin
5. **Version Management**: Use semantic versioning for your plugins
6. **Dependencies**: Clearly document any external dependencies

## Advanced Features

### Plugin Communication
Plugins can access the topology object and read data from other components:

```python
def generate_post_start_code(self, topology: Topology, params: Dict[str, Any]) -> List[str]:
    code = []
    # Access topology components
    for host in topology.hosts:
        code.append(f"# Configure host {host['id']}")
    
    # Access custom components
    if "NAT_DEVICES" in topology.custom_components:
        for nat in topology.custom_components["NAT_DEVICES"]:
            code.append(f"# Configure NAT {nat['id']}")
    
    return code
```

### Dynamic Plugin Loading
The plugin manager automatically discovers and loads all valid plugins from the `plugins/` directory on startup.

### Plugin Execution Order
1. Component plugins parse custom components during topology loading
2. Topology plugins execute after topology is loaded
3. Script generator plugins execute during script generation in this order:
   - `generate_imports()`
   - `generate_pre_network_code()`
   - `generate_post_network_code()`
   - `generate_post_start_code()`

## Troubleshooting

### Plugin Not Loading
- Check that the plugin file is in the `plugins/` directory
- Ensure the plugin class inherits from the correct base class
- Verify there are no syntax errors in the plugin file
- Check the console output for error messages

### Plugin Not Executing
- Verify the plugin name in JSON matches `get_name()` return value
- Check that the plugin is listed in the `PLUGINS` section of your JSON
- Ensure parameters are correctly formatted in JSON

### Generated Code Issues
- Review the generated Python script for syntax errors
- Check that all required imports are included
- Verify that plugin-generated code is compatible with your Mininet version

## Example Workflow

1. **Create a new plugin** in `plugins/my_feature.py`
2. **Add plugin configuration** to your topology JSON
3. **Run the generator**: `python main.py`
4. **Review generated script** for your custom functionality
5. **Execute the Mininet script**: `sudo python your_topology_net.py`

## Contributing New Plugins

When creating plugins for sharing:
1. Follow the naming convention: `feature_plugin.py`
2. Include comprehensive docstrings
3. Create example JSON configurations
4. Test with multiple Mininet versions
5. Document any special requirements or dependencies