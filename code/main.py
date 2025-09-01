import json
from pathlib import Path
from typing import List, Dict, Optional, Any

class Topology:
    """
    Representa a topologia da rede, lida a partir de um arquivo JSON.
    Esta versão é atualizada para lidar com um formato JSON mais robusto,
    com parâmetros opcionais para hosts, switches, controladores e links.
    """
    def __init__(self, json_data: Dict[str, Any]):
        self._json_data = json_data
        components = self._json_data.get("COMPONENTS", {})
        
        # Informações básicas da topologia
        self.id = self._json_data.get("ID", "unknown_topology").lower()
        self.version = self._json_data.get("VERSION", "N/A")
        self.description = self._json_data.get("DESCRIPTION", "No description provided.")

        # Componentes da rede
        self.hosts = self._parse_hosts(components)
        self.switches = self._parse_switches(components)
        self.controllers = self._parse_controllers(components)
        self.connections = self._parse_connections()

    def _parse_hosts(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai a lista de hosts. Cada host é um dicionário.
        O MAC é um parâmetro opcional.
        """
        parsed_hosts = []
        hosts_data = components.get("HOSTS", [])
        for host in hosts_data:
            host_info = {
                "id": host.get("ID"),
                "ip": host.get("IP"),
                "mac": host.get("MAC")  # Retorna None se a chave 'MAC' não existir
            }
            if host_info["id"] and host_info["ip"]:
                parsed_hosts.append(host_info)
        return parsed_hosts

    def _parse_switches(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai a lista de switches. A estrutura agora é uma lista de objetos.
        """
        return components.get("SWITCHES", [])

    def _parse_controllers(self, components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrai a lista de controladores. A estrutura agora é uma lista de objetos.
        """
        return components.get("CONTROLLERS", [])

    def _parse_connections(self) -> List[Dict[str, Any]]:
        """
        Extrai as conexões. A estrutura agora usa 'ENDPOINTS' e 'PARAMS'.
        """
        return self._json_data.get("CONNECTIONS", [])

    def print_details(self):
        """Imprime os detalhes da topologia de forma organizada."""
        print(f"--- Topology Details: {self.id.capitalize()} (v{self.version}) ---")
        print(f"Description: {self.description}\n")

        print("Hosts:")
        if not self.hosts: print("  None")
        for host in self.hosts:
            mac_info = f", MAC: {host['mac']}" if host['mac'] else ""
            print(f"  - ID: {host['id']}, IP: {host['ip']}{mac_info}")
        
        print("\nSwitches:")
        if not self.switches: print("  None")
        for switch in self.switches:
            params_info = f", PARAMS: {switch.get('PARAMS', {})}"
            print(f"  - ID: {switch.get('ID')}, TYPE: {switch.get('TYPE', 'Default')}{params_info}")
        
        print("\nControllers:")
        if not self.controllers: print("  None")
        for controller in self.controllers:
            params_info = f", PARAMS: {controller.get('PARAMS', {})}"
            print(f"  - ID: {controller.get('ID')}, TYPE: {controller.get('TYPE', 'Default')}{params_info}")
        
        print("\nConnections:")
        if not self.connections: print("  None")
        for conn in self.connections:
            endpoints = conn.get('ENDPOINTS', ['N/A', 'N/A'])
            params_info = f", PARAMS: {conn.get('PARAMS', {})}"
            print(f"  - ENDPOINTS: {endpoints[0]} <--> {endpoints[1]}{params_info}")
        
        print("\n" + "-" * 40)


def find_matching_file(dir_path: Path, prefix: str) -> Optional[Path]:
    """Encontra o primeiro arquivo no diretório que começa com o prefixo."""
    files = sorted([f for f in dir_path.iterdir() if f.is_file()])
    matching_file = next((f for f in files if f.name.lower().startswith(prefix.lower())), None)
    if matching_file is None:
        raise FileNotFoundError(f"No file found starting with '{prefix}' in {dir_path}")
    return matching_file


def load_json_file(file_path: Path) -> Dict:
    """Carrega dados de um arquivo JSON."""
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def generate_mininet_script(topology: Topology, output_file: str = "topology.py"):
    """Gera um script Python para Mininet baseado na topologia fornecida."""
    with open(output_file, "w+", encoding='utf-8') as mn_file:
        # --- Imports ---
        mn_file.write(
            '"""\n'
            'Script Mininet gerado automaticamente.\n'
            f'Topologia: {topology.id.capitalize()}\n'
            '"""\n'
            "from mininet.net import Mininet\n"
            "from mininet.node import Controller, RemoteController, OVSKernelSwitch\n"
            "from mininet.cli import CLI\n"
            "from mininet.log import setLogLevel, info\n"
            "from mininet.link import TCLink\n\n"
        )

        # --- Definição da Função da Topologia ---
        mn_file.write(f"def {topology.id}_topology():\n\n")
        mn_file.write("\t'Cria e configura a topologia de rede.'\n")
        mn_file.write("\tnet = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=True)\n\n")

        # --- Adicionar Controladores ---
        mn_file.write(f"\tinfo('*** Adding {len(topology.controllers)} controllers\\n')\n")
        for controller in topology.controllers:
            cid = controller.get('ID', 'c0')
            ctype = controller.get('TYPE', 'Controller')
            params = controller.get('PARAMS', {})
            
            if ctype == 'RemoteController':
                ip = params.get('IP', '127.0.0.1')
                port = params.get('PORT', 6653)
                mn_file.write(f"\t{cid} = net.addController('{cid}', controller=RemoteController, ip='{ip}', port={port})\n")
            else: # Controller padrão
                mn_file.write(f"\t{cid} = net.addController('{cid}')\n")
        mn_file.write("\n")

        # --- Adicionar Hosts ---
        mn_file.write(f"\tinfo('*** Adding {len(topology.hosts)} hosts\\n')\n")
        for host in topology.hosts:
            params_list = [f"'{host['id']}'", f"ip='{host['ip']}'"]
            if host.get('mac'):
                params_list.append(f"mac='{host['mac']}'")
            params_str = ", ".join(params_list)
            mn_file.write(f"\t{host['id']} = net.addHost({params_str})\n")
        mn_file.write("\n")

        # --- Adicionar Switches ---
        mn_file.write(f"\tinfo('*** Adding {len(topology.switches)} switches\\n')\n")
        for switch in topology.switches:
            sid = switch.get('ID', 's1')
            params = switch.get('PARAMS', {})
            params_str = ", ".join([f"{k.lower()}='{v}'" for k, v in params.items()])
            mn_file.write(f"\t{sid} = net.addSwitch('{sid}', {params_str})\n" if params_str else f"\t{sid} = net.addSwitch('{sid}')\n")
        mn_file.write("\n")

        # --- Criar Links ---
        mn_file.write(f"\tinfo('*** Creating {len(topology.connections)} links\\n')\n")
        # Mapeia nomes de parâmetros do JSON para os nomes esperados pelo Mininet/TCLink
        param_map = {'bandwidth': 'bw'}
        for conn in topology.connections:
            endpoints = conn.get('ENDPOINTS')
            params = conn.get('PARAMS', {})
            if endpoints and len(endpoints) == 2:
                param_list = []
                for k, v in params.items():
                    key_lower = k.lower()
                    mininet_key = param_map.get(key_lower, key_lower)
                    # Formata o valor: strings precisam de aspas, números não. repr() lida com isso.
                    value_repr = repr(v) if isinstance(v, str) else v
                    param_list.append(f"{mininet_key}={value_repr}")

                link_params_str = ", ".join(param_list)
                mn_file.write(f"\tnet.addLink({endpoints[0]}, {endpoints[1]}, {link_params_str})\n" if link_params_str else f"\tnet.addLink({endpoints[0]}, {endpoints[1]})\n")
        mn_file.write("\n")

        # --- Iniciar e Parar a Rede ---
        mn_file.write("\tinfo('*** Starting network\\n')\n")
        mn_file.write("\tnet.start()\n\n")

        mn_file.write("\tinfo('*** Running CLI\\n')\n")
        mn_file.write("\tCLI(net)\n\n")

        mn_file.write("\tinfo('*** Stopping network\\n')\n")
        mn_file.write("\tnet.stop()\n\n")

        # --- Bloco Principal ---
        mn_file.write("if __name__ == '__main__':\n")
        mn_file.write("\tsetLogLevel('info')\n")
        mn_file.write(f"\t{topology.id}_topology()\n")


def main():
    """Função principal para executar o script."""
    try:
        dir_path = Path() / "topologies"
        prefix = input("Digite o nome da topologia: ")
        
        matching_file = find_matching_file(dir_path, prefix)
        print(f"Arquivo encontrado: {matching_file}\n")
        
        json_data = load_json_file(matching_file)
        
        topology = Topology(json_data)
        topology.print_details()
        
        output_filename = f"{topology.id}_net.py"
        generate_mininet_script(topology, output_filename)
        print(f"Script Mininet gerado com sucesso: '{output_filename}'")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Erro ao processar o arquivo JSON: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()

