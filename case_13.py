"""
Mininet script generated automatically.
Topology: Datacentertopology
Version: 1.0
Description: Data Center topology with 2 core switches (s1, s2) and 16 hosts.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def datacentertopology_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 16 hosts\n')
	h1_1 = net.addHost('h1_1', ip='10.0.1.1/24', mem='2048M')
	h1_2 = net.addHost('h1_2', ip='10.0.1.2/24', mem='2048M')
	h1_3 = net.addHost('h1_3', ip='10.0.1.3/24', mem='2048M')
	h1_4 = net.addHost('h1_4', ip='10.0.1.4/24', mem='2048M')
	h1_5 = net.addHost('h1_5', ip='10.0.1.5/24', mem='2048M')
	h1_6 = net.addHost('h1_6', ip='10.0.1.6/24', mem='2048M')
	h1_7 = net.addHost('h1_7', ip='10.0.1.7/24', mem='2048M')
	h1_8 = net.addHost('h1_8', ip='10.0.1.8/24', mem='2048M')
	h2_1 = net.addHost('h2_1', ip='10.0.2.1/24', mem='512M')
	h2_2 = net.addHost('h2_2', ip='10.0.2.2/24', mem='512M')
	h2_3 = net.addHost('h2_3', ip='10.0.2.3/24', mem='512M')
	h2_4 = net.addHost('h2_4', ip='10.0.2.4/24', mem='512M')
	h2_5 = net.addHost('h2_5', ip='10.0.2.5/24', mem='512M')
	h2_6 = net.addHost('h2_6', ip='10.0.2.6/24', mem='512M')
	h2_7 = net.addHost('h2_7', ip='10.0.2.7/24', mem='512M')
	h2_8 = net.addHost('h2_8', ip='10.0.2.8/24', mem='512M')

	info('*** Adding 2 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')

	info('*** Creating 17 links\n')
	net.addLink(s1, s2)
	net.addLink(h1_1, s1)
	net.addLink(h1_2, s1)
	net.addLink(h1_3, s1)
	net.addLink(h1_4, s1)
	net.addLink(h1_5, s1)
	net.addLink(h1_6, s1)
	net.addLink(h1_7, s1)
	net.addLink(h1_8, s1)
	net.addLink(h2_1, s2)
	net.addLink(h2_2, s2)
	net.addLink(h2_3, s2)
	net.addLink(h2_4, s2)
	net.addLink(h2_5, s2)
	net.addLink(h2_6, s2)
	net.addLink(h2_7, s2)
	net.addLink(h2_8, s2)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'datacentertopology',
		'version': '1.0',
		'description': 'Data Center topology with 2 core switches (s1, s2) and 16 hosts.',
		'hosts': [
			{'id': 'h1_1', 'ip': '10.0.1.1/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h1_2', 'ip': '10.0.1.2/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h1_3', 'ip': '10.0.1.3/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h1_4', 'ip': '10.0.1.4/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h1_5', 'ip': '10.0.1.5/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h1_6', 'ip': '10.0.1.6/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h1_7', 'ip': '10.0.1.7/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h1_8', 'ip': '10.0.1.8/24', 'mac': None, 'max_ram': 2048},
			{'id': 'h2_1', 'ip': '10.0.2.1/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2_2', 'ip': '10.0.2.2/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2_3', 'ip': '10.0.2.3/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2_4', 'ip': '10.0.2.4/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2_5', 'ip': '10.0.2.5/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2_6', 'ip': '10.0.2.6/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2_7', 'ip': '10.0.2.7/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2_8', 'ip': '10.0.2.8/24', 'mac': None, 'max_ram': 512},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch'},
			{'ID': 's2', 'TYPE': 'OVSSwitch'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['s1', 's2']},
			{'ENDPOINTS': ['h1_1', 's1']},
			{'ENDPOINTS': ['h1_2', 's1']},
			{'ENDPOINTS': ['h1_3', 's1']},
			{'ENDPOINTS': ['h1_4', 's1']},
			{'ENDPOINTS': ['h1_5', 's1']},
			{'ENDPOINTS': ['h1_6', 's1']},
			{'ENDPOINTS': ['h1_7', 's1']},
			{'ENDPOINTS': ['h1_8', 's1']},
			{'ENDPOINTS': ['h2_1', 's2']},
			{'ENDPOINTS': ['h2_2', 's2']},
			{'ENDPOINTS': ['h2_3', 's2']},
			{'ENDPOINTS': ['h2_4', 's2']},
			{'ENDPOINTS': ['h2_5', 's2']},
			{'ENDPOINTS': ['h2_6', 's2']},
			{'ENDPOINTS': ['h2_7', 's2']},
			{'ENDPOINTS': ['h2_8', 's2']},
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
	datacentertopology_topology()
