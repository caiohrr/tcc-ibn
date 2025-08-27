from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from Validator import Validator
import threading
import time
import re


class ResourceMonitor(threading.Thread):
    """
    Uma thread para monitorar continuamente o uso de CPU e memória dos hosts na rede.
    """
    def __init__(self, network, interval=2):
        super(ResourceMonitor, self).__init__()
        self.network = network
        self.interval = interval
        self.stopped = threading.Event()

    def run(self):
        """O corpo principal da thread de monitoramento."""
        print("--- Iniciando Monitor de Recursos ---")
        while not self.stopped.is_set():
            for host in self.network.hosts:
                try:
                    # Coleta de uso de CPU e Memória
                    # Usamos 'top' em modo batch para uma leitura instantânea
                    output = host.cmd('top -b -n 1')
                    
                    # Extrai a carga média (load average) como um indicador de uso de CPU
                    load_avg_match = re.search(r'load average: ([\d.]+)', output)
                    load_avg = float(load_avg_match.group(1)) if load_avg_match else 'N/A'
                    
                    # Extrai o uso de memória
                    mem_match = re.search(r'KiB Mem[\s:]+([\d]+) total,[\s]+([\d]+) free,[\s]+([\d]+) used', output)
                    if mem_match:
                        mem_total = int(mem_match.group(1))
                        mem_used = int(mem_match.group(3))
                        mem_percent = (mem_used / mem_total) * 100 if mem_total > 0 else 0
                        mem_usage_str = f"{mem_percent:.2f}% ({mem_used}k / {mem_total}k)"
                    else:
                        mem_usage_str = "N/A"

                    print(f"Host: {host.name} | CPU Load Avg (1m): {load_avg} | Memória: {mem_usage_str}")

                except Exception as e:
                    print(f"Erro ao monitorar {host.name}: {e}")
            
            # Espera o intervalo definido antes da próxima coleta
            time.sleep(self.interval)
        print("--- Monitor de Recursos Finalizado ---")

    def stop(self):
        """Sinaliza para a thread parar."""
        self.stopped.set()

class Executer:

    NETWORK = None
    TOPOLOGY = None
    MONITOR_THREAD = None

    def __init__(self, TOPOLOGY):
        if isinstance(TOPOLOGY, Validator):
            self.TOPOLOGY = TOPOLOGY
        else:
            return
        self.NETWORK = Mininet()

        if self.TOPOLOGY.MNHOSTS is not []:
            for HOST in self.TOPOLOGY.MNHOSTS:
                # Adicionamos o host com o parâmetro inNamespace=True para isolar o monitoramento
                HOST.ELEM = self.NETWORK.addHost(HOST.ID)

        if self.TOPOLOGY.MNSWITCHES is not []:
            for SWITCH in self.TOPOLOGY.MNSWITCHES:
                SWITCH.ELEM = self.NETWORK.addSwitch(SWITCH.ID)

        if self.TOPOLOGY.MNOVSES is not []:
            for OVSES in self.TOPOLOGY.MNOVSES:
                OVSES.ELEM = self.NETWORK.addSwitch(OVSES.ID, failMode='standalone')

        if self.TOPOLOGY.CONNECTIONS is not []:
            for CONNECTION in self.TOPOLOGY.CONNECTIONS:
                # Corrigido para obter os elementos de nó corretos para criar o link
                node1 = self.NETWORK.get(CONNECTION["IN/OUT"])
                node2 = self.NETWORK.get(CONNECTION["OUT/IN"])
                self.NETWORK.addLink(node1, node2)

#------------------------------------------------------------------

    def executeTopology(self):
        self.NETWORK.build()
        self.NETWORK.start()

        # Inicia a thread de monitoramento
        self.MONITOR_THREAD = ResourceMonitor(self.NETWORK)
        self.MONITOR_THREAD.start()

        # Abre a CLI para interação do usuário
        CLI(self.NETWORK)

        # Para a thread de monitoramento antes de parar a rede
        self.MONITOR_THREAD.stop()
        self.MONITOR_THREAD.join() # Espera a thread finalizar

        self.NETWORK.stop()
