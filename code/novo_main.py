import json
from pathlib import Path
from typing import List, Dict, Optional

class Topology:
    def __init__(self, json_data: Dict):
        self._json_data = json_data
        self.id = self._parse_id()
        self.hosts = self._parse_hosts()
        self.switches = self._parse_switches()
        self.controllers = self._parse_controllers()
        self.ovsswitches = self._parse_ovsswitches()
        self.connections = self._parse_connections()

    def _parse_id(self) -> str:
        return self._json_data.get("ID", "unknown_topology").lower()

    def _parse_hosts(self) -> List[Dict[str, str]]:
        components = self._json_data.get("COMPONENTS", {})
        hosts = components.get("HOSTS", [])
        return [{"id": host["ID"], "ip": host["IP"]} for host in hosts]

    def _parse_switches(self) -> List[str]:
        components = self._json_data.get("COMPONENTS", {})
        switches = components.get("SWITCHES", [])
        return [switch.lower() for switch in switches]

    def _parse_controllers(self) -> List[str]:
        components = self._json_data.get("COMPONENTS", {})
        controllers = components.get("CONTROLLERS", [])
        return [controller.lower() for controller in controllers]

    def _parse_ovsswitches(self) -> List[Dict[str, str]]:
        components = self._json_data.get("COMPONENTS", {})
        ovsswitches = components.get("OVSSWITCHES", [])
        return [{"id": ovs["ID"], "controller": ovs["CONTROLLER"]} for ovs in ovsswitches]

    def _parse_connections(self) -> List[Dict[str, str]]:
        return self._json_data.get("CONNECTIONS", [])

    def print_details(self):
        print("Hosts:")
        for host in self.hosts:
            print(f"ID: {host['id']}")
            print(f"IP: {host['ip']}")
        
        print("\nSwitches:")
        for switch in self.switches:
            print(f"SWITCH: {switch}")
        
        print("\nControllers:")
        for controller in self.controllers:
            print(f"CONTROLLER: {controller}")
        
        print("\nOVS Switches:")
        for ovs in self.ovsswitches:
            print(f"ID: {ovs['id']}")
            print(f"CONTROLLER: {ovs['controller']}")
        
        print("\nConnections:")
        for conn in self.connections:
            print(f"IN/OUT: {conn['IN/OUT']}")
            print(f"OUT/IN: {conn['OUT/IN']}")
        
        print("\nLists:")
        print(self.hosts)
        print(self.switches)
        print(self.controllers)
        print(self.ovsswitches)
        print(self.connections)


def find_matching_file(dir_path: Path, prefix: str) -> Optional[Path]:
    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    matching_file = next((f for f in files if f.name.startswith(prefix)), None)
    if matching_file is None:
        raise FileNotFoundError(f"No file found starting with '{prefix}' in {dir_path}")
    return matching_file


def load_json_file(file_path: Path) -> Dict:
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def generate_mininet_script(topology: Topology, output_file: str = "topology.py"):
    with open(output_file, "w+") as mn_file:
        mn_file.write(
            """
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
"""
        )

        mn_file.write(f"def {topology.id}():\n\n")
        mn_file.write("\tnet = Mininet(controller=Controller, waitConnected=True)\n\n")
        
        mn_file.write(f"\tinfo('*** Adding {len(topology.controllers)} controllers\\n')\n")
        for controller in topology.controllers:
            mn_file.write(f"\t{controller} = net.addController('{controller}')\n")
        mn_file.write("\n")

        mn_file.write(f"\tinfo('*** Adding {len(topology.hosts)} hosts\\n')\n")
        for host in topology.hosts:
            id_ = host["id"]
            ip = host["ip"]
            mn_file.write(f"\t{id_} = net.addHost('{id_}', ip='{ip}')\n")
        mn_file.write("\n")

        mn_file.write(f"\tinfo('*** Adding {len(topology.switches)} switches\\n')\n")
        for switch in topology.switches:
            mn_file.write(f"\t{switch} = net.addSwitch('{switch}')\n")
        mn_file.write("\n")

        mn_file.write(f"\tinfo('*** Creating {len(topology.connections)} links\\n')\n")
        for connection in topology.connections:
            in_out = connection["IN/OUT"]
            out_in = connection["OUT/IN"]
            mn_file.write(f"\tnet.addLink({in_out}, {out_in})\n")
        mn_file.write("\n")

        mn_file.write(f"\tinfo('*** Starting network\\n')\n")
        mn_file.write(f"\tnet.start()\n\n")

        mn_file.write(f"\tinfo('*** Running CLI\\n')\n")
        mn_file.write(f"\tCLI(net)\n\n")

        mn_file.write(f"\tinfo('*** Stopping network\\n')\n")
        mn_file.write(f"\tnet.stop()\n\n")

        mn_file.write("if __name__ == '__main__':\n")
        mn_file.write("\tsetLogLevel('info')\n")
        mn_file.write(f"\t{topology.id}()\n")


def main():
    dir_path = Path() / ".." / "topologies"
    prefix = input("digite o nome da topologia: ")
    
    matching_file = find_matching_file(dir_path, prefix)
    json_data = load_json_file(matching_file)
    
    topology = Topology(json_data)
    topology.print_details()
    generate_mininet_script(topology)


if __name__ == "__main__":
    main()
