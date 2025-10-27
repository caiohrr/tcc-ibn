"""
Mininet script generated automatically.
Topology: Star_topology_4_hosts
Version: 1.0
Description: A star topology with four hosts connected to a central switch, each on a different subnet.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def star_topology_4_hosts_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	#info('*** Adding 1 controllers\n')
	#c0 = net.addController('c0')

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02')
	h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03')
	h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 4 links\n')
	net.addLink(h1, s1, bw=100, delay='2ms')
	net.addLink(h2, s1, bw=100, delay='2ms')
	net.addLink(h3, s1, bw=100, delay='2ms')
	net.addLink(h4, s1, bw=100, delay='2ms')

	info('*** Starting network\n')
	net.start()

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'star_topology_4_hosts',
		'version': '1.0',
		'description': 'A star topology with four hosts connected to a central switch, each on a different subnet.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': '00:00:00:00:00:01'},
			{'id': 'h2', 'ip': '20.0.0.1/24', 'mac': '00:00:00:00:00:02'},
			{'id': 'h3', 'ip': '30.0.0.1/24', 'mac': '00:00:00:00:00:03'},
			{'id': 'h4', 'ip': '40.0.0.1/24', 'mac': '00:00:00:00:00:04'},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
			{'ID': 'c0', 'TYPE': 'Controller', 'PARAMS': {'IP': '127.0.0.1', 'PORT': 6653}},
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '2ms'}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '2ms'}},
			{'ENDPOINTS': ['h3', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '2ms'}},
			{'ENDPOINTS': ['h4', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '2ms'}},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 5
	monitor.recovery_enabled = False
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
	star_topology_4_hosts_topology()
