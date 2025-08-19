from Validator import Validator

class Translator:

    STATUS = None
    TOPOLOGY = None

    def __init__(self, TOPOLOGY):

        if isinstance(TOPOLOGY, Validator):
            self.TOPOLOGY = TOPOLOGY
        else:
            self.STATUS = -1
            return

        self.STATUS = 0

#------------------------------------------------------------------

    def lowLevelTranslation(self):

        llFile = open("LL" + self.TOPOLOGY.ID + ".py", 'w+')

        llFile.write("from mininet.node import *\n\n")
        llFile.write("def " + self.TOPOLOGY.ID + "():\n\n")

        if self.TOPOLOGY.MNHOSTS is not []:
            for HOST in self.TOPOLOGY.MNHOSTS:
                llFile.write("  " + HOST.ID + " = " + "Host('" + HOST.ID + "')\n")
                llFile.write("  " + HOST.ID + ".setIP('" + HOST.IP + "')\n")
            llFile.write("\n")

        if self.TOPOLOGY.MNSWITCHES is not []:
            for SWITCH in self.TOPOLOGY.MNSWITCHES:
                llFile.write("  " + SWITCH.ID + " = " + "Switch('" + SWITCH.ID + "')\n")
            llFile.write("\n")

        if self.TOPOLOGY.MNCONTROLLER is not []:
            for CONTROLLER in self.TOPOLOGY.MNCONTROLLER:
                llFile.write("  " + CONTROLLER.ID + " = " + "Controller('" + CONTROLLER.ID + "', inNamespace=False)\n")
                llFile.write("  " + CONTROLLER.ID + ".start()\n")
            llFile.write("\n")

        if self.TOPOLOGY.MNOVSES is not []:
            for OVSES in self.TOPOLOGY.MNOVSES:
                llFile.write("  " + OVSES.ID + " = " + "OVSSwitch('" + OVSES.ID + "', inNamespace=False)\n")
                llFile.write("  " + OVSES.ID + ".start([" + OVSES.CONTROLLER + "])\n")
            llFile.write("\n")

        if self.TOPOLOGY.CONNECTIONS is not []:
            for CONNECTION in self.TOPOLOGY.CONNECTIONS:
                llFile.write("  Link(" + CONNECTION["IN/OUT"] + ", " + CONNECTION["OUT/IN"] + ")\n")
            llFile.write("\n")

        llFile.write("  #### SCRIPT AREA ####\n\n")
        llFile.write("  #####################\n\n")

        if self.TOPOLOGY.MNOVSES is not []:
            for OVSES in self.TOPOLOGY.MNOVSES:
                llFile.write("  " + OVSES.ID + ".stop()\n")
            llFile.write("\n")

        if self.TOPOLOGY.MNCONTROLLER is not []:
            for CONTROLLER in self.TOPOLOGY.MNCONTROLLER:
                llFile.write("  " + CONTROLLER.ID + ".stop()\n")
            llFile.write("\n")

        llFile.write(self.TOPOLOGY.ID + "()")

#------------------------------------------------------------------

    def midLevelTranslation(self):

        llFile = open("ML" + self.TOPOLOGY.ID + ".py", 'w+')

        llFile.write("from mininet.net import Mininet\n")
        llFile.write("from mininet.cli import CLI\n\n")

        llFile.write("def " + self.TOPOLOGY.ID + "():\n\n")

        llFile.write("  NETWORK = Mininet()\n\n")

        if self.TOPOLOGY.MNHOSTS is not []:
            for HOST in self.TOPOLOGY.MNHOSTS:
                llFile.write("  " + HOST.ID + " = " + "NETWORK.addHost('" + HOST.ID + "')\n")
            llFile.write("\n")

        if self.TOPOLOGY.MNSWITCHES is not []:
            for SWITCH in self.TOPOLOGY.MNSWITCHES:
                llFile.write("  " + SWITCH.ID + " = " + "NETWORK.addSwitch('" + SWITCH.ID + "')\n")
            llFile.write("\n")

        if self.TOPOLOGY.MNCONTROLLER is not []:
            for CONTROLLER in self.TOPOLOGY.MNCONTROLLER:
                llFile.write("  " + CONTROLLER.ID + " = " + "NETWORK.addController('" + CONTROLLER.ID + "')\n")
            llFile.write("\n")

        if self.TOPOLOGY.MNOVSES is not []:
            for OVSES in self.TOPOLOGY.MNOVSES:
                llFile.write("  " + OVSES.ID + " = " + "NETWORK.addSwitch('" + OVSES.ID + "')\n")
            llFile.write("\n")

        if self.TOPOLOGY.CONNECTIONS is not []:
            for CONNECTION in self.TOPOLOGY.CONNECTIONS:
                llFile.write("  NETWORK.addLink(" + CONNECTION["IN/OUT"] + ", " + CONNECTION["OUT/IN"] + ")\n")
            llFile.write("\n")

        llFile.write("  NETWORK.start()\n")
        llFile.write("  CLI(NETWORK)\n")
        llFile.write("  NETWORK.stop()\n\n")

        llFile.write(self.TOPOLOGY.ID + "()")