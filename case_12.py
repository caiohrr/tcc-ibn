"""
Mininet script generated automatically.
Topology: Core_switch_topology
Version: 1.0
Description: Topology with 15 hosts, 3 switches (5 hosts per switch). Switch 1 is core and its hosts have 80% CPU priority.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def core_switch_topology_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 15 hosts\n')
	h1_1 = net.addHost('h1_1', ip='10.0.0.1/24', cpu=0.8)
	h1_2 = net.addHost('h1_2', ip='10.0.0.2/24', cpu=0.8)
	h1_3 = net.addHost('h1_3', ip='10.0.0.3/24', cpu=0.8)
	h1_4 = net.addHost('h1_4', ip='10.0.0.4/24', cpu=0.8)
	h1_5 = net.addHost('h1_5', ip='10.0.0.5/24', cpu=0.8)
	h2_1 = net.addHost('h2_1', ip='10.0.1.1/24')
	h2_2 = net.addHost('h2_2', ip='10.0.1.2/24')
	h2_3 = net.addHost('h2_3', ip='10.0.1.3/24')
	h2_4 = net.addHost('h2_4', ip='10.0.1.4/24')
	h2_5 = net.addHost('h2_5', ip='10.0.1.5/24')
	h3_1 = net.addHost('h3_1', ip='10.0.2.1/24')
	h3_2 = net.addHost('h3_2', ip='10.0.2.2/24')
	h3_3 = net.addHost('h3_3', ip='10.0.2.3/24')
	h3_4 = net.addHost('h3_4', ip='10.0.2.4/24')
	h3_5 = net.addHost('h3_5', ip='10.0.2.5/24')

	info('*** Adding 3 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')

	info('*** Creating 17 links\n')
	net.addLink(h1_1, s1)
	net.addLink(h1_2, s1)
	net.addLink(h1_3, s1)
	net.addLink(h1_4, s1)
	net.addLink(h1_5, s1)
	net.addLink(h2_1, s2)
	net.addLink(h2_2, s2)
	net.addLink(h2_3, s2)
	net.addLink(h2_4, s2)
	net.addLink(h2_5, s2)
	net.addLink(h3_1, s3)
	net.addLink(h3_2, s3)
	net.addLink(h3_3, s3)
	net.addLink(h3_4, s3)
	net.addLink(h3_5, s3)
	net.addLink(s1, s2)
	net.addLink(s1, s3)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')
	net.get('s3').cmd('ovs-ofctl add-flow s3 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'core_switch_topology',
		'version': '1.0',
		'description': 'Topology with 15 hosts, 3 switches (5 hosts per switch). Switch 1 is core and its hosts have 80% CPU priority.',
		'hosts': [
			{'id': 'h1_1', 'ip': '10.0.0.1/24', 'mac': None, 'max_cpu': 0.8},
			{'id': 'h1_2', 'ip': '10.0.0.2/24', 'mac': None, 'max_cpu': 0.8},
			{'id': 'h1_3', 'ip': '10.0.0.3/24', 'mac': None, 'max_cpu': 0.8},
			{'id': 'h1_4', 'ip': '10.0.0.4/24', 'mac': None, 'max_cpu': 0.8},
			{'id': 'h1_5', 'ip': '10.0.0.5/24', 'mac': None, 'max_cpu': 0.8},
			{'id': 'h2_1', 'ip': '10.0.1.1/24', 'mac': None},
			{'id': 'h2_2', 'ip': '10.0.1.2/24', 'mac': None},
			{'id': 'h2_3', 'ip': '10.0.1.3/24', 'mac': None},
			{'id': 'h2_4', 'ip': '10.0.1.4/24', 'mac': None},
			{'id': 'h2_5', 'ip': '10.0.1.5/24', 'mac': None},
			{'id': 'h3_1', 'ip': '10.0.2.1/24', 'mac': None},
			{'id': 'h3_2', 'ip': '10.0.2.2/24', 'mac': None},
			{'id': 'h3_3', 'ip': '10.0.2.3/24', 'mac': None},
			{'id': 'h3_4', 'ip': '10.0.2.4/24', 'mac': None},
			{'id': 'h3_5', 'ip': '10.0.2.5/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch'},
			{'ID': 's2', 'TYPE': 'OVSSwitch'},
			{'ID': 's3', 'TYPE': 'OVSSwitch'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1_1', 's1']},
			{'ENDPOINTS': ['h1_2', 's1']},
			{'ENDPOINTS': ['h1_3', 's1']},
			{'ENDPOINTS': ['h1_4', 's1']},
			{'ENDPOINTS': ['h1_5', 's1']},
			{'ENDPOINTS': ['h2_1', 's2']},
			{'ENDPOINTS': ['h2_2', 's2']},
			{'ENDPOINTS': ['h2_3', 's2']},
			{'ENDPOINTS': ['h2_4', 's2']},
			{'ENDPOINTS': ['h2_5', 's2']},
			{'ENDPOINTS': ['h3_1', 's3']},
			{'ENDPOINTS': ['h3_2', 's3']},
			{'ENDPOINTS': ['h3_3', 's3']},
			{'ENDPOINTS': ['h3_4', 's3']},
			{'ENDPOINTS': ['h3_5', 's3']},
			{'ENDPOINTS': ['s1', 's2']},
			{'ENDPOINTS': ['s1', 's3']},
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
	core_switch_topology_topology()
