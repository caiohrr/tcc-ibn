"""
Mininet script generated automatically.
Topology: Large_network_30_hosts
Version: 1.0
Description: Network with 30 hosts. Critical servers (multiples of 5) have high CPU/RAM/Bandwidth. Clients have lower CPU/Bandwidth.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def large_network_30_hosts_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 30 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01', cpu=0.2)
	h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:02', cpu=0.2)
	h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03', cpu=0.2)
	h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04', cpu=0.2)
	h5 = net.addHost('h5', ip='10.0.0.5/24', mac='00:00:00:00:00:05', cpu=1.0, mem='2048M')
	h6 = net.addHost('h6', ip='10.0.0.6/24', mac='00:00:00:00:00:06', cpu=0.2)
	h7 = net.addHost('h7', ip='10.0.0.7/24', mac='00:00:00:00:00:07', cpu=0.2)
	h8 = net.addHost('h8', ip='10.0.0.8/24', mac='00:00:00:00:00:08', cpu=0.2)
	h9 = net.addHost('h9', ip='10.0.0.9/24', mac='00:00:00:00:00:09', cpu=0.2)
	h10 = net.addHost('h10', ip='10.0.0.10/24', mac='00:00:00:00:00:0a', cpu=1.0, mem='2048M')
	h11 = net.addHost('h11', ip='10.0.0.11/24', mac='00:00:00:00:00:0b', cpu=0.2)
	h12 = net.addHost('h12', ip='10.0.0.12/24', mac='00:00:00:00:00:0c', cpu=0.2)
	h13 = net.addHost('h13', ip='10.0.0.13/24', mac='00:00:00:00:00:0d', cpu=0.2)
	h14 = net.addHost('h14', ip='10.0.0.14/24', mac='00:00:00:00:00:0e', cpu=0.2)
	h15 = net.addHost('h15', ip='10.0.0.15/24', mac='00:00:00:00:00:0f', cpu=1.0, mem='2048M')
	h16 = net.addHost('h16', ip='10.0.0.16/24', mac='00:00:00:00:00:10', cpu=0.2)
	h17 = net.addHost('h17', ip='10.0.0.17/24', mac='00:00:00:00:00:11', cpu=0.2)
	h18 = net.addHost('h18', ip='10.0.0.18/24', mac='00:00:00:00:00:12', cpu=0.2)
	h19 = net.addHost('h19', ip='10.0.0.19/24', mac='00:00:00:00:00:13', cpu=0.2)
	h20 = net.addHost('h20', ip='10.0.0.20/24', mac='00:00:00:00:00:14', cpu=1.0, mem='2048M')
	h21 = net.addHost('h21', ip='10.0.0.21/24', mac='00:00:00:00:00:15', cpu=0.2)
	h22 = net.addHost('h22', ip='10.0.0.22/24', mac='00:00:00:00:00:16', cpu=0.2)
	h23 = net.addHost('h23', ip='10.0.0.23/24', mac='00:00:00:00:00:17', cpu=0.2)
	h24 = net.addHost('h24', ip='10.0.0.24/24', mac='00:00:00:00:00:18', cpu=0.2)
	h25 = net.addHost('h25', ip='10.0.0.25/24', mac='00:00:00:00:00:19', cpu=1.0, mem='2048M')
	h26 = net.addHost('h26', ip='10.0.0.26/24', mac='00:00:00:00:00:1a', cpu=0.2)
	h27 = net.addHost('h27', ip='10.0.0.27/24', mac='00:00:00:00:00:1b', cpu=0.2)
	h28 = net.addHost('h28', ip='10.0.0.28/24', mac='00:00:00:00:00:1c', cpu=0.2)
	h29 = net.addHost('h29', ip='10.0.0.29/24', mac='00:00:00:00:00:1d', cpu=0.2)
	h30 = net.addHost('h30', ip='10.0.0.30/24', mac='00:00:00:00:00:1e', cpu=1.0, mem='2048M')

	info('*** Adding 1 switches\n')
	s1 = net.addSwitch('s1')

	info('*** Creating 30 links\n')
	net.addLink(h1, s1, bw=10)
	net.addLink(h2, s1, bw=10)
	net.addLink(h3, s1, bw=10)
	net.addLink(h4, s1, bw=10)
	net.addLink(h5, s1, bw=1000)
	net.addLink(h6, s1, bw=10)
	net.addLink(h7, s1, bw=10)
	net.addLink(h8, s1, bw=10)
	net.addLink(h9, s1, bw=10)
	net.addLink(h10, s1, bw=1000)
	net.addLink(h11, s1, bw=10)
	net.addLink(h12, s1, bw=10)
	net.addLink(h13, s1, bw=10)
	net.addLink(h14, s1, bw=10)
	net.addLink(h15, s1, bw=1000)
	net.addLink(h16, s1, bw=10)
	net.addLink(h17, s1, bw=10)
	net.addLink(h18, s1, bw=10)
	net.addLink(h19, s1, bw=10)
	net.addLink(h20, s1, bw=1000)
	net.addLink(h21, s1, bw=10)
	net.addLink(h22, s1, bw=10)
	net.addLink(h23, s1, bw=10)
	net.addLink(h24, s1, bw=10)
	net.addLink(h25, s1, bw=1000)
	net.addLink(h26, s1, bw=10)
	net.addLink(h27, s1, bw=10)
	net.addLink(h28, s1, bw=10)
	net.addLink(h29, s1, bw=10)
	net.addLink(h30, s1, bw=1000)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': 'large_network_30_hosts',
		'version': '1.0',
		'description': 'Network with 30 hosts. Critical servers (multiples of 5) have high CPU/RAM/Bandwidth. Clients have lower CPU/Bandwidth.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': '00:00:00:00:00:01', 'max_cpu': 0.2},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': '00:00:00:00:00:02', 'max_cpu': 0.2},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': '00:00:00:00:00:03', 'max_cpu': 0.2},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': '00:00:00:00:00:04', 'max_cpu': 0.2},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': '00:00:00:00:00:05', 'max_cpu': 1.0, 'max_ram': 2048},
			{'id': 'h6', 'ip': '10.0.0.6/24', 'mac': '00:00:00:00:00:06', 'max_cpu': 0.2},
			{'id': 'h7', 'ip': '10.0.0.7/24', 'mac': '00:00:00:00:00:07', 'max_cpu': 0.2},
			{'id': 'h8', 'ip': '10.0.0.8/24', 'mac': '00:00:00:00:00:08', 'max_cpu': 0.2},
			{'id': 'h9', 'ip': '10.0.0.9/24', 'mac': '00:00:00:00:00:09', 'max_cpu': 0.2},
			{'id': 'h10', 'ip': '10.0.0.10/24', 'mac': '00:00:00:00:00:0a', 'max_cpu': 1.0, 'max_ram': 2048},
			{'id': 'h11', 'ip': '10.0.0.11/24', 'mac': '00:00:00:00:00:0b', 'max_cpu': 0.2},
			{'id': 'h12', 'ip': '10.0.0.12/24', 'mac': '00:00:00:00:00:0c', 'max_cpu': 0.2},
			{'id': 'h13', 'ip': '10.0.0.13/24', 'mac': '00:00:00:00:00:0d', 'max_cpu': 0.2},
			{'id': 'h14', 'ip': '10.0.0.14/24', 'mac': '00:00:00:00:00:0e', 'max_cpu': 0.2},
			{'id': 'h15', 'ip': '10.0.0.15/24', 'mac': '00:00:00:00:00:0f', 'max_cpu': 1.0, 'max_ram': 2048},
			{'id': 'h16', 'ip': '10.0.0.16/24', 'mac': '00:00:00:00:00:10', 'max_cpu': 0.2},
			{'id': 'h17', 'ip': '10.0.0.17/24', 'mac': '00:00:00:00:00:11', 'max_cpu': 0.2},
			{'id': 'h18', 'ip': '10.0.0.18/24', 'mac': '00:00:00:00:00:12', 'max_cpu': 0.2},
			{'id': 'h19', 'ip': '10.0.0.19/24', 'mac': '00:00:00:00:00:13', 'max_cpu': 0.2},
			{'id': 'h20', 'ip': '10.0.0.20/24', 'mac': '00:00:00:00:00:14', 'max_cpu': 1.0, 'max_ram': 2048},
			{'id': 'h21', 'ip': '10.0.0.21/24', 'mac': '00:00:00:00:00:15', 'max_cpu': 0.2},
			{'id': 'h22', 'ip': '10.0.0.22/24', 'mac': '00:00:00:00:00:16', 'max_cpu': 0.2},
			{'id': 'h23', 'ip': '10.0.0.23/24', 'mac': '00:00:00:00:00:17', 'max_cpu': 0.2},
			{'id': 'h24', 'ip': '10.0.0.24/24', 'mac': '00:00:00:00:00:18', 'max_cpu': 0.2},
			{'id': 'h25', 'ip': '10.0.0.25/24', 'mac': '00:00:00:00:00:19', 'max_cpu': 1.0, 'max_ram': 2048},
			{'id': 'h26', 'ip': '10.0.0.26/24', 'mac': '00:00:00:00:00:1a', 'max_cpu': 0.2},
			{'id': 'h27', 'ip': '10.0.0.27/24', 'mac': '00:00:00:00:00:1b', 'max_cpu': 0.2},
			{'id': 'h28', 'ip': '10.0.0.28/24', 'mac': '00:00:00:00:00:1c', 'max_cpu': 0.2},
			{'id': 'h29', 'ip': '10.0.0.29/24', 'mac': '00:00:00:00:00:1d', 'max_cpu': 0.2},
			{'id': 'h30', 'ip': '10.0.0.30/24', 'mac': '00:00:00:00:00:1e', 'max_cpu': 1.0, 'max_ram': 2048},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch', 'PARAMS': {'PROTOCOLS': 'OpenFlow13'}},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['h1', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h2', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h3', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h4', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h5', 's1'], 'PARAMS': {'BANDWIDTH': 1000}},
			{'ENDPOINTS': ['h6', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h7', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h8', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h9', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h10', 's1'], 'PARAMS': {'BANDWIDTH': 1000}},
			{'ENDPOINTS': ['h11', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h12', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h13', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h14', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h15', 's1'], 'PARAMS': {'BANDWIDTH': 1000}},
			{'ENDPOINTS': ['h16', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h17', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h18', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h19', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h20', 's1'], 'PARAMS': {'BANDWIDTH': 1000}},
			{'ENDPOINTS': ['h21', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h22', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h23', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h24', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h25', 's1'], 'PARAMS': {'BANDWIDTH': 1000}},
			{'ENDPOINTS': ['h26', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h27', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h28', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h29', 's1'], 'PARAMS': {'BANDWIDTH': 10}},
			{'ENDPOINTS': ['h30', 's1'], 'PARAMS': {'BANDWIDTH': 1000}},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 15
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
	large_network_30_hosts_topology()
