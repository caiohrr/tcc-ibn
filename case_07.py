"""
Mininet script generated automatically.
Topology: Eight_hosts_to_s1_loss_test
Version: 1.0
Description: Uma rede com 8 hosts conectados a um único switch (s1), com 1% de perda de pacotes em todos os links para teste de robustez.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def eight_hosts_to_s1_loss_test_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 8 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')
	h3 = net.addHost('h3', ip='10.0.0.3/24')
	h4 = net.addHost('h4', ip='10.0.0.4/24')
	h5 = net.addHost('h5', ip='10.0.0.5/24')
	h6 = net.addHost('h6', ip='10.0.0.6/24')
	h7 = net.addHost('h7', ip='10.0.0.7/24')
	h8 = net.addHost('h8', ip='10.0.0.8/24')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 8 links\n')
	net.addLink(h1, s1, loss=1)
	net.addLink(h2, s1, loss=1)
	net.addLink(h3, s1, loss=1)
	net.addLink(h4, s1, loss=1)
	net.addLink(h5, s1, loss=1)
	net.addLink(h6, s1, loss=1)
	net.addLink(h7, s1, loss=1)
	net.addLink(h8, s1, loss=1)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'eight_hosts_to_s1_loss_test',
		'version': '1.0',
		'description': 'Uma rede com 8 hosts conectados a um único switch (s1), com 1% de perda de pacotes em todos os links para teste de robustez.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': None},
			{'id': 'h6', 'ip': '10.0.0.6/24', 'mac': None},
			{'id': 'h7', 'ip': '10.0.0.7/24', 'mac': None},
			{'id': 'h8', 'ip': '10.0.0.8/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h3', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h4', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h5', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h6', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h7', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h8', 's1'], 'PARAMS': {'LOSS': 1}},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 5
	monitor.start_monitoring()

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping intent monitor\n')
	if 'monitor' in locals():
		monitor.stop_monitoring()
		monitor.export_report()

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	eight_hosts_to_s1_loss_test_topology()
