"""
Mininet script generated automatically.
Topology: Simple_server_client_net
Version: 1.0
Description: A simple network connecting a server and a client to a core switch.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def simple_server_client_net_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 2 hosts\n')
	servidor = net.addHost('servidor', ip='10.0.0.10/24')
	cliente = net.addHost('cliente', ip='10.0.0.20/24')

	info('*** Adding 1 switches\n')
	core = net.addSwitch('s1')

	info('*** Creating 2 links\n')
	net.addLink(servidor, core)
	net.addLink(cliente, core)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'simple_server_client_net',
		'version': '1.0',
		'description': 'A simple network connecting a server and a client to a core switch.',
		'hosts': [
			{'id': 'servidor', 'ip': '10.0.0.10/24', 'mac': None},
			{'id': 'cliente', 'ip': '10.0.0.20/24', 'mac': None},
		],
		'switches': [
			{'ID': 'core'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['servidor', 'core']},
			{'ENDPOINTS': ['cliente', 'core']},
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
	simple_server_client_net_topology()
