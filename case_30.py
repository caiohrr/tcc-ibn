"""
Mininet script generated automatically.
Topology: Cascadingfailurescenario
Version: 1.0
Description: Topology simulating a cascading failure with 30 hosts and 3 switches in a chain. Middle switch (s2) and its connected hosts/links have 50% packet loss.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def cascadingfailurescenario_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 30 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')
	h3 = net.addHost('h3', ip='10.0.0.3/24')
	h4 = net.addHost('h4', ip='10.0.0.4/24')
	h5 = net.addHost('h5', ip='10.0.0.5/24')
	h6 = net.addHost('h6', ip='10.0.0.6/24')
	h7 = net.addHost('h7', ip='10.0.0.7/24')
	h8 = net.addHost('h8', ip='10.0.0.8/24')
	h9 = net.addHost('h9', ip='10.0.0.9/24')
	h10 = net.addHost('h10', ip='10.0.0.10/24')
	h11 = net.addHost('h11', ip='10.0.0.11/24')
	h12 = net.addHost('h12', ip='10.0.0.12/24')
	h13 = net.addHost('h13', ip='10.0.0.13/24')
	h14 = net.addHost('h14', ip='10.0.0.14/24')
	h15 = net.addHost('h15', ip='10.0.0.15/24')
	h16 = net.addHost('h16', ip='10.0.0.16/24')
	h17 = net.addHost('h17', ip='10.0.0.17/24')
	h18 = net.addHost('h18', ip='10.0.0.18/24')
	h19 = net.addHost('h19', ip='10.0.0.19/24')
	h20 = net.addHost('h20', ip='10.0.0.20/24')
	h21 = net.addHost('h21', ip='10.0.0.21/24')
	h22 = net.addHost('h22', ip='10.0.0.22/24')
	h23 = net.addHost('h23', ip='10.0.0.23/24')
	h24 = net.addHost('h24', ip='10.0.0.24/24')
	h25 = net.addHost('h25', ip='10.0.0.25/24')
	h26 = net.addHost('h26', ip='10.0.0.26/24')
	h27 = net.addHost('h27', ip='10.0.0.27/24')
	h28 = net.addHost('h28', ip='10.0.0.28/24')
	h29 = net.addHost('h29', ip='10.0.0.29/24')
	h30 = net.addHost('h30', ip='10.0.0.30/24')

	info('*** Adding 3 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')

	info('*** Creating 32 links\n')
	net.addLink(s1, s2, loss=50)
	net.addLink(s2, s3, loss=50)
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s1)
	net.addLink(h4, s1)
	net.addLink(h5, s1)
	net.addLink(h6, s1)
	net.addLink(h7, s1)
	net.addLink(h8, s1)
	net.addLink(h9, s1)
	net.addLink(h10, s1)
	net.addLink(h11, s2, loss=50)
	net.addLink(h12, s2, loss=50)
	net.addLink(h13, s2, loss=50)
	net.addLink(h14, s2, loss=50)
	net.addLink(h15, s2, loss=50)
	net.addLink(h16, s2, loss=50)
	net.addLink(h17, s2, loss=50)
	net.addLink(h18, s2, loss=50)
	net.addLink(h19, s2, loss=50)
	net.addLink(h20, s2, loss=50)
	net.addLink(h21, s3)
	net.addLink(h22, s3)
	net.addLink(h23, s3)
	net.addLink(h24, s3)
	net.addLink(h25, s3)
	net.addLink(h26, s3)
	net.addLink(h27, s3)
	net.addLink(h28, s3)
	net.addLink(h29, s3)
	net.addLink(h30, s3)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')
	net.get('s3').cmd('ovs-ofctl add-flow s3 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'cascadingfailurescenario',
		'version': '1.0',
		'description': 'Topology simulating a cascading failure with 30 hosts and 3 switches in a chain. Middle switch (s2) and its connected hosts/links have 50% packet loss.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': None},
			{'id': 'h6', 'ip': '10.0.0.6/24', 'mac': None},
			{'id': 'h7', 'ip': '10.0.0.7/24', 'mac': None},
			{'id': 'h8', 'ip': '10.0.0.8/24', 'mac': None},
			{'id': 'h9', 'ip': '10.0.0.9/24', 'mac': None},
			{'id': 'h10', 'ip': '10.0.0.10/24', 'mac': None},
			{'id': 'h11', 'ip': '10.0.0.11/24', 'mac': None},
			{'id': 'h12', 'ip': '10.0.0.12/24', 'mac': None},
			{'id': 'h13', 'ip': '10.0.0.13/24', 'mac': None},
			{'id': 'h14', 'ip': '10.0.0.14/24', 'mac': None},
			{'id': 'h15', 'ip': '10.0.0.15/24', 'mac': None},
			{'id': 'h16', 'ip': '10.0.0.16/24', 'mac': None},
			{'id': 'h17', 'ip': '10.0.0.17/24', 'mac': None},
			{'id': 'h18', 'ip': '10.0.0.18/24', 'mac': None},
			{'id': 'h19', 'ip': '10.0.0.19/24', 'mac': None},
			{'id': 'h20', 'ip': '10.0.0.20/24', 'mac': None},
			{'id': 'h21', 'ip': '10.0.0.21/24', 'mac': None},
			{'id': 'h22', 'ip': '10.0.0.22/24', 'mac': None},
			{'id': 'h23', 'ip': '10.0.0.23/24', 'mac': None},
			{'id': 'h24', 'ip': '10.0.0.24/24', 'mac': None},
			{'id': 'h25', 'ip': '10.0.0.25/24', 'mac': None},
			{'id': 'h26', 'ip': '10.0.0.26/24', 'mac': None},
			{'id': 'h27', 'ip': '10.0.0.27/24', 'mac': None},
			{'id': 'h28', 'ip': '10.0.0.28/24', 'mac': None},
			{'id': 'h29', 'ip': '10.0.0.29/24', 'mac': None},
			{'id': 'h30', 'ip': '10.0.0.30/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
			{'ID': 's2', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
			{'ID': 's3', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['s1', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['s2', 's3'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h1', 's1']},
			{'ENDPOINTS': ['h2', 's1']},
			{'ENDPOINTS': ['h3', 's1']},
			{'ENDPOINTS': ['h4', 's1']},
			{'ENDPOINTS': ['h5', 's1']},
			{'ENDPOINTS': ['h6', 's1']},
			{'ENDPOINTS': ['h7', 's1']},
			{'ENDPOINTS': ['h8', 's1']},
			{'ENDPOINTS': ['h9', 's1']},
			{'ENDPOINTS': ['h10', 's1']},
			{'ENDPOINTS': ['h11', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h12', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h13', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h14', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h15', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h16', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h17', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h18', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h19', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h20', 's2'], 'PARAMS': {'LOSS': 50}},
			{'ENDPOINTS': ['h21', 's3']},
			{'ENDPOINTS': ['h22', 's3']},
			{'ENDPOINTS': ['h23', 's3']},
			{'ENDPOINTS': ['h24', 's3']},
			{'ENDPOINTS': ['h25', 's3']},
			{'ENDPOINTS': ['h26', 's3']},
			{'ENDPOINTS': ['h27', 's3']},
			{'ENDPOINTS': ['h28', 's3']},
			{'ENDPOINTS': ['h29', 's3']},
			{'ENDPOINTS': ['h30', 's3']},
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
	cascadingfailurescenario_topology()
