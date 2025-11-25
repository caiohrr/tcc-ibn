"""
Mininet script generated automatically.
Topology: Star_topology_4_hosts
Version: 1.0
Description: A star topology with one central switch (s1) and four connected hosts (h1-h4).
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
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', cpu=0.6)
	h2 = net.addHost('h2', ip='10.0.0.2/24', mem='512M')
	h3 = net.addHost('h3', ip='10.0.0.3/24')
	h4 = net.addHost('h4', ip='10.0.0.4/24')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 4 links\n')
	net.addLink(h1, s1, bw=100, delay='2ms')
	net.addLink(h2, s1, bw=100)
	net.addLink(h3, s1, bw=50, loss=0.5)
	net.addLink(h4, s1)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'star_topology_4_hosts',
		'version': '1.0',
		'description': 'A star topology with one central switch (s1) and four connected hosts (h1-h4).',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None, 'max_cpu': 0.6},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None, 'max_ram': 512},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '2ms'}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h3', 's1'], 'PARAMS': {'BANDWIDTH': 50, 'LOSS': 0.5}},
			{'ENDPOINTS': ['h4', 's1']},
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
