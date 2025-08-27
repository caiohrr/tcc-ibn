
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
def simplestar():

	net = Mininet(controller=Controller, waitConnected=True)
	info('*** Adding 0 controllers\n')

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')
	h3 = net.addHost('h3', ip='10.0.0.3/24')
	h4 = net.addHost('h4', ip='10.0.0.4/24')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 4 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s1)
	net.addLink(h4, s1)

	info('*** Starting network\n')
	net.start()

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	simplestar()
