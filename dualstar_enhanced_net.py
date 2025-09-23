"""
Mininet script generated automatically.
Topology: Dualstar_enhanced
Version: 1.1
Description: A dual star topology with two switches and multiple hosts.
"""
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def dualstar_enhanced_topology():

	'Creates and configures the network topology.'
	net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink, waitConnected=True)

	info('*** Adding 1 controllers\n')
	c0 = net.addController('c0')

	info('*** Adding 4 hosts\n')
	h1 = net.addHost('h1', ip='192.168.1.1/24', mac='00:00:00:00:00:11')
	h2 = net.addHost('h2', ip='192.168.1.2/24', mac='00:00:00:00:00:12')
	h3 = net.addHost('h3', ip='192.168.1.3/24', mac='00:00:00:00:00:13')
	h4 = net.addHost('h4', ip='192.168.1.4/24', mac='00:00:00:00:00:14')

	info('*** Adding 2 switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')

	info('*** Creating 5 links\n')
	net.addLink(h1, s1, bw=200, delay='2ms')
	net.addLink(h2, s1, bw=100, delay='3ms', loss=0.5)
	net.addLink(h3, s2, bw=150, delay='4ms')
	net.addLink(h4, s2, bw=120, delay='5ms')
	net.addLink(s1, s2, bw=500, delay='1ms')

	info('*** Starting network\n')
	net.start()

	info('*** Starting monitoring\n')
	info('*** Monitoring configured parameters\n')
	h1_ip = h1.cmd('ip addr show h1-eth0 | grep inet | awk \'{print $2}\' | cut -d/ -f1').strip()
	if h1_ip != '192.168.1.1/24':
	    info(f'Warning: IP mismatch for h1: expected 192.168.1.1/24, got {h1_ip}')
	h1_mac = h1.cmd('ip link show h1-eth0 | grep ether | awk \'{print $2}\'').strip()
	if h1_mac != '00:00:00:00:00:11':
	    info(f'Warning: MAC mismatch for h1: expected 00:00:00:00:00:11, got {h1_mac}')
	h2_ip = h2.cmd('ip addr show h2-eth0 | grep inet | awk \'{print $2}\' | cut -d/ -f1').strip()
	if h2_ip != '192.168.1.2/24':
	    info(f'Warning: IP mismatch for h2: expected 192.168.1.2/24, got {h2_ip}')
	h2_mac = h2.cmd('ip link show h2-eth0 | grep ether | awk \'{print $2}\'').strip()
	if h2_mac != '00:00:00:00:00:12':
	    info(f'Warning: MAC mismatch for h2: expected 00:00:00:00:00:12, got {h2_mac}')
	h3_ip = h3.cmd('ip addr show h3-eth0 | grep inet | awk \'{print $2}\' | cut -d/ -f1').strip()
	if h3_ip != '192.168.1.3/24':
	    info(f'Warning: IP mismatch for h3: expected 192.168.1.3/24, got {h3_ip}')
	h3_mac = h3.cmd('ip link show h3-eth0 | grep ether | awk \'{print $2}\'').strip()
	if h3_mac != '00:00:00:00:00:13':
	    info(f'Warning: MAC mismatch for h3: expected 00:00:00:00:00:13, got {h3_mac}')
	h4_ip = h4.cmd('ip addr show h4-eth0 | grep inet | awk \'{print $2}\' | cut -d/ -f1').strip()
	if h4_ip != '192.168.1.4/24':
	    info(f'Warning: IP mismatch for h4: expected 192.168.1.4/24, got {h4_ip}')
	h4_mac = h4.cmd('ip link show h4-eth0 | grep ether | awk \'{print $2}\'').strip()
	if h4_mac != '00:00:00:00:00:14':
	    info(f'Warning: MAC mismatch for h4: expected 00:00:00:00:00:14, got {h4_mac}')
	links = net.linksBetween(h1, s1)
	if links:
	    link = links[0]
	    if 'bw' in link.intf1.params:
	        actual = link.intf1.params['bw']
	        if actual != 200:
	            info(f'Warning: BANDWIDTH mismatch for link h1-s1: expected 200, got {actual}')
	    if 'delay' in link.intf1.params:
	        actual = link.intf1.params['delay']
	        if actual != '2ms':
	            info(f'Warning: DELAY mismatch for link h1-s1: expected 2ms, got {actual}')
	links = net.linksBetween(h2, s1)
	if links:
	    link = links[0]
	    if 'bw' in link.intf1.params:
	        actual = link.intf1.params['bw']
	        if actual != 100:
	            info(f'Warning: BANDWIDTH mismatch for link h2-s1: expected 100, got {actual}')
	    if 'delay' in link.intf1.params:
	        actual = link.intf1.params['delay']
	        if actual != '3ms':
	            info(f'Warning: DELAY mismatch for link h2-s1: expected 3ms, got {actual}')
	    if 'loss' in link.intf1.params:
	        actual = link.intf1.params['loss']
	        if actual != 0.5:
	            info(f'Warning: LOSS mismatch for link h2-s1: expected 0.5, got {actual}')
	links = net.linksBetween(h3, s2)
	if links:
	    link = links[0]
	    if 'bw' in link.intf1.params:
	        actual = link.intf1.params['bw']
	        if actual != 150:
	            info(f'Warning: BANDWIDTH mismatch for link h3-s2: expected 150, got {actual}')
	    if 'delay' in link.intf1.params:
	        actual = link.intf1.params['delay']
	        if actual != '4ms':
	            info(f'Warning: DELAY mismatch for link h3-s2: expected 4ms, got {actual}')
	links = net.linksBetween(h4, s2)
	if links:
	    link = links[0]
	    if 'bw' in link.intf1.params:
	        actual = link.intf1.params['bw']
	        if actual != 120:
	            info(f'Warning: BANDWIDTH mismatch for link h4-s2: expected 120, got {actual}')
	    if 'delay' in link.intf1.params:
	        actual = link.intf1.params['delay']
	        if actual != '5ms':
	            info(f'Warning: DELAY mismatch for link h4-s2: expected 5ms, got {actual}')
	links = net.linksBetween(s1, s2)
	if links:
	    link = links[0]
	    if 'bw' in link.intf1.params:
	        actual = link.intf1.params['bw']
	        if actual != 500:
	            info(f'Warning: BANDWIDTH mismatch for link s1-s2: expected 500, got {actual}')
	    if 'delay' in link.intf1.params:
	        actual = link.intf1.params['delay']
	        if actual != '1ms':
	            info(f'Warning: DELAY mismatch for link s1-s2: expected 1ms, got {actual}')

	info('*** Running CLI\n')
	CLI(net)

	info('*** Stopping network\n')
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	dualstar_enhanced_topology()
