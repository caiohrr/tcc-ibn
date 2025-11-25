"""
Mininet script generated automatically.
Topology: Linear_3_switches_6_hosts
Version: 1.0
Description: A linear network with 3 switches (s1, s2, s3) in series, and 2 hosts connected to each switch. All links have a 10ms delay.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def linear_3_switches_6_hosts_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 6 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')
	h3 = net.addHost('h3', ip='10.0.0.3/24')
	h4 = net.addHost('h4', ip='10.0.0.4/24')
	h5 = net.addHost('h5', ip='10.0.0.5/24')
	h6 = net.addHost('h6', ip='10.0.0.6/24')

	info('*** Adding 3 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')

	info('*** Creating 8 links\n')
	net.addLink(h1, s1, delay='10ms')
	net.addLink(h2, s1, delay='10ms')
	net.addLink(s1, s2, delay='10ms')
	net.addLink(h3, s2, delay='10ms')
	net.addLink(h4, s2, delay='10ms')
	net.addLink(s2, s3, delay='10ms')
	net.addLink(h5, s3, delay='10ms')
	net.addLink(h6, s3, delay='10ms')

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')
	net.get('s3').cmd('ovs-ofctl add-flow s3 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'linear_3_switches_6_hosts',
		'version': '1.0',
		'description': 'A linear network with 3 switches (s1, s2, s3) in series, and 2 hosts connected to each switch. All links have a 10ms delay.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': None},
			{'id': 'h6', 'ip': '10.0.0.6/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1'},
			{'ID': 's2'},
			{'ID': 's3'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'DELAY': '10ms'}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'DELAY': '10ms'}},
			{'ENDPOINTS': ['s1', 's2'], 'PARAMS': {'DELAY': '10ms'}},
			{'ENDPOINTS': ['h3', 's2'], 'PARAMS': {'DELAY': '10ms'}},
			{'ENDPOINTS': ['h4', 's2'], 'PARAMS': {'DELAY': '10ms'}},
			{'ENDPOINTS': ['s2', 's3'], 'PARAMS': {'DELAY': '10ms'}},
			{'ENDPOINTS': ['h5', 's3'], 'PARAMS': {'DELAY': '10ms'}},
			{'ENDPOINTS': ['h6', 's3'], 'PARAMS': {'DELAY': '10ms'}},
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
	linear_3_switches_6_hosts_topology()
