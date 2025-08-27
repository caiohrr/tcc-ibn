#!/usr/bin/python

from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.node import Controller
import time
import re

def parse_iperf(iperf_output):
    """
    Parses the iperf output string to extract the bandwidth in Mbits/sec.
    """
    # Use a regular expression to find the bandwidth value and unit
    match = re.search(r'(\d+\.?\d*)\s+(Kbits/sec|Mbits/sec|Gbits/sec)', iperf_output)
    if match:
        value = float(match.group(1))
        unit = match.group(2)
        
        # Convert all units to Mbits/sec for consistent comparison
        if unit == 'Kbits/sec':
            return value / 1000
        elif unit == 'Gbits/sec':
            return value * 1000
        else: # Mbits/sec
            return value
    return 0.0

def intent_based_monitoring():
    """
    Main function to set up Mininet and run the intent monitoring loop.
    """
    
    # 1. DEFINE THE INTENT
    # Intent: Bandwidth between h1 and h2 must be higher than 10 Mbits/sec.
    INTENT_BANDWIDTH_THRESHOLD_MBPS = 10.0
    POLLING_INTERVAL_S = 3 # Time to wait between checks

    # Set up the network with a 20 Mbps link initially
    net = Mininet(link=TCLink)
    c0 = net.addController('c0')
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    s1 = net.addSwitch('s1')
    
    # The initial link satisfies the intent
    link = net.addLink(h1, s1, bw=20) 
    net.addLink(s1, h2, bw=20)

    info("*** Starting network\n")
    net.start()

    info(f"*** Intent: Bandwidth between h1 and h2 > {INTENT_BANDWIDTH_THRESHOLD_MBPS} Mbps\n")
    info("*** Starting monitoring loop (Press Ctrl+C to stop)\n")

    # This part simulates network degradation after 10 seconds
    degradation_timer = time.time() + 10

    try:
        while True:
            # 2. MEASURE THE BANDWIDTH
            info(f"--- Checking bandwidth at {time.strftime('%H:%M:%S')} ---\n")
            # The net.iperf command returns a tuple of (client_output, server_output)
            iperf_result_tuple = net.iperf(hosts=(h1, h2), seconds=2)
            
            # 3. PARSE THE RESULT
            measured_bw = parse_iperf(iperf_result_tuple[0])
            
            # 4. VALIDATE AGAINST INTENT
            info(f"Measured Bandwidth: {measured_bw:.2f} Mbps\n")
            
            if measured_bw < INTENT_BANDWIDTH_THRESHOLD_MBPS:
                # 5. TAKE ACTION
                info(f"⚠️  WARNING: INTENT VIOLATED! Bandwidth is {measured_bw:.2f} Mbps, which is below the required {INTENT_BANDWIDTH_THRESHOLD_MBPS} Mbps.\n")
            else:
                info("✅  Intent is satisfied.\n")

            # Simulate network degradation after a delay
            if time.time() > degradation_timer:
                info("*** Simulating network degradation: Reducing link bandwidth to 5 Mbps ***\n")
                link.intf1.config(bw=5) # Degrade the link bandwidth
                degradation_timer = float('inf') # Ensure this only runs once

            time.sleep(POLLING_INTERVAL_S)

    except KeyboardInterrupt:
        info("\n*** Stopping monitoring.\n")
    finally:
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    intent_based_monitoring()
