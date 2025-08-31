
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def mixedswitchestopo():

	net = Mininet(controller=Controller, waitConnected=True)

	info('*** Adding 1 controllers\n')
	{'ID': 'c0', 'TYPE': 'RemoteController', 'PARAMS': {'IP': '127.0.0.1'}} = net.addController('{'ID': 'c0', 'TYPE': 'RemoteController', 'PARAMS': {'IP': '127.0.0.1'}}')

	info('*** Adding 3 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')
	h3 = net.addHost('h3', ip='10.0.0.3/24')

	info('*** Adding 2 switches\n')
	{'id': 's1', 'type': 'OVSSwitch', 'controller': 'c0', 'params': {'protocols': 'OpenFlow13'}} = net.addSwitch('{'id': 's1', 'type': 'OVSSwitch', 'controller': 'c0', 'params': {'protocols': 'OpenFlow13'}}')
	{'id': 's2', 'type': 'LinuxBridge', 'controller': '', 'params': ''} = net.addSwitch('{'id': 's2', 'type': 'LinuxBridge', 'controller': '', 'params': ''}')

	info('*** Creating 4 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s2)
	net.addLink(s1, s2)

	info('*** Starting network\n')
	net.start()

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	mixedswitchestopo()
