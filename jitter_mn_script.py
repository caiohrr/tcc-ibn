"""
Mininet script generated automatically.
Topology: Jitter
Version: 1.0
Description: Uma topologia de exemplo
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def jitter_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, waitConnected=True)

	info('*** Adding 1 controllers\n')
	c0 = net.addController('c0')

	info('*** Adding 2 hosts\n')
	h1 = net.addHost('h1', ip='192.168.1.1/24', mac='00:00:00:00:00:11')
	h2 = net.addHost('h2', ip='192.168.1.2/24', mac='00:00:00:00:00:12')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 2 links\n')
	net.addLink(h1, s1, bw=200, delay='2ms', jitter=5)
	net.addLink(h2, s1, bw=100, delay='3ms', loss=0.5, jitter=10)

	info('*** Starting network\n')
	net.start()

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'jitter',
		'version': '1.0',
		'description': 'Uma topologia de exemplo',
		'hosts': [
			{'id': 'h1', 'ip': '192.168.1.1/24', 'mac': '00:00:00:00:00:11'},
			{'id': 'h2', 'ip': '192.168.1.2/24', 'mac': '00:00:00:00:00:12'},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
			{'ID': 'c0', 'TYPE': 'Controller', 'PARAMS': {'IP': '127.0.0.1', 'PORT': 6653}},
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 200, 'DELAY': '2ms', 'JITTER': 5}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '3ms', 'LOSS': 0.5, 'JITTER': 10}},
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
	jitter_topology()
