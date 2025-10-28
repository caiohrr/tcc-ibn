"""
Mininet script generated automatically.
Topology: Multiswitchtopo_7h3s
Version: 1.0
Description: A topology with 3 switches and 7 hosts. s1 is connected to h1, h2. s2 is connected to h3, h4. s3 is connected to h5, h6, h7. IPs increment by 10.
Intent Monitoring: Disabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def multiswitchtopo_7h3s_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, waitConnected=True)

	info('*** Adding 1 controllers\n')
	c0 = net.addController('c0')

	info('*** Adding 7 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.10/24')
	h2 = net.addHost('h2', ip='10.0.0.20/24')
	h3 = net.addHost('h3', ip='10.0.0.30/24')
	h4 = net.addHost('h4', ip='10.0.0.40/24')
	h5 = net.addHost('h5', ip='10.0.0.50/24')
	h6 = net.addHost('h6', ip='10.0.0.60/24')
	h7 = net.addHost('h7', ip='10.0.0.70/24')

	info('*** Adding 3 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')

	info('*** Creating 9 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s2)
	net.addLink(h4, s2)
	net.addLink(h5, s3)
	net.addLink(h6, s3)
	net.addLink(h7, s3)
	net.addLink(s1, s2)
	net.addLink(s2, s3)

	info('*** Starting network\n')
	net.start()

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	multiswitchtopo_7h3s_topology()
