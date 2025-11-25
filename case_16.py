"""
Mininet script generated automatically.
Topology: Sixteenhostnetwork
Version: 1.0
Description: A network with 16 hosts divided among 4 switches, with aggressive monitoring. Hosts on s1 have a memory limit.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def sixteenhostnetwork_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 16 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', mem='256M')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mem='256M')
	h3 = net.addHost('h3', ip='10.0.0.3/24', mem='256M')
	h4 = net.addHost('h4', ip='10.0.0.4/24', mem='256M')
	h5 = net.addHost('h5', ip='10.0.0.5/24')
	h6 = net.addHost('h6', ip='10.0.0.6/24')
	h7 = net.addHost('h7', ip='10.0.0.7/24')
	h8 = net.addHost('h8', ip='10.0.0.8/24')
	h9 = net.addHost('h9', ip='10.0.0.9/24')
	h10 = net.addHost('h10', ip='10.0.0.10/24')
	h11 = net.addHost('h11', ip='10.0.0.11/24')
	h12 = net.addHost('h12', ip='10.0.0.12/24')
	h13 = net.addHost('h13', ip='10.0.0.13/24')
	h14 = net.addHost('h14', ip='10.0.0.14/24')
	h15 = net.addHost('h15', ip='10.0.0.15/24')
	h16 = net.addHost('h16', ip='10.0.0.16/24')

	info('*** Adding 4 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	s4 = net.addSwitch('s4')

	info('*** Creating 16 links\n')
	net.addLink(h1, s1)
	net.addLink(h2, s1)
	net.addLink(h3, s1)
	net.addLink(h4, s1)
	net.addLink(h5, s2)
	net.addLink(h6, s2)
	net.addLink(h7, s2)
	net.addLink(h8, s2)
	net.addLink(h9, s3)
	net.addLink(h10, s3)
	net.addLink(h11, s3)
	net.addLink(h12, s3)
	net.addLink(h13, s4)
	net.addLink(h14, s4)
	net.addLink(h15, s4)
	net.addLink(h16, s4)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')
	net.get('s3').cmd('ovs-ofctl add-flow s3 "priority=0,actions=normal"')
	net.get('s4').cmd('ovs-ofctl add-flow s4 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'sixteenhostnetwork',
		'version': '1.0',
		'description': 'A network with 16 hosts divided among 4 switches, with aggressive monitoring. Hosts on s1 have a memory limit.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None, 'max_ram': 256},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None, 'max_ram': 256},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None, 'max_ram': 256},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None, 'max_ram': 256},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': None},
			{'id': 'h6', 'ip': '10.0.0.6/24', 'mac': None},
			{'id': 'h7', 'ip': '10.0.0.7/24', 'mac': None},
			{'id': 'h8', 'ip': '10.0.0.8/24', 'mac': None},
			{'id': 'h9', 'ip': '10.0.0.9/24', 'mac': None},
			{'id': 'h10', 'ip': '10.0.0.10/24', 'mac': None},
			{'id': 'h11', 'ip': '10.0.0.11/24', 'mac': None},
			{'id': 'h12', 'ip': '10.0.0.12/24', 'mac': None},
			{'id': 'h13', 'ip': '10.0.0.13/24', 'mac': None},
			{'id': 'h14', 'ip': '10.0.0.14/24', 'mac': None},
			{'id': 'h15', 'ip': '10.0.0.15/24', 'mac': None},
			{'id': 'h16', 'ip': '10.0.0.16/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1'},
			{'ID': 's2'},
			{'ID': 's3'},
			{'ID': 's4'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1']},
			{'ENDPOINTS': ['h2', 's1']},
			{'ENDPOINTS': ['h3', 's1']},
			{'ENDPOINTS': ['h4', 's1']},
			{'ENDPOINTS': ['h5', 's2']},
			{'ENDPOINTS': ['h6', 's2']},
			{'ENDPOINTS': ['h7', 's2']},
			{'ENDPOINTS': ['h8', 's2']},
			{'ENDPOINTS': ['h9', 's3']},
			{'ENDPOINTS': ['h10', 's3']},
			{'ENDPOINTS': ['h11', 's3']},
			{'ENDPOINTS': ['h12', 's3']},
			{'ENDPOINTS': ['h13', 's4']},
			{'ENDPOINTS': ['h14', 's4']},
			{'ENDPOINTS': ['h15', 's4']},
			{'ENDPOINTS': ['h16', 's4']},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 2
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
	sixteenhostnetwork_topology()
