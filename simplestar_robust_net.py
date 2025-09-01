"""
Script Mininet gerado automaticamente.
Topologia: Simplestar_robust
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def simplestar_robust_topology():

	'Cria e configura a topologia de rede.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=True)

	info('*** Adding 1 controllers\n')
	c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
	h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
	h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1', protocols='OpenFlow13')

	info('*** Creating 4 links\n')
	net.addLink(h1, s1, bw=100, delay='5ms')
	net.addLink(h2, s1, bw=50, delay='10ms', loss=1)
	net.addLink(h3, s1, bw=100, delay='5ms')
	net.addLink(h4, s1, bw=80, delay='7ms')

	info('*** Starting network\n')
	net.start()

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	simplestar_robust_topology()
