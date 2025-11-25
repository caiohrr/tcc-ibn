"""
Mininet script generated automatically.
Topology: Massive_50_hosts_s1
Version: 1.0
Description: A massive network with 50 hosts connected to a single switch (s1), with varying link loss every 10 hosts.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def massive_50_hosts_s1_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 50 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24')
	h2 = net.addHost('h2', ip='10.0.0.2/24')
	h3 = net.addHost('h3', ip='10.0.0.3/24')
	h4 = net.addHost('h4', ip='10.0.0.4/24')
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
	h17 = net.addHost('h17', ip='10.0.0.17/24')
	h18 = net.addHost('h18', ip='10.0.0.18/24')
	h19 = net.addHost('h19', ip='10.0.0.19/24')
	h20 = net.addHost('h20', ip='10.0.0.20/24')
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
	h41 = net.addHost('h41', ip='10.0.0.41/24')
	h42 = net.addHost('h42', ip='10.0.0.42/24')
	h43 = net.addHost('h43', ip='10.0.0.43/24')
	h44 = net.addHost('h44', ip='10.0.0.44/24')
	h45 = net.addHost('h45', ip='10.0.0.45/24')
	h46 = net.addHost('h46', ip='10.0.0.46/24')
	h47 = net.addHost('h47', ip='10.0.0.47/24')
	h48 = net.addHost('h48', ip='10.0.0.48/24')
	h49 = net.addHost('h49', ip='10.0.0.49/24')
	h50 = net.addHost('h50', ip='10.0.0.50/24')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 50 links\n')
	net.addLink(h1, s1, loss=0)
	net.addLink(h2, s1, loss=0)
	net.addLink(h3, s1, loss=0)
	net.addLink(h4, s1, loss=0)
	net.addLink(h5, s1, loss=0)
	net.addLink(h6, s1, loss=0)
	net.addLink(h7, s1, loss=0)
	net.addLink(h8, s1, loss=0)
	net.addLink(h9, s1, loss=0)
	net.addLink(h10, s1, loss=0)
	net.addLink(h11, s1, loss=1)
	net.addLink(h12, s1, loss=1)
	net.addLink(h13, s1, loss=1)
	net.addLink(h14, s1, loss=1)
	net.addLink(h15, s1, loss=1)
	net.addLink(h16, s1, loss=1)
	net.addLink(h17, s1, loss=1)
	net.addLink(h18, s1, loss=1)
	net.addLink(h19, s1, loss=1)
	net.addLink(h20, s1, loss=1)
	net.addLink(h21, s1, loss=2)
	net.addLink(h22, s1, loss=2)
	net.addLink(h23, s1, loss=2)
	net.addLink(h24, s1, loss=2)
	net.addLink(h25, s1, loss=2)
	net.addLink(h26, s1, loss=2)
	net.addLink(h27, s1, loss=2)
	net.addLink(h28, s1, loss=2)
	net.addLink(h29, s1, loss=2)
	net.addLink(h30, s1, loss=2)
	net.addLink(h31, s1, loss=3)
	net.addLink(h32, s1, loss=3)
	net.addLink(h33, s1, loss=3)
	net.addLink(h34, s1, loss=3)
	net.addLink(h35, s1, loss=3)
	net.addLink(h36, s1, loss=3)
	net.addLink(h37, s1, loss=3)
	net.addLink(h38, s1, loss=3)
	net.addLink(h39, s1, loss=3)
	net.addLink(h40, s1, loss=3)
	net.addLink(h41, s1, loss=4)
	net.addLink(h42, s1, loss=4)
	net.addLink(h43, s1, loss=4)
	net.addLink(h44, s1, loss=4)
	net.addLink(h45, s1, loss=4)
	net.addLink(h46, s1, loss=4)
	net.addLink(h47, s1, loss=4)
	net.addLink(h48, s1, loss=4)
	net.addLink(h49, s1, loss=4)
	net.addLink(h50, s1, loss=4)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'massive_50_hosts_s1',
		'version': '1.0',
		'description': 'A massive network with 50 hosts connected to a single switch (s1), with varying link loss every 10 hosts.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': None},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': None},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': None},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': None},
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
			{'id': 'h17', 'ip': '10.0.0.17/24', 'mac': None},
			{'id': 'h18', 'ip': '10.0.0.18/24', 'mac': None},
			{'id': 'h19', 'ip': '10.0.0.19/24', 'mac': None},
			{'id': 'h20', 'ip': '10.0.0.20/24', 'mac': None},
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
			{'id': 'h41', 'ip': '10.0.0.41/24', 'mac': None},
			{'id': 'h42', 'ip': '10.0.0.42/24', 'mac': None},
			{'id': 'h43', 'ip': '10.0.0.43/24', 'mac': None},
			{'id': 'h44', 'ip': '10.0.0.44/24', 'mac': None},
			{'id': 'h45', 'ip': '10.0.0.45/24', 'mac': None},
			{'id': 'h46', 'ip': '10.0.0.46/24', 'mac': None},
			{'id': 'h47', 'ip': '10.0.0.47/24', 'mac': None},
			{'id': 'h48', 'ip': '10.0.0.48/24', 'mac': None},
			{'id': 'h49', 'ip': '10.0.0.49/24', 'mac': None},
			{'id': 'h50', 'ip': '10.0.0.50/24', 'mac': None},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h3', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h4', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h5', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h6', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h7', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h8', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h9', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h10', 's1'], 'PARAMS': {'LOSS': 0}},
			{'ENDPOINTS': ['h11', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h12', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h13', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h14', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h15', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h16', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h17', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h18', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h19', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h20', 's1'], 'PARAMS': {'LOSS': 1}},
			{'ENDPOINTS': ['h21', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h22', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h23', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h24', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h25', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h26', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h27', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h28', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h29', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h30', 's1'], 'PARAMS': {'LOSS': 2}},
			{'ENDPOINTS': ['h31', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h32', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h33', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h34', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h35', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h36', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h37', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h38', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h39', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h40', 's1'], 'PARAMS': {'LOSS': 3}},
			{'ENDPOINTS': ['h41', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h42', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h43', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h44', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h45', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h46', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h47', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h48', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h49', 's1'], 'PARAMS': {'LOSS': 4}},
			{'ENDPOINTS': ['h50', 's1'], 'PARAMS': {'LOSS': 4}},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 15
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
	massive_50_hosts_s1_topology()
