"""
Mininet script generated automatically.
Topology: 32_hosts_2_switches_mac_rules
Version: 1.0
Description: Topology with 32 hosts divided between two switches. Hosts on s1 have even MACs, hosts on s2 have odd MACs. Monitoring enabled.
Intent Monitoring: Enabled
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import json
from intent_monitor import IntentMonitor

def 32_hosts_2_switches_mac_rules_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=None, switch=OVSKernelSwitch, link=TCLink, waitConnected=False)

	info('*** No controller defined. OVS will be configured for standalone mode.\n')

	info('*** Adding 32 hosts\n')
	h1 = net.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:02')
	h2 = net.addHost('h2', ip='10.0.0.2/24', mac='00:00:00:00:00:04')
	h3 = net.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:06')
	h4 = net.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:08')
	h5 = net.addHost('h5', ip='10.0.0.5/24', mac='00:00:00:00:00:0A')
	h6 = net.addHost('h6', ip='10.0.0.6/24', mac='00:00:00:00:00:0C')
	h7 = net.addHost('h7', ip='10.0.0.7/24', mac='00:00:00:00:00:0E')
	h8 = net.addHost('h8', ip='10.0.0.8/24', mac='00:00:00:00:00:10')
	h9 = net.addHost('h9', ip='10.0.0.9/24', mac='00:00:00:00:00:12')
	h10 = net.addHost('h10', ip='10.0.0.10/24', mac='00:00:00:00:00:14')
	h11 = net.addHost('h11', ip='10.0.0.11/24', mac='00:00:00:00:00:16')
	h12 = net.addHost('h12', ip='10.0.0.12/24', mac='00:00:00:00:00:18')
	h13 = net.addHost('h13', ip='10.0.0.13/24', mac='00:00:00:00:00:1A')
	h14 = net.addHost('h14', ip='10.0.0.14/24', mac='00:00:00:00:00:1C')
	h15 = net.addHost('h15', ip='10.0.0.15/24', mac='00:00:00:00:00:1E')
	h16 = net.addHost('h16', ip='10.0.0.16/24', mac='00:00:00:00:00:20')
	h17 = net.addHost('h17', ip='10.0.0.17/24', mac='00:00:00:00:00:01')
	h18 = net.addHost('h18', ip='10.0.0.18/24', mac='00:00:00:00:00:03')
	h19 = net.addHost('h19', ip='10.0.0.19/24', mac='00:00:00:00:00:05')
	h20 = net.addHost('h20', ip='10.0.0.20/24', mac='00:00:00:00:00:07')
	h21 = net.addHost('h21', ip='10.0.0.21/24', mac='00:00:00:00:00:09')
	h22 = net.addHost('h22', ip='10.0.0.22/24', mac='00:00:00:00:00:0B')
	h23 = net.addHost('h23', ip='10.0.0.23/24', mac='00:00:00:00:00:0D')
	h24 = net.addHost('h24', ip='10.0.0.24/24', mac='00:00:00:00:00:0F')
	h25 = net.addHost('h25', ip='10.0.0.25/24', mac='00:00:00:00:00:11')
	h26 = net.addHost('h26', ip='10.0.0.26/24', mac='00:00:00:00:00:13')
	h27 = net.addHost('h27', ip='10.0.0.27/24', mac='00:00:00:00:00:15')
	h28 = net.addHost('h28', ip='10.0.0.28/24', mac='00:00:00:00:00:17')
	h29 = net.addHost('h29', ip='10.0.0.29/24', mac='00:00:00:00:00:19')
	h30 = net.addHost('h30', ip='10.0.0.30/24', mac='00:00:00:00:00:1B')
	h31 = net.addHost('h31', ip='10.0.0.31/24', mac='00:00:00:00:00:1D')
	h32 = net.addHost('h32', ip='10.0.0.32/24', mac='00:00:00:00:00:1F')

	info('*** Adding 2 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')

	info('*** Creating 33 links\n')
	net.addLink(s1, s2)
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
	net.addLink(h17, s2)
	net.addLink(h18, s2)
	net.addLink(h19, s2)
	net.addLink(h20, s2)
	net.addLink(h21, s2)
	net.addLink(h22, s2)
	net.addLink(h23, s2)
	net.addLink(h24, s2)
	net.addLink(h25, s2)
	net.addLink(h26, s2)
	net.addLink(h27, s2)
	net.addLink(h28, s2)
	net.addLink(h29, s2)
	net.addLink(h30, s2)
	net.addLink(h31, s2)
	net.addLink(h32, s2)

	info('*** Starting network\n')
	net.start()

	info('*** Configuring switches for standalone mode\n')
	net.get('s1').cmd('ovs-ofctl add-flow s1 "priority=0,actions=normal"')
	net.get('s2').cmd('ovs-ofctl add-flow s2 "priority=0,actions=normal"')

	# Setup intent monitoring
	info('*** Setting up intent monitoring\n')
	topology_data = {
		'id': '32_hosts_2_switches_mac_rules',
		'version': '1.0',
		'description': 'Topology with 32 hosts divided between two switches. Hosts on s1 have even MACs, hosts on s2 have odd MACs. Monitoring enabled.',
		'hosts': [
			{'id': 'h1', 'ip': '10.0.0.1/24', 'mac': '00:00:00:00:00:02'},
			{'id': 'h2', 'ip': '10.0.0.2/24', 'mac': '00:00:00:00:00:04'},
			{'id': 'h3', 'ip': '10.0.0.3/24', 'mac': '00:00:00:00:00:06'},
			{'id': 'h4', 'ip': '10.0.0.4/24', 'mac': '00:00:00:00:00:08'},
			{'id': 'h5', 'ip': '10.0.0.5/24', 'mac': '00:00:00:00:00:0A'},
			{'id': 'h6', 'ip': '10.0.0.6/24', 'mac': '00:00:00:00:00:0C'},
			{'id': 'h7', 'ip': '10.0.0.7/24', 'mac': '00:00:00:00:00:0E'},
			{'id': 'h8', 'ip': '10.0.0.8/24', 'mac': '00:00:00:00:00:10'},
			{'id': 'h9', 'ip': '10.0.0.9/24', 'mac': '00:00:00:00:00:12'},
			{'id': 'h10', 'ip': '10.0.0.10/24', 'mac': '00:00:00:00:00:14'},
			{'id': 'h11', 'ip': '10.0.0.11/24', 'mac': '00:00:00:00:00:16'},
			{'id': 'h12', 'ip': '10.0.0.12/24', 'mac': '00:00:00:00:00:18'},
			{'id': 'h13', 'ip': '10.0.0.13/24', 'mac': '00:00:00:00:00:1A'},
			{'id': 'h14', 'ip': '10.0.0.14/24', 'mac': '00:00:00:00:00:1C'},
			{'id': 'h15', 'ip': '10.0.0.15/24', 'mac': '00:00:00:00:00:1E'},
			{'id': 'h16', 'ip': '10.0.0.16/24', 'mac': '00:00:00:00:00:20'},
			{'id': 'h17', 'ip': '10.0.0.17/24', 'mac': '00:00:00:00:00:01'},
			{'id': 'h18', 'ip': '10.0.0.18/24', 'mac': '00:00:00:00:00:03'},
			{'id': 'h19', 'ip': '10.0.0.19/24', 'mac': '00:00:00:00:00:05'},
			{'id': 'h20', 'ip': '10.0.0.20/24', 'mac': '00:00:00:00:00:07'},
			{'id': 'h21', 'ip': '10.0.0.21/24', 'mac': '00:00:00:00:00:09'},
			{'id': 'h22', 'ip': '10.0.0.22/24', 'mac': '00:00:00:00:00:0B'},
			{'id': 'h23', 'ip': '10.0.0.23/24', 'mac': '00:00:00:00:00:0D'},
			{'id': 'h24', 'ip': '10.0.0.24/24', 'mac': '00:00:00:00:00:0F'},
			{'id': 'h25', 'ip': '10.0.0.25/24', 'mac': '00:00:00:00:00:11'},
			{'id': 'h26', 'ip': '10.0.0.26/24', 'mac': '00:00:00:00:00:13'},
			{'id': 'h27', 'ip': '10.0.0.27/24', 'mac': '00:00:00:00:00:15'},
			{'id': 'h28', 'ip': '10.0.0.28/24', 'mac': '00:00:00:00:00:17'},
			{'id': 'h29', 'ip': '10.0.0.29/24', 'mac': '00:00:00:00:00:19'},
			{'id': 'h30', 'ip': '10.0.0.30/24', 'mac': '00:00:00:00:00:1B'},
			{'id': 'h31', 'ip': '10.0.0.31/24', 'mac': '00:00:00:00:00:1D'},
			{'id': 'h32', 'ip': '10.0.0.32/24', 'mac': '00:00:00:00:00:1F'},
		],
		'switches': [
			{'ID': 's1', 'TYPE': 'OVSSwitch'},
			{'ID': 's2', 'TYPE': 'OVSSwitch'},
		],
		'controllers': [
		],
		'connections': [
			{'ENDPOINTS': ['s1', 's2']},
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
			{'ENDPOINTS': ['h17', 's2']},
			{'ENDPOINTS': ['h18', 's2']},
			{'ENDPOINTS': ['h19', 's2']},
			{'ENDPOINTS': ['h20', 's2']},
			{'ENDPOINTS': ['h21', 's2']},
			{'ENDPOINTS': ['h22', 's2']},
			{'ENDPOINTS': ['h23', 's2']},
			{'ENDPOINTS': ['h24', 's2']},
			{'ENDPOINTS': ['h25', 's2']},
			{'ENDPOINTS': ['h26', 's2']},
			{'ENDPOINTS': ['h27', 's2']},
			{'ENDPOINTS': ['h28', 's2']},
			{'ENDPOINTS': ['h29', 's2']},
			{'ENDPOINTS': ['h30', 's2']},
			{'ENDPOINTS': ['h31', 's2']},
			{'ENDPOINTS': ['h32', 's2']},
		]
	}

	class TopologyWrapper:
		def __init__(self, data):
			self.__dict__.update(data)

	topology_wrapper = TopologyWrapper(topology_data)
	monitor = IntentMonitor(topology_wrapper, net)
	monitor.monitor_interval = 10
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
	32_hosts_2_switches_mac_rules_topology()
