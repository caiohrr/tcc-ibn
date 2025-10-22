"""
Mininet script generated automatically.
Topology: Simplestar_simple
Version: 1.0
Description: Uma topologia estrela com parâmetros de link e recursos de host, sem ips para os hosts.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def simplestar_simple_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', mac='00:00:00:00:00:01', cpu=0.05)
	h2 = net.addHost('h2', mac='00:00:00:00:00:02', mem='10M')
	h3 = net.addHost('h3', mac='00:00:00:00:00:03', cpu=0.33, mem='300M')
	h4 = net.addHost('h4', mac='00:00:00:00:00:04')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 4 links\n')
	net.addLink(h1, s1, bw=100, delay='5ms')
	net.addLink(h2, s1, bw=50, delay='10ms', loss=1)
	net.addLink(h3, s1, bw=100, delay='5ms')
	net.addLink(h4, s1, bw=80, delay='7ms')

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'simplestar_simple',
		'version': '1.0',
		'description': 'Uma topologia estrela com parâmetros de link e recursos de host, sem ips para os hosts.',
		'hosts': [
			{'id': 'h1', 'ip': None, 'mac': '00:00:00:00:00:01', 'max_cpu': 0.05},
			{'id': 'h2', 'ip': None, 'mac': '00:00:00:00:00:02', 'max_ram': 10},
			{'id': 'h3', 'ip': None, 'mac': '00:00:00:00:00:03', 'max_cpu': 0.33, 'max_ram': 300},
			{'id': 'h4', 'ip': None, 'mac': '00:00:00:00:00:04'},
		],
		'switches': [
			{'ID': 's1', 'PARAMS': {}},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '5ms'}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'BANDWIDTH': 50, 'DELAY': '10ms', 'LOSS': 1}},
			{'ENDPOINTS': ['h3', 's1'], 'PARAMS': {'BANDWIDTH': 100, 'DELAY': '5ms'}},
			{'ENDPOINTS': ['h4', 's1'], 'PARAMS': {'BANDWIDTH': 80, 'DELAY': '7ms'}},
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
	simplestar_simple_topology()
