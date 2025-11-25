"""
Mininet script generated automatically.
Topology: Ten_hosts_to_s1
Version: 1.0
Description: 10 hosts connected to a single switch s1 with sequential IPs and 0.5% link loss.
Intent Monitoring: Disabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def ten_hosts_to_s1_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 10 hosts\n')
	h1 = net.addHost('h1', ip='192.168.0.10/24')
	h2 = net.addHost('h2', ip='192.168.0.11/24')
	h3 = net.addHost('h3', ip='192.168.0.12/24')
	h4 = net.addHost('h4', ip='192.168.0.13/24')
	h5 = net.addHost('h5', ip='192.168.0.14/24')
	h6 = net.addHost('h6', ip='192.168.0.15/24')
	h7 = net.addHost('h7', ip='192.168.0.16/24')
	h8 = net.addHost('h8', ip='192.168.0.17/24')
	h9 = net.addHost('h9', ip='192.168.0.18/24')
	h10 = net.addHost('h10', ip='192.168.0.19/24')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 10 links\n')
	net.addLink(h1, s1, loss=0.5)
	net.addLink(h2, s1, loss=0.5)
	net.addLink(h3, s1, loss=0.5)
	net.addLink(h4, s1, loss=0.5)
	net.addLink(h5, s1, loss=0.5)
	net.addLink(h6, s1, loss=0.5)
	net.addLink(h7, s1, loss=0.5)
	net.addLink(h8, s1, loss=0.5)
	net.addLink(h9, s1, loss=0.5)
	net.addLink(h10, s1, loss=0.5)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	ten_hosts_to_s1_topology()
