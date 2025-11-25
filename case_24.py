"""
Mininet script generated automatically.
Topology: Binarytreetopology
Version: 1.0
Description: A binary tree topology with 7 switches and 12 hosts (3 per leaf switch).
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def binarytreetopology_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 12 hosts\n')
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

	info('*** Adding 7 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')
	s5 = net.addSwitch('s5')
	s6 = net.addSwitch('s6')
	s7 = net.addSwitch('s7')

	info('*** Creating 18 links\n')
	net.addLink(s1, s2)
	net.addLink(s1, s3)
	net.addLink(s2, s4)
	net.addLink(s2, s5)
	net.addLink(s3, s6)
	net.addLink(s3, s7)
	net.addLink(h1, s4)
	net.addLink(h2, s4)
	net.addLink(h3, s4)
	net.addLink(h4, s5)
	net.addLink(h5, s5)
	net.addLink(h6, s5)
	net.addLink(h7, s6)
	net.addLink(h8, s6)
	net.addLink(h9, s6)
	net.addLink(h10, s7)
	net.addLink(h11, s7)
	net.addLink(h12, s7)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')
	net.get('s3').cmd('ovs-ofctl add-flow s3 "priority=0,actions=normal"')
	net.get('s4').cmd('ovs-ofctl add-flow s4 "priority=0,actions=normal"')
	net.get('s5').cmd('ovs-ofctl add-flow s5 "priority=0,actions=normal"')
	net.get('s6').cmd('ovs-ofctl add-flow s6 "priority=0,actions=normal"')
	net.get('s7').cmd('ovs-ofctl add-flow s7 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'binarytreetopology',
		'version': '1.0',
		'description': 'A binary tree topology with 7 switches and 12 hosts (3 per leaf switch).',
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
		],
		'switches': [
			{'ID': 's1'},
			{'ID': 's2'},
			{'ID': 's3'},
			{'ID': 's4'},
			{'ID': 's5'},
			{'ID': 's6'},
			{'ID': 's7'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['s1', 's2']},
			{'ENDPOINTS': ['s1', 's3']},
			{'ENDPOINTS': ['s2', 's4']},
			{'ENDPOINTS': ['s2', 's5']},
			{'ENDPOINTS': ['s3', 's6']},
			{'ENDPOINTS': ['s3', 's7']},
			{'ENDPOINTS': ['h1', 's4']},
			{'ENDPOINTS': ['h2', 's4']},
			{'ENDPOINTS': ['h3', 's4']},
			{'ENDPOINTS': ['h4', 's5']},
			{'ENDPOINTS': ['h5', 's5']},
			{'ENDPOINTS': ['h6', 's5']},
			{'ENDPOINTS': ['h7', 's6']},
			{'ENDPOINTS': ['h8', 's6']},
			{'ENDPOINTS': ['h9', 's6']},
			{'ENDPOINTS': ['h10', 's7']},
			{'ENDPOINTS': ['h11', 's7']},
			{'ENDPOINTS': ['h12', 's7']},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 10
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
	binarytreetopology_topology()
