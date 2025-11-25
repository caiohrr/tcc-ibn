"""
Mininet script generated automatically.
Topology: 25_hosts_on_s1_challenge
Version: 1.0
Description: Topology with 25 hosts connected to a single switch s1, with specific IP addressing (10.0.X.1/24) and 50% CPU limit for all hosts.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def 25_hosts_on_s1_challenge_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 25 hosts\n')
	h1 = net.addHost('h1', ip='10.0.1.1/24', cpu=0.5)
	h2 = net.addHost('h2', ip='10.0.2.1/24', cpu=0.5)
	h3 = net.addHost('h3', ip='10.0.3.1/24', cpu=0.5)
	h4 = net.addHost('h4', ip='10.0.4.1/24', cpu=0.5)
	h5 = net.addHost('h5', ip='10.0.5.1/24', cpu=0.5)
	h6 = net.addHost('h6', ip='10.0.6.1/24', cpu=0.5)
	h7 = net.addHost('h7', ip='10.0.7.1/24', cpu=0.5)
	h8 = net.addHost('h8', ip='10.0.8.1/24', cpu=0.5)
	h9 = net.addHost('h9', ip='10.0.9.1/24', cpu=0.5)
	h10 = net.addHost('h10', ip='10.0.10.1/24', cpu=0.5)
	h11 = net.addHost('h11', ip='10.0.11.1/24', cpu=0.5)
	h12 = net.addHost('h12', ip='10.0.12.1/24', cpu=0.5)
	h13 = net.addHost('h13', ip='10.0.13.1/24', cpu=0.5)
	h14 = net.addHost('h14', ip='10.0.14.1/24', cpu=0.5)
	h15 = net.addHost('h15', ip='10.0.15.1/24', cpu=0.5)
	h16 = net.addHost('h16', ip='10.0.16.1/24', cpu=0.5)
	h17 = net.addHost('h17', ip='10.0.17.1/24', cpu=0.5)
	h18 = net.addHost('h18', ip='10.0.18.1/24', cpu=0.5)
	h19 = net.addHost('h19', ip='10.0.19.1/24', cpu=0.5)
	h20 = net.addHost('h20', ip='10.0.20.1/24', cpu=0.5)
	h21 = net.addHost('h21', ip='10.0.21.1/24', cpu=0.5)
	h22 = net.addHost('h22', ip='10.0.22.1/24', cpu=0.5)
	h23 = net.addHost('h23', ip='10.0.23.1/24', cpu=0.5)
	h24 = net.addHost('h24', ip='10.0.24.1/24', cpu=0.5)
	h25 = net.addHost('h25', ip='10.0.25.1/24', cpu=0.5)

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 25 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s1)
	net.addLink(h4, s1)
	net.addLink(h5, s1)
	net.addLink(h6, s1)
	net.addLink(h7, s1)
	net.addLink(h8, s1)
	net.addLink(h9, s1)
	net.addLink(h10, s1)
	net.addLink(h11, s1)
	net.addLink(h12, s1)
	net.addLink(h13, s1)
	net.addLink(h14, s1)
	net.addLink(h15, s1)
	net.addLink(h16, s1)
	net.addLink(h17, s1)
	net.addLink(h18, s1)
	net.addLink(h19, s1)
	net.addLink(h20, s1)
	net.addLink(h21, s1)
	net.addLink(h22, s1)
	net.addLink(h23, s1)
	net.addLink(h24, s1)
	net.addLink(h25, s1)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': '25_hosts_on_s1_challenge',
		'version': '1.0',
		'description': 'Topology with 25 hosts connected to a single switch s1, with specific IP addressing (10.0.X.1/24) and 50% CPU limit for all hosts.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.1.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h2', 'ip': '10.0.2.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h3', 'ip': '10.0.3.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h4', 'ip': '10.0.4.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h5', 'ip': '10.0.5.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h6', 'ip': '10.0.6.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h7', 'ip': '10.0.7.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h8', 'ip': '10.0.8.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h9', 'ip': '10.0.9.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h10', 'ip': '10.0.10.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h11', 'ip': '10.0.11.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h12', 'ip': '10.0.12.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h13', 'ip': '10.0.13.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h14', 'ip': '10.0.14.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h15', 'ip': '10.0.15.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h16', 'ip': '10.0.16.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h17', 'ip': '10.0.17.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h18', 'ip': '10.0.18.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h19', 'ip': '10.0.19.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h20', 'ip': '10.0.20.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h21', 'ip': '10.0.21.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h22', 'ip': '10.0.22.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h23', 'ip': '10.0.23.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h24', 'ip': '10.0.24.1/24', 'mac': None, 'max_cpu': 0.5},
			{'id': 'h25', 'ip': '10.0.25.1/24', 'mac': None, 'max_cpu': 0.5},
		],
		'switches': [
			{'ID': 's1'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1']},
			{'ENDPOINTS': ['h2', 's1']},
			{'ENDPOINTS': ['h3', 's1']},
			{'ENDPOINTS': ['h4', 's1']},
			{'ENDPOINTS': ['h5', 's1']},
			{'ENDPOINTS': ['h6', 's1']},
			{'ENDPOINTS': ['h7', 's1']},
			{'ENDPOINTS': ['h8', 's1']},
			{'ENDPOINTS': ['h9', 's1']},
			{'ENDPOINTS': ['h10', 's1']},
			{'ENDPOINTS': ['h11', 's1']},
			{'ENDPOINTS': ['h12', 's1']},
			{'ENDPOINTS': ['h13', 's1']},
			{'ENDPOINTS': ['h14', 's1']},
			{'ENDPOINTS': ['h15', 's1']},
			{'ENDPOINTS': ['h16', 's1']},
			{'ENDPOINTS': ['h17', 's1']},
			{'ENDPOINTS': ['h18', 's1']},
			{'ENDPOINTS': ['h19', 's1']},
			{'ENDPOINTS': ['h20', 's1']},
			{'ENDPOINTS': ['h21', 's1']},
			{'ENDPOINTS': ['h22', 's1']},
			{'ENDPOINTS': ['h23', 's1']},
			{'ENDPOINTS': ['h24', 's1']},
			{'ENDPOINTS': ['h25', 's1']},
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
	25_hosts_on_s1_challenge_topology()
