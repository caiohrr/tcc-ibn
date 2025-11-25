"""
Mininet script generated automatically.
Topology: Ring_4_switches_1_host_per_switch
Version: 1.0
Description: A ring topology with 4 switches (s1-s2-s3-s4-s1) and one host connected to each switch. Inter-switch links have 500Mbps bandwidth.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def ring_4_switches_1_host_per_switch_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')
	h3 = net.addHost('h3', ip='10.0.0.3/24')
	h4 = net.addHost('h4', ip='10.0.0.4/24')

	info('*** Adding 4 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')

	info('*** Creating 8 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s2)
	net.addLink(h3, s3)
	net.addLink(h4, s4)
	net.addLink(s1, s2, bw=500)
	net.addLink(s2, s3, bw=500)
	net.addLink(s3, s4, bw=500)
	net.addLink(s4, s1, bw=500)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')
	net.get('s3').cmd('ovs-ofctl add-flow s3 "priority=0,actions=normal"')
	net.get('s4').cmd('ovs-ofctl add-flow s4 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'ring_4_switches_1_host_per_switch',
		'version': '1.0',
		'description': 'A ring topology with 4 switches (s1-s2-s3-s4-s1) and one host connected to each switch. Inter-switch links have 500Mbps bandwidth.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1'},
			{'ID': 's2'},
			{'ID': 's3'},
			{'ID': 's4'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1']},
			{'ENDPOINTS': ['h2', 's2']},
			{'ENDPOINTS': ['h3', 's3']},
			{'ENDPOINTS': ['h4', 's4']},
			{'ENDPOINTS': ['s1', 's2'], 'PARAMS': {'BANDWIDTH': 500}},
			{'ENDPOINTS': ['s2', 's3'], 'PARAMS': {'BANDWIDTH': 500}},
			{'ENDPOINTS': ['s3', 's4'], 'PARAMS': {'BANDWIDTH': 500}},
			{'ENDPOINTS': ['s4', 's1'], 'PARAMS': {'BANDWIDTH': 500}},
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
	ring_4_switches_1_host_per_switch_topology()
