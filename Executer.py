from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from Validator import Validator

class Executer:

    NETWORK = None
    TOPOLOGY = None

    def __init__(self, TOPOLOGY):

        if isinstance(TOPOLOGY, Validator):
            self.TOPOLOGY = TOPOLOGY
        else:
            return
        self.NETWORK = Mininet()

        if self.TOPOLOGY.MNHOSTS is not []:
            for HOST in self.TOPOLOGY.MNHOSTS:
                HOST.ELEM = self.NETWORK.addHost(HOST.ID)

        if self.TOPOLOGY.MNSWITCHES is not []:
            for SWITCH in self.TOPOLOGY.MNSWITCHES:
                SWITCH.ELEM = self.NETWORK.addSwitch(SWITCH.ID)

        #if self.TOPOLOGY.MNCONTROLLER is not []:
        #    for CONTROLLER in self.TOPOLOGY.MNCONTROLLER:
        #        CONTROLLER.ELEM = self.NETWORK.addController(CONTROLLER.ID)

        if self.TOPOLOGY.MNOVSES is not []:
            for OVSES in self.TOPOLOGY.MNOVSES:
                OVSES.ELEM = self.NETWORK.addSwitch(OVSES.ID, failMode='standalone')

        if self.TOPOLOGY.CONNECTIONS is not []:
            for CONNECTION in self.TOPOLOGY.CONNECTIONS:
                self.NETWORK.addLink(CONNECTION["IN/OUT"], CONNECTION["OUT/IN"])

#------------------------------------------------------------------

    def executeTopology(self):

        self.NETWORK.start()
        CLI(self.NETWORK)
        self.NETWORK.stop()
