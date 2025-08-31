
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def topology01():

	net = Mininet(controller=Controller, waitConnected=True)

	info('*** Adding 1 controllers\n')
	controller01 = net.addController('controller01')

	info('*** Adding 3 hosts\n')
	HOST01 = net.addHost('HOST01', ip='192.168.122.01/24')
	HOST02 = net.addHost('HOST02', ip='192.168.122.02/24')
	HOST03 = net.addHost('HOST03', ip='192.168.122.03/24')

	info('*** Adding 0 switches\n')

	info('*** Adding 0 ovsswitches\n')
	OVSS01 = net.addSwitch('OVSS01')
	OVSS02 = net.addSwitch('OVSS02')

	info('*** Creating 3 links\n')
	net.addLink(HOST01, OVSS01)
	net.addLink(HOST02, OVSS01)
	net.addLink(HOST03, OVSS02)

	info('*** Starting network\n')
	net.start()

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	topology01()
