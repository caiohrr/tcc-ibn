"""
Mininet script generated automatically.
Topology: Fivehostnetwork
Version: 1.0
Description: A network with 5 hosts. Host h1 is a server with high resources, and h2-h5 are clients with limited CPU.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def fivehostnetwork_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 5 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01', cpu=1.0, mem='1024M')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02', cpu=0.2)
	h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03', cpu=0.2)
	h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04', cpu=0.2)
	h5 = net.addHost('h5', ip='10.0.0.5/24', mac='00:00:00:00:00:05', cpu=0.2)

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 5 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s1)
	net.addLink(h4, s1)
	net.addLink(h5, s1)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'fivehostnetwork',
		'version': '1.0',
		'description': 'A network with 5 hosts. Host h1 is a server with high resources, and h2-h5 are clients with limited CPU.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': '00:00:00:00:00:01', 'max_cpu': 1.0, 'max_ram': 1024},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': '00:00:00:00:00:02', 'max_cpu': 0.2},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': '00:00:00:00:00:03', 'max_cpu': 0.2},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': '00:00:00:00:00:04', 'max_cpu': 0.2},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': '00:00:00:00:00:05', 'max_cpu': 0.2},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1']},
			{'ENDPOINTS': ['h2', 's1']},
			{'ENDPOINTS': ['h3', 's1']},
			{'ENDPOINTS': ['h4', 's1']},
			{'ENDPOINTS': ['h5', 's1']},
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
	fivehostnetwork_topology()
