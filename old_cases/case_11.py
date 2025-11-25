"""
Mininet script generated automatically.
Topology: H1_h2_to_s1
Version: 1.0
Description: Connects h1 and h2 to s1, with 100Mbps bandwidth on h1-s1 link.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def h1_h2_to_s1_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 2 hosts\n')
	h1 = net.addHost('h1')
	h2 = net.addHost('h2')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 2 links\n')
	net.addLink(h1, s1, bw=100)
	net.addLink(h2, s1)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'h1_h2_to_s1',
		'version': '1.0',
		'description': 'Connects h1 and h2 to s1, with 100Mbps bandwidth on h1-s1 link.',
		'hosts': [
			{'id': 'h1', 'ip': None, 'mac': None},
			{'id': 'h2', 'ip': None, 'mac': None},
		],
		'switches': [
			{'ID': 's1'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
			{'ENDPOINTS': ['h2', 's1']},
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
	h1_h2_to_s1_topology()
