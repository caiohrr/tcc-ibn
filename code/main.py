import json
from pathlib import Path
from typing import List, Dict, Optional

class Topology:
    def __init__(self, json_data: Dict):
        self._json_data = json_data
        components = self._json_data.get("COMPONENTS", {})
        self.id = self._parse_id()
        self.hosts = self._parse_hosts(components)
        self.switches = self._parse_switches(components)
        self.controllers = self._parse_controllers(components)
        self.connections = self._parse_connections()

    def _parse_id(self) -> str:
        return self._json_data.get("ID", "unknown_topology").lower()

    def _parse_hosts(self, components: Dict) -> List[Dict[str, str]]:
        hosts = components.get("HOSTS", [])
        return [{"id": host["ID"], "ip": host["IP"]} for host in hosts]

    def _parse_switches(self, components: Dict) -> List[str]:
        switches = components.get("SWITCHES", [])
        return [{
            "id": switch_info.get("ID").lower(),
            "type": switch_info.get("TYPE"),
            "controller": switch_info.get("CONTROLLER", "").lower(),
            "params": switch_info.get("PARAMS", "")
        } for switch_info in switches]

    def _parse_controllers(self, components: Dict) -> List[str]:
        controllers = components.get("CONTROLLERS", [])
        return [controller for controller in controllers]

    def _parse_connections(self) -> List[Dict[str, str]]:
        return self._json_data.get("CONNECTIONS", [])

    def print_details(self):
        for attr, value in self.__dict__.items():
            if not callable(value) and not attr.startswith("_"):
                print(f"{attr.capitalize()}:")
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            for k, v in item.items():
                                print(f"    {k.upper()}: {v}")
                        else:
                            print(f"    {item}")
                        print()
                else:
                    print(f"    {value}")


def find_matching_file(dir_path: Path, prefix: str) -> Optional[Path]:
    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    matching_file = next((f for f in files if f.name.startswith(prefix)), None)
    if matching_file is None:
        raise FileNotFoundError(f"No file found starting with '{prefix}' in {dir_path}")
    return matching_file


def load_json_file(file_path: Path) -> Dict:
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def generate_mininet_script(
    topology: Topology,
    output_file: str = "topology.py"
):
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
            id = host["id"]
            ip = host["ip"]
            mn_file.write(f"\t{id} = net.addHost('{id}', ip='{ip}')\n")
        mn_file.write("\n")

        mn_file.write(f"\tinfo('*** Adding {len(topology.switches)} switches\\n')\n")
        for switch in topology.switches:
            mn_file.write(f"\t{switch} = net.addSwitch('{switch}')\n")
        mn_file.write("\n")

        mn_file.write(f"\tinfo('*** Creating {len(topology.connections)} links\\n')\n")
        for connection in topology.connections:
            endpoints = connection.get("ENDPOINTS")
            mn_file.write(f"\tnet.addLink({endpoints[0]}, {endpoints[1]})\n")
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
    prefix = input("Digite o nome da topologia: ")
    
    matching_file = find_matching_file(dir_path, prefix)
    json_data = load_json_file(matching_file)
    
    topology = Topology(json_data)
    topology.print_details()
    generate_mininet_script(topology)


if __name__ == "__main__":
    main()
