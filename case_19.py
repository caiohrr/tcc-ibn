"""
Mininet script generated automatically.
Topology: Redegargalo
Version: 1.0
Description: Rede com 18 hosts distribuídos em 2 switches, com um link gargalo de 10Mbps entre os switches e links de 100Mbps para os hosts. Monitoramento habilitado.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def redegargalo_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 18 hosts\n')
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

	info('*** Adding 2 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')

	info('*** Creating 19 links\n')
	net.addLink(s1, s2, bw=10)
	net.addLink(h1, s1, bw=100)
	net.addLink(h2, s1, bw=100)
	net.addLink(h3, s1, bw=100)
	net.addLink(h4, s1, bw=100)
	net.addLink(h5, s1, bw=100)
	net.addLink(h6, s1, bw=100)
	net.addLink(h7, s1, bw=100)
	net.addLink(h8, s1, bw=100)
	net.addLink(h9, s1, bw=100)
	net.addLink(h10, s2, bw=100)
	net.addLink(h11, s2, bw=100)
	net.addLink(h12, s2, bw=100)
	net.addLink(h13, s2, bw=100)
	net.addLink(h14, s2, bw=100)
	net.addLink(h15, s2, bw=100)
	net.addLink(h16, s2, bw=100)
	net.addLink(h17, s2, bw=100)
	net.addLink(h18, s2, bw=100)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'redegargalo',
		'version': '1.0',
		'description': 'Rede com 18 hosts distribuídos em 2 switches, com um link gargalo de 10Mbps entre os switches e links de 100Mbps para os hosts. Monitoramento habilitado.',
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
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch'},
			{'ID': 's2', 'TYPE': 'OVSSwitch'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['s1', 's2'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h3', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h4', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h5', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h6', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h7', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h8', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h9', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h10', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h11', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h12', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h13', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h14', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h15', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h16', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h17', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h18', 's2'], 'PARAMS': {'BANDWIDTH': 100}},
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
	redegargalo_topology()
