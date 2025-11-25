"""
Mininet script generated automatically.
Topology: Officesimulation
Version: 1.0
Description: Simulação de escritório com 40 hosts divididos em 4 departamentos, conectados a um switch central.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def officesimulation_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 40 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', cpu=0.9)
	h2 = net.addHost('h2', ip='10.0.0.2/24', cpu=0.9)
	h3 = net.addHost('h3', ip='10.0.0.3/24', cpu=0.9)
	h4 = net.addHost('h4', ip='10.0.0.4/24', cpu=0.9)
	h5 = net.addHost('h5', ip='10.0.0.5/24', cpu=0.9)
	h6 = net.addHost('h6', ip='10.0.0.6/24', cpu=0.9)
	h7 = net.addHost('h7', ip='10.0.0.7/24', cpu=0.9)
	h8 = net.addHost('h8', ip='10.0.0.8/24', cpu=0.9)
	h9 = net.addHost('h9', ip='10.0.0.9/24', cpu=0.9)
	h10 = net.addHost('h10', ip='10.0.0.10/24', cpu=0.9)
	h11 = net.addHost('h11', ip='10.0.0.11/24', mem='1024M')
	h12 = net.addHost('h12', ip='10.0.0.12/24', mem='1024M')
	h13 = net.addHost('h13', ip='10.0.0.13/24', mem='1024M')
	h14 = net.addHost('h14', ip='10.0.0.14/24', mem='1024M')
	h15 = net.addHost('h15', ip='10.0.0.15/24', mem='1024M')
	h16 = net.addHost('h16', ip='10.0.0.16/24', mem='1024M')
	h17 = net.addHost('h17', ip='10.0.0.17/24', mem='1024M')
	h18 = net.addHost('h18', ip='10.0.0.18/24', mem='1024M')
	h19 = net.addHost('h19', ip='10.0.0.19/24', mem='1024M')
	h20 = net.addHost('h20', ip='10.0.0.20/24', mem='1024M')
	h21 = net.addHost('h21', ip='10.0.0.21/24')
	h22 = net.addHost('h22', ip='10.0.0.22/24')
	h23 = net.addHost('h23', ip='10.0.0.23/24')
	h24 = net.addHost('h24', ip='10.0.0.24/24')
	h25 = net.addHost('h25', ip='10.0.0.25/24')
	h26 = net.addHost('h26', ip='10.0.0.26/24')
	h27 = net.addHost('h27', ip='10.0.0.27/24')
	h28 = net.addHost('h28', ip='10.0.0.28/24')
	h29 = net.addHost('h29', ip='10.0.0.29/24')
	h30 = net.addHost('h30', ip='10.0.0.30/24')
	h31 = net.addHost('h31', ip='10.0.0.31/24')
	h32 = net.addHost('h32', ip='10.0.0.32/24')
	h33 = net.addHost('h33', ip='10.0.0.33/24')
	h34 = net.addHost('h34', ip='10.0.0.34/24')
	h35 = net.addHost('h35', ip='10.0.0.35/24')
	h36 = net.addHost('h36', ip='10.0.0.36/24')
	h37 = net.addHost('h37', ip='10.0.0.37/24')
	h38 = net.addHost('h38', ip='10.0.0.38/24')
	h39 = net.addHost('h39', ip='10.0.0.39/24')
	h40 = net.addHost('h40', ip='10.0.0.40/24')

	info('*** Adding 5 switches\n')
	s_deptA = net.addSwitch('s_deptA')
	s_deptB = net.addSwitch('s_deptB')
	s_deptC = net.addSwitch('s_deptC')
	s_deptD = net.addSwitch('s_deptD')
	s_core = net.addSwitch('s_core')

	info('*** Creating 44 links\n')
	net.addLink(h1, s_deptA)
	net.addLink(h2, s_deptA)
	net.addLink(h3, s_deptA)
	net.addLink(h4, s_deptA)
	net.addLink(h5, s_deptA)
	net.addLink(h6, s_deptA)
	net.addLink(h7, s_deptA)
	net.addLink(h8, s_deptA)
	net.addLink(h9, s_deptA)
	net.addLink(h10, s_deptA)
	net.addLink(h11, s_deptB)
	net.addLink(h12, s_deptB)
	net.addLink(h13, s_deptB)
	net.addLink(h14, s_deptB)
	net.addLink(h15, s_deptB)
	net.addLink(h16, s_deptB)
	net.addLink(h17, s_deptB)
	net.addLink(h18, s_deptB)
	net.addLink(h19, s_deptB)
	net.addLink(h20, s_deptB)
	net.addLink(h21, s_deptC)
	net.addLink(h22, s_deptC)
	net.addLink(h23, s_deptC)
	net.addLink(h24, s_deptC)
	net.addLink(h25, s_deptC)
	net.addLink(h26, s_deptC)
	net.addLink(h27, s_deptC)
	net.addLink(h28, s_deptC)
	net.addLink(h29, s_deptC)
	net.addLink(h30, s_deptC)
	net.addLink(h31, s_deptD)
	net.addLink(h32, s_deptD)
	net.addLink(h33, s_deptD)
	net.addLink(h34, s_deptD)
	net.addLink(h35, s_deptD)
	net.addLink(h36, s_deptD)
	net.addLink(h37, s_deptD)
	net.addLink(h38, s_deptD)
	net.addLink(h39, s_deptD)
	net.addLink(h40, s_deptD)
	net.addLink(s_deptA, s_core)
	net.addLink(s_deptB, s_core)
	net.addLink(s_deptC, s_core)
	net.addLink(s_deptD, s_core)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s_deptA').cmd('ovs-ofctl add-flow s_deptA "priority=0,actions=normal"')
	net.get('s_deptB').cmd('ovs-ofctl add-flow s_deptB "priority=0,actions=normal"')
	net.get('s_deptC').cmd('ovs-ofctl add-flow s_deptC "priority=0,actions=normal"')
	net.get('s_deptD').cmd('ovs-ofctl add-flow s_deptD "priority=0,actions=normal"')
	net.get('s_core').cmd('ovs-ofctl add-flow s_core "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'officesimulation',
		'version': '1.0',
		'description': 'Simulação de escritório com 40 hosts divididos em 4 departamentos, conectados a um switch central.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h6', 'ip': '10.0.0.6/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h7', 'ip': '10.0.0.7/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h8', 'ip': '10.0.0.8/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h9', 'ip': '10.0.0.9/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h10', 'ip': '10.0.0.10/24', 'mac': None, 'max_cpu': 0.9},
			{'id': 'h11', 'ip': '10.0.0.11/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h12', 'ip': '10.0.0.12/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h13', 'ip': '10.0.0.13/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h14', 'ip': '10.0.0.14/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h15', 'ip': '10.0.0.15/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h16', 'ip': '10.0.0.16/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h17', 'ip': '10.0.0.17/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h18', 'ip': '10.0.0.18/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h19', 'ip': '10.0.0.19/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h20', 'ip': '10.0.0.20/24', 'mac': None, 'max_ram': 1024},
			{'id': 'h21', 'ip': '10.0.0.21/24', 'mac': None},
			{'id': 'h22', 'ip': '10.0.0.22/24', 'mac': None},
			{'id': 'h23', 'ip': '10.0.0.23/24', 'mac': None},
			{'id': 'h24', 'ip': '10.0.0.24/24', 'mac': None},
			{'id': 'h25', 'ip': '10.0.0.25/24', 'mac': None},
			{'id': 'h26', 'ip': '10.0.0.26/24', 'mac': None},
			{'id': 'h27', 'ip': '10.0.0.27/24', 'mac': None},
			{'id': 'h28', 'ip': '10.0.0.28/24', 'mac': None},
			{'id': 'h29', 'ip': '10.0.0.29/24', 'mac': None},
			{'id': 'h30', 'ip': '10.0.0.30/24', 'mac': None},
			{'id': 'h31', 'ip': '10.0.0.31/24', 'mac': None},
			{'id': 'h32', 'ip': '10.0.0.32/24', 'mac': None},
			{'id': 'h33', 'ip': '10.0.0.33/24', 'mac': None},
			{'id': 'h34', 'ip': '10.0.0.34/24', 'mac': None},
			{'id': 'h35', 'ip': '10.0.0.35/24', 'mac': None},
			{'id': 'h36', 'ip': '10.0.0.36/24', 'mac': None},
			{'id': 'h37', 'ip': '10.0.0.37/24', 'mac': None},
			{'id': 'h38', 'ip': '10.0.0.38/24', 'mac': None},
			{'id': 'h39', 'ip': '10.0.0.39/24', 'mac': None},
			{'id': 'h40', 'ip': '10.0.0.40/24', 'mac': None},
		],
		'switches': [
			{'ID': 's_deptA'},
			{'ID': 's_deptB'},
			{'ID': 's_deptC'},
			{'ID': 's_deptD'},
			{'ID': 's_core'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's_deptA']},
			{'ENDPOINTS': ['h2', 's_deptA']},
			{'ENDPOINTS': ['h3', 's_deptA']},
			{'ENDPOINTS': ['h4', 's_deptA']},
			{'ENDPOINTS': ['h5', 's_deptA']},
			{'ENDPOINTS': ['h6', 's_deptA']},
			{'ENDPOINTS': ['h7', 's_deptA']},
			{'ENDPOINTS': ['h8', 's_deptA']},
			{'ENDPOINTS': ['h9', 's_deptA']},
			{'ENDPOINTS': ['h10', 's_deptA']},
			{'ENDPOINTS': ['h11', 's_deptB']},
			{'ENDPOINTS': ['h12', 's_deptB']},
			{'ENDPOINTS': ['h13', 's_deptB']},
			{'ENDPOINTS': ['h14', 's_deptB']},
			{'ENDPOINTS': ['h15', 's_deptB']},
			{'ENDPOINTS': ['h16', 's_deptB']},
			{'ENDPOINTS': ['h17', 's_deptB']},
			{'ENDPOINTS': ['h18', 's_deptB']},
			{'ENDPOINTS': ['h19', 's_deptB']},
			{'ENDPOINTS': ['h20', 's_deptB']},
			{'ENDPOINTS': ['h21', 's_deptC']},
			{'ENDPOINTS': ['h22', 's_deptC']},
			{'ENDPOINTS': ['h23', 's_deptC']},
			{'ENDPOINTS': ['h24', 's_deptC']},
			{'ENDPOINTS': ['h25', 's_deptC']},
			{'ENDPOINTS': ['h26', 's_deptC']},
			{'ENDPOINTS': ['h27', 's_deptC']},
			{'ENDPOINTS': ['h28', 's_deptC']},
			{'ENDPOINTS': ['h29', 's_deptC']},
			{'ENDPOINTS': ['h30', 's_deptC']},
			{'ENDPOINTS': ['h31', 's_deptD']},
			{'ENDPOINTS': ['h32', 's_deptD']},
			{'ENDPOINTS': ['h33', 's_deptD']},
			{'ENDPOINTS': ['h34', 's_deptD']},
			{'ENDPOINTS': ['h35', 's_deptD']},
			{'ENDPOINTS': ['h36', 's_deptD']},
			{'ENDPOINTS': ['h37', 's_deptD']},
			{'ENDPOINTS': ['h38', 's_deptD']},
			{'ENDPOINTS': ['h39', 's_deptD']},
			{'ENDPOINTS': ['h40', 's_deptD']},
			{'ENDPOINTS': ['s_deptA', 's_core']},
			{'ENDPOINTS': ['s_deptB', 's_core']},
			{'ENDPOINTS': ['s_deptC', 's_core']},
			{'ENDPOINTS': ['s_deptD', 's_core']},
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
	officesimulation_topology()
