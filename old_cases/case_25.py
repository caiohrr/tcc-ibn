"""
Mininet script generated automatically.
Topology: Simple_h1_s1_net
Version: 1.0
Description: Host h1 connected to switch s1 with monitoring enabled.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def simple_h1_s1_net_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 1 hosts\n')
	h1 = net.addHost('h1', cpu=0.5)

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 1 links\n')
	net.addLink(h1, s1, bw=100)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'simple_h1_s1_net',
		'version': '1.0',
		'description': 'Host h1 connected to switch s1 with monitoring enabled.',
		'hosts': [
			{'id': 'h1', 'ip': None, 'mac': None, 'max_cpu': 0.5},
		],
		'switches': [
			{'ID': 's1', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 100}},
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
	simple_h1_s1_net_topology()
