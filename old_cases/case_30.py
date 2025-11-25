"""
Mininet script generated automatically.
Topology: Highavailabilitynet
Version: 1.0
Description: High availability environment with aggressive monitoring.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def highavailabilitynet_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, waitConnected=True)

	info('*** Adding 1 controllers\n')
	c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

	info('*** Adding 2 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 2 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)

	info('*** Starting network\n')
	net.start()

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'highavailabilitynet',
		'version': '1.0',
		'description': 'High availability environment with aggressive monitoring.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
			{'ID': 'c0', 'TYPE': 'RemoteController', 'PARAMS': {'IP': '127.0.0.1', 'PORT': 6653}},
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1']},
			{'ENDPOINTS': ['h2', 's1']},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 2
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
	highavailabilitynet_topology()
