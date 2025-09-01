from mininet.node import *

def TOPOLOGY01():

  HOST01 = Host('HOST01')
  HOST01.setIP('192.168.122.01/24')
  HOST02 = Host('HOST02')
  HOST02.setIP('192.168.122.02/24')


  CONTROLLER01 = Controller('CONTROLLER01', inNamespace=False)
  CONTROLLER01.start()

  OVSS01 = OVSSwitch('OVSS01', inNamespace=False)
  OVSS01.start([CONTROLLER01])

  Link(HOST01, OVSS01)
  Link(HOST02, OVSS01)

  #### SCRIPT AREA ####

  #####################

  OVSS01.stop()

  CONTROLLER01.stop()

TOPOLOGY01()