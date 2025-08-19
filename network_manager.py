# network_manager.py

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, Controller
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class NetworkManager:
    """
    Gerencia a criação e a manipulação da rede Mininet.
    """
    def __init__(self):
        self.net = None
        self._build_topology()

    def _build_topology(self):
        """
        Constrói uma topologia de rede simples para nosso protótipo.
        Topologia: 4 hosts, 2 switches, com links entre eles.
           h1 -- s1 -- s2 -- h3
                 |    |
           h2 -- s1   s2 -- h4
        """
        info('*** Criando a rede Mininet\n')
        # Usamos TCLink para poder alterar os parâmetros dos links dinamicamente
        self.net = Mininet(switch=OVSKernelSwitch, link=TCLink, autoSetMacs=True, autoStaticArp=True)

        info('*** Adicionando hosts\n')
        h1 = self.net.addHost('h1', ip='10.0.0.1/24')
        h2 = self.net.addHost('h2', ip='10.0.0.2/24')
        h3 = self.net.addHost('h3', ip='10.0.0.3/24')
        h4 = self.net.addHost('h4', ip='10.0.0.4/24')

        info('*** Adicionando switches\n')
        s1 = self.net.addSwitch('s1')
        s2 = self.net.addSwitch('s2')

        info('*** Criando links\n')
        # Links dos hosts para os switches
        self.net.addLink(h1, s1)
        self.net.addLink(h2, s1)
        self.net.addLink(h3, s2)
        self.net.addLink(h4, s2)
        # Link entre os switches
        self.net.addLink(s1, s2)

    def start_network(self):
        """Inicia a rede."""
        if self.net:
            info('*** Iniciando a rede\n')
            self.net.start()
            self._configure_switches_standalone()

    def stop_network(self):
        """Para a rede."""
        if self.net:
            info('*** Parando a rede\n')
            self.net.stop()

    def _configure_switches_standalone(self):
        """Configura todos os switches para operar em modo standalone (learning switch)."""
        info('*** Configurando switches em modo standalone\n')
        for switch in self.net.switches:
            # Este comando instrui o switch a agir como um learning switch L2
            # sem a necessidade de um controlador.
            switch.cmd(f'ovs-vsctl set-fail-mode {switch.name} standalone')

    def get_node_by_name(self, name):
        """Retorna um objeto de nó (host, switch) pelo nome."""
        try:
            return self.net.get(name)
        except KeyError:
            info(f'*** Erro: Nó {name} não encontrado na topologia.\n')
            return None

    def apply_delay(self, node1_name, node2_name, delay):
        """
        Aplica um delay a um link específico entre dois nós.
        Nota: A modificação é feita nas interfaces de ambos os nós.
        """
        node1 = self.get_node_by_name(node1_name)
        node2 = self.get_node_by_name(node2_name)

        if not node1 or not node2:
            return

        info(f'*** Aplicando delay de {delay} entre {node1_name} e {node2_name}\n')

        # Encontra as interfaces que conectam os dois nós
        for intf in node1.intfList():
            if intf.link and intf.link.intf2.node == node2:
                intf.config(delay=delay)
                # A configuração é aplicada em ambas as direções
                intf.link.intf2.config(delay=delay)
                info(f'    - Delay aplicado em {intf.name} ({node1_name}) e {intf.link.intf2.name} ({node2_name})\n')
                return

        info(f'*** Erro: Link direto entre {node1_name} e {node2_name} não encontrado.\n')


    def run_cli(self):
        """Inicia a Command Line Interface (CLI) da Mininet para depuração."""
        if self.net:
            info('*** Executando a CLI da Mininet. Digite "exit" para sair.\n')
            CLI(self.net)
