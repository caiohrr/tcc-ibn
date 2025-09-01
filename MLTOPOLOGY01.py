from mininet.net import Mininet
from mininet.cli import CLI

def TOPOLOGY01():

  NETWORK = Mininet()

  HOST01 = NETWORK.addHost('HOST01')
  HOST02 = NETWORK.addHost('HOST02')


  CONTROLLER01 = NETWORK.addController('CONTROLLER01')

  OVSS01 = NETWORK.addSwitch('OVSS01')

  NETWORK.addLink(HOST01, OVSS01)
  NETWORK.addLink(HOST02, OVSS01)

  NETWORK.start()
  CLI(NETWORK)
  NETWORK.stop()

TOPOLOGY01()