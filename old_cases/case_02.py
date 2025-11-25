"""
Mininet script generated automatically.
Topology: Linear_h_s_h
Version: 1.0
Description: A simple linear topology with two hosts connected to a single switch.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def linear_h_s_h_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 2 hosts\n')
	hA = net.addHost('hA', ip='10.0.0.1/24')
	hB = net.addHost('hB', ip='10.0.0.2/24')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 2 links\n')
	net.addLink(hA, s1)
	net.addLink(hB, s1)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'linear_h_s_h',
		'version': '1.0',
		'description': 'A simple linear topology with two hosts connected to a single switch.',
		'hosts': [
			{'id': 'hA', 'ip': '10.0.0.1/24', 'mac': None},
			{'id': 'hB', 'ip': '10.0.0.2/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['hA', 's1']},
			{'ENDPOINTS': ['hB', 's1']},
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
	linear_h_s_h_topology()
