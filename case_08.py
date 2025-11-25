"""
Mininet script generated automatically.
Topology: Four_hosts_remote_controller
Version: 1.0
Description: Topology with 4 hosts connected to a single switch, managed by a remote controller. All hosts have 512MB RAM.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def four_hosts_remote_controller_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, waitConnected=True)

	info('*** Adding 1 controllers\n')
	c0 = net.addController('c0', controller=RemoteController, ip='192.168.56.1', port=6633)

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', mem='512M')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mem='512M')
	h3 = net.addHost('h3', ip='10.0.0.3/24', mem='512M')
	h4 = net.addHost('h4', ip='10.0.0.4/24', mem='512M')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 4 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s1)
	net.addLink(h4, s1)

	info('*** Starting network\n')
	net.start()

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'four_hosts_remote_controller',
		'version': '1.0',
		'description': 'Topology with 4 hosts connected to a single switch, managed by a remote controller. All hosts have 512MB RAM.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None, 'max_ram': 512},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None, 'max_ram': 512},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None, 'max_ram': 512},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None, 'max_ram': 512},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
			{'ID': 'c0', 'TYPE': 'RemoteController', 'PARAMS': {'IP': '192.168.56.1', 'PORT': 6633}},
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1']},
			{'ENDPOINTS': ['h2', 's1']},
			{'ENDPOINTS': ['h3', 's1']},
			{'ENDPOINTS': ['h4', 's1']},
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
	four_hosts_remote_controller_topology()
