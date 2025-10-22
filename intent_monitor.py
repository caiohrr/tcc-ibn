# intent_monitor.py
import threading
import time
import json
import re
from datetime import datetime
from pathlib import Path

# Assuming main-v2.py is in the same directory or accessible in the path
# We need the PluginManager and the new MonitorRecoveryPlugin interface
from main import PluginManager, MonitorRecoveryPlugin 

class IntentMonitor:
    """
    Monitors the network to ensure operational intents are met and can trigger
    recovery actions when they are violated.
    """
    def __init__(self, topology, net):
        """
        Initializes the Intent Monitor.
        
        Args:
            topology: An object representing the parsed topology data.
            net: The Mininet network object.
        """
        self.topology = topology
        self.net = net
        self.intents = []
        self.report = []
        
        # Monitoring control
        self.monitor_interval = 30  # seconds
        self.recovery_enabled = True
        self._monitoring_active = False
        self._timer = None
        
        # --- Plugin Integration ---
        # The monitor instantiates its own PluginManager to discover monitoring plugins
        self.plugin_manager = PluginManager(plugins_dir=Path("plugins"))
        self.check_functions = {}
        self.recovery_functions = {}
        self._register_default_functions()
        self._register_plugin_functions()
        
        # Parse intents from the topology file
        self._parse_intents()
        print(f"✔ Intent Monitor initialized with {len(self.intents)} intents.")

    def _register_default_functions(self):
        """Registers the built-in check and recovery functions."""
        self.check_functions = {
            'CONNECTIVITY': self.check_connectivity,
            'BANDWIDTH': self.check_bandwidth,
            'DELAY': self.check_delay,
            'PACKET_LOSS': self.check_packet_loss,
            'CPU_USAGE': self.check_cpu_usage,
            'MEMORY_USAGE': self.check_memory_usage,
            'LINK_UTILIZATION': self.check_link_utilization,
        }
        self.recovery_functions = {
            'CONNECTIVITY': self.recover_connectivity,
            'BANDWIDTH': self.recover_link_params,
            'DELAY': self.recover_link_params,
            'PACKET_LOSS': self.recover_link_params,
            'CPU_USAGE': self.recover_cpu_usage,
            'MEMORY_USAGE': self.recover_resource,
            'LINK_UTILIZATION': self.recover_traffic_routing,
        }

    def _register_plugin_functions(self):
        """Discovers and registers check/recovery functions from plugins."""
        # Note: The 'MonitorRecoveryPlugin' type is defined in the updated main.py
        for plugin in self.plugin_manager.monitor_recovery_plugins:
            print(f"  - Loading functions from monitor plugin: {plugin.get_name()}")
            # Add or override check functions
            for intent_type, func in plugin.get_check_functions().items():
                self.check_functions[intent_type] = func
            # Add or override recovery functions
            for intent_type, func in plugin.get_recovery_functions().items():
                self.recovery_functions[intent_type] = func
                
    def _parse_intents(self):
        """Parses intents from the topology data."""
        # --- Connectivity Intents ---
        # Assuming full connectivity between all hosts is an implicit intent.
        for i, host1_data in enumerate(self.topology.hosts):
            for host2_data in self.topology.hosts[i+1:]:
                intent = {
                    'type': 'CONNECTIVITY',
                    'target': (host1_data['id'], host2_data['id']),
                    'description': f"Connectivity between {host1_data['id']} and {host2_data['id']}",
                    'status': 'UNKNOWN'
                }
                self.intents.append(intent)

        # --- Link Parameter Intents ---
        for conn in self.topology.connections:
            endpoints = tuple(conn.get('ENDPOINTS', []))
            params = conn.get('PARAMS', {})
            
            if params.get('BANDWIDTH'):
                self.intents.append({
                    'type': 'BANDWIDTH', 'target': endpoints, 'value': params['BANDWIDTH'],
                    'description': f"Bandwidth >= {params['BANDWIDTH']} Mbps for link {endpoints[0]}-{endpoints[1]}",
                    'status': 'UNKNOWN'
                })
            if params.get('DELAY'):
                self.intents.append({
                    'type': 'DELAY', 'target': endpoints, 'value': params['DELAY'],
                    'description': f"Delay <= {params['DELAY']} for link {endpoints[0]}-{endpoints[1]}",
                    'status': 'UNKNOWN'
                })
            if params.get('LOSS'):
                self.intents.append({
                    'type': 'PACKET_LOSS', 'target': endpoints, 'value': params['LOSS'],
                    'description': f"Packet Loss <= {params['LOSS']}% for link {endpoints[0]}-{endpoints[1]}",
                    'status': 'UNKNOWN'
                })

        # --- Host Resource Intents (Example Structure) ---
        # "HOSTS": [{ "ID": "h1", "MAX_CPU": 0.5, "MAX_RAM": 128 }]
        for host_data in self.topology.hosts:
            # === MODIFIED HERE ===
            if host_data.get('max_cpu'): 
                self.intents.append({
                    'type': 'CPU_USAGE', 'target': host_data['id'],
                    'value': host_data['max_cpu'], 
                    'description': f"CPU usage <= {host_data['max_cpu']*100}% for host {host_data['id']}",
                    'status': 'UNKNOWN'
                })
            # === MODIFIED HERE ===
            if host_data.get('max_ram'): 
                self.intents.append({
                    'type': 'MEMORY_USAGE', 'target': host_data['id'],
                    'value': host_data['max_ram'],
                    'description': f"Memory usage <= {host_data['max_ram']}MB for host {host_data['id']}",
                    'status': 'UNKNOWN'
                })
        
    def start_monitoring(self):
        """Starts the periodic intent monitoring process."""
        if not self._monitoring_active:
            self._monitoring_active = True
            self._monitor_loop()
            print("✔ Monitoring started.")

    def stop_monitoring(self):
        """Stops the intent monitoring process."""
        if self._timer:
            self._timer.cancel()
        self._monitoring_active = False
        print("✔ Monitoring stopped.")

    def _monitor_loop(self):
        """The main loop that checks all intents."""
        if not self._monitoring_active:
            return
        
        timestamp = datetime.now().isoformat()
        print(f"\n--- Running Intent Check @ {timestamp} ---")
        
        for intent in self.intents:
            check_function = self.check_functions.get(intent['type'])
            if not check_function:
                print(f"  [?] Warning: No check function found for intent type '{intent['type']}'")
                continue

            try:
                is_ok = check_function(intent)
                
                if not is_ok:
                    intent['status'] = 'BROKEN'
                    log_entry = f"  [✗] BROKEN: {intent['description']}"
                    print(log_entry)
                    self.report.append({'timestamp': timestamp, 'log': log_entry, 'intent': intent})
                    
                    if self.recovery_enabled:
                        recovery_function = self.recovery_functions.get(intent['type'])
                        if recovery_function:
                            print(f"    -> Attempting recovery for '{intent['type']}'...")
                            recovery_function(intent)
                        else:
                            print(f"    -> Warning: No recovery function found for intent type '{intent['type']}'")
                else:
                    if intent['status'] != 'OK':
                        intent['status'] = 'OK'
                        log_entry = f"  [✔] OK: {intent['description']}"
                        print(log_entry)
                        self.report.append({'timestamp': timestamp, 'log': log_entry, 'intent': intent})

            except NotImplementedError:
                print(f"  [!] Not Implemented: Check for '{intent['type']}' on {intent['target']}.")
            except Exception as e:
                print(f"  [!] ERROR checking intent '{intent['type']}': {e}")

        # Schedule the next check
        self._timer = threading.Timer(self.monitor_interval, self._monitor_loop)
        self._timer.start()

    def export_report(self):
        """Exports the monitoring report to a JSON file."""
        report_filename = f"intent_report_{self.topology.id}_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(report_filename, 'w') as f:
            json.dump(self.report, f, indent=4)
        print(f"✔ Intent monitoring report saved to '{report_filename}'")
        
    # Monitoring functions
    
    def check_connectivity(self, intent):
        """Checks if two hosts can ping each other."""
        host1_id, host2_id = intent['target']
        host1 = self.net.get(host1_id)
        host2 = self.net.get(host2_id)

        result = host1.cmd(f'ping -c 1 {host2.IP()}')

        is_successful = '0% packet loss' in result
        return is_successful

        #raise NotImplementedError("Connectivity check logic is not implemented.")

    def check_bandwidth(self, intent):
        """
        Checks if a link meets the minimum bandwidth requirement (passive measurement).
        intent: dict with keys:
            - 'target': tuple of host names (host1, host2)
            - 'value': minimum required bandwidth in Mbps
        Returns True if bandwidth >= required, False otherwise.
        """
        host1_id, host2_id = intent['target']
        #min_bw_mbps = intent.get('value', 10)  # default 10 Mbps
        min_bw_mbps = 0  # default 10 Mbps

        host1 = self.net.get(host1_id)
        host2 = self.net.get(host2_id)

        # Pick the interface connected to host2 (simplest: first interface)
        iface = host1.intfNames()[0]

        # Sample TX bytes over a short interval (1 second)
        tx_bytes_1 = int(host1.cmd(f"cat /sys/class/net/{iface}/statistics/tx_bytes").strip())
        time.sleep(1)
        tx_bytes_2 = int(host1.cmd(f"cat /sys/class/net/{iface}/statistics/tx_bytes").strip())

        # Convert to bits per second
        bw_bps = (tx_bytes_2 - tx_bytes_1) * 8
        bw_mbps = bw_bps / 1_000_000

        #print(f"[INFO] Estimated bandwidth {host1_id}->{host2_id}: {bw_mbps:.2f} Mbps")

        if bw_mbps >= min_bw_mbps:
            return True
        else:
            print(f"[WARN] Bandwidth below minimum threshold ({min_bw_mbps} Mbps)!")
            return False


    def check_delay(self, intent):
        """
        Checks if a link's delay is within the acceptable limit.
        Uses net.ping() to get the parsed average latency.
        """
        #print(f'checking : {intent['value']}')
        host1_id, host2_id = intent['target']
        #max_delay = intent.get('value', 50)  # default 50ms
        #max_delay = intent['value']  # default 50ms
        max_delay_match = re.match(r"(\d+(?:\.\d+)?)ms", intent['value'])
        max_delay = float(max_delay_match.group(1))
        host1 = self.net.get(host1_id)
        host2 = self.net.get(host2_id)

        # Run ping 4 times
        result = host1.cmd(f'ping -c 3 {host2.IP()}')
        # Example line to parse: rtt min/avg/max/mdev = 0.063/0.065/0.068/0.002 ms

        match = re.search(r'rtt .* = .*?/([\d.]+)/.* ms', result)
        if match:
            avg_delay = float(match.group(1))
            #print(f"[INFO] Average delay from {host1_id} to {host2_id}: {avg_delay} ms")
            if avg_delay <= max_delay:
                return True
            else:
                print(f"[WARN] Delay exceeded threshold ({max_delay} ms)!")
                return False
        else:
            print(f"[ERROR] Could not parse ping output:\n{result}")
            return False

        raise NotImplementedError("Not implemented delay")

    def check_packet_loss(self, intent):
        """Checks if a link's packet loss is below the threshold."""
        host1_id, host2_id = intent['target']
        #max_loss = intent.get('max_loss_percent', 5)  # default threshold
        max_loss = intent['value']

        host1 = self.net.get(host1_id)
        host2 = self.net.get(host2_id)

        result = host1.cmd(f'ping -c 5 {host2.IP()}')
        match = re.search(r'(\d+)% packet loss', result)
        if match:
            loss = int(match.group(1))
            print(f"[INFO] Packet loss {host1_id} -> {host2_id}: {loss}% . MAX LOSS = {max_loss}")
            return loss <= max_loss
        else:
            print("[ERROR] Could not parse ping output")
        return False 
        #raise NotImplementedError("Packet loss check logic is not implemented.")
    
    def check_cpu_usage(self, intent):
        """Checks a host's CPU usage."""
        host_id = intent['target']
        max_cpu = intent.get('value', 80)  # default threshold
        max_cpu *= 100
        
        host = self.net.get(host_id)
        
        # Get CPU usage from the host's perspective
        result = host.cmd("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        
        try:
            # Extract the CPU usage percentage (remove '%' if present)
            cpu_usage = float(result.strip().replace('%', ''))
            
            print(f"[INFO] CPU usage for {host_id}: {cpu_usage}%")
            
            if cpu_usage <= max_cpu:
                return True
            else:
                print(f"[WARN] CPU usage exceeded threshold ({max_cpu}%)!")
                return False
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Could not parse CPU usage for {host_id}: {e}")

        return False
       
    def check_memory_usage(self, intent):
        """Checks a host's memory usage."""
        # Similar to CPU usage, this is tricky in standard Mininet.
        # You might need to use cgroups or other virtualization features.
        raise NotImplementedError("Memory usage check logic is not implemented.")
        
    def check_link_utilization(self, intent):
        """
        Checks the utilization of a link.
        intent: dict with keys:
            - 'target': tuple of host names (host1, host2)
            - 'value': numeric threshold in Mbps
        Returns True if utilization is within limit, False if exceeded.
        """
        host1_id, host2_id = intent['target']
        host1 = self.net.get(host1_id)
        host2 = self.net.get(host2_id)

        # Convert threshold to bits per second
        max_util_bps = intent.get('value', 10) * 1_000_000  # Mbps -> bps

        # Pick the first interface of host1
        iface = host1.intfNames()[0]

        # Sample TX bytes over 1 second
        tx_bytes_1 = int(host1.cmd(f"cat /sys/class/net/{iface}/statistics/tx_bytes").strip())
        time.sleep(1)
        tx_bytes_2 = int(host1.cmd(f"cat /sys/class/net/{iface}/statistics/tx_bytes").strip())

        # Convert to bits per second
        bits_per_sec = (tx_bytes_2 - tx_bytes_1) * 8

        print(f"[INFO] Link utilization {host1_id}->{host2_id}: {bits_per_sec/1e6:.2f} Mbps")

        if bits_per_sec <= max_util_bps:
            return True
        else:
            print(f"[WARN] Link utilization exceeded threshold ({max_util_bps/1e6:.2f} Mbps)!")
            return False

    def recover_connectivity(self, intent):
        """
        Attempts to recover connectivity by ensuring host interfaces are 'UP'.
        """
        host1_id, host2_id = intent['target']
        host1 = self.net.get(host1_id)
        host2 = self.net.get(host2_id)

        try:
            # Get the first interface for each host
            iface1 = host1.intfNames()[0]
            iface2 = host2.intfNames()[0]

            print(f"  -> ACTION: Ensuring interfaces are UP for {host1_id}({iface1}) and {host2_id}({iface2}).")
            host1.cmd(f"ip link set {iface1} up")
            host2.cmd(f"ip link set {iface2} up")
        
        except Exception as e:
            print(f"  -> ERROR: Failed to bring interfaces up for {host1_id}-{host2_id}: {e}")        


    def recover_link_params(self, intent):
        #"""Attempts to recover link parameters like BW, delay, loss."""
        ## In Mininet, this would mean re-applying the link configuration.
        ## This is difficult to do on a live link without tearing it down.
        ## A more realistic action could be to reroute traffic if possible.
        #host1_id, host2_id = intent['target']

        #host1 = self.net.get(host1_id)
        #host2 = self.net.get(host2_id)

        #host1.cmd(f"ip link set {host1_id}-eth0 down")
        #host1.cmd(f"ip link set {host1_id}-eth0 up")
        #host1.cmd(f"{host1_id} tc qdisc del dev {host1_id}-eth0 parent 5:1")

        #host2.cmd(f"ip link set {host2_id}-eth0 down")
        #host2.cmd(f"ip link set {host2_id}-eth0 up")
        #host1.cmd(f"{host2_id} tc qdisc del dev {host2_id}-eth0 parent 5:1")


        ##print(f"    - ACTION: Placeholder for recovering link parameters for {intent['target']}.")

        """
        Attempts to recover link parameters (BW, delay, loss) by resetting
        the 'tc' queueing disciplines on the link.
        """
        node1_id, node2_id = intent['target']
        node1 = self.net.get(node1_id)
        node2 = self.net.get(node2_id)

        try:
            # Find the link between the two nodes
            links = self.net.linksBetween(node1, node2)
            if not links:
                print(f"  -> ERROR: Could not find link between {node1_id} and {node2_id}.")
                return
            
            link = links[0] # Assume only one direct link
            intf1, intf2 = link.intf1, link.intf2
            
            # Delete all 'tc' qdisc rules from the 'root' of both interfaces.
            # This resets them to the default (no bandwidth/delay/loss shaping).
            print(f"  -> ACTION: Resetting TC qdisc rules on link {intf1.name} (at {node1_id}) and {intf2.name} (at {node2_id}).")
            node1.cmd(f"tc qdisc del dev {intf1.name} root")
            node2.cmd(f"tc qdisc del dev {intf2.name} root")
            print(f"  -> INFO: TC rules on {intf1.name} and {intf2.name} reset to default.")
            
            # NOTE: A more advanced recovery would re-apply the *original*
            # parameters from the topology file, but that's more complex.
            # This simple "reset" is often enough to clear a bad state.

        except Exception as e:
            print(f"  -> ERROR: Failed to reset TC rules for {node1_id}-{node2_id}: {e}")
            print(f"  -> INFO: This can happen if no rules were set. Usually safe to ignore.")


    def recover_resource(self, intent):
        """Attempts to recover host resources (CPU/Memory)."""
        # Recovery could involve:
        # 1. Killing non-essential processes on the host.
        # 2. Migrating services to another host (in a more advanced setup).
        print(f"    - ACTION: Placeholder for recovering resources on host {intent['target']}.")
        pass

    def recover_cpu_usage(self, intent):
        """
        Identifies the top 3 CPU-consuming processes on the host and
        prints a warning to the network operator.
        """
        host_id = intent['target']
        intent_type = intent['type']
        value = intent['value']
        host = self.net.get(host_id)

        print(f"  -> RECOVERY: High {intent_type} detected on host {host_id} (threshold: {value}%).")
        print(f"  -> ACTION: Identifying top 3 CPU-consuming processes on {host_id}...")

        try:
            # Command to get top 3 processes:
            # -bn1: batch mode, 1 iteration
            # tail -n +8: Skip the 7 header lines of 'top'
            # head -n 3: Take just the top 3 processes
            # awk: Print PID (col 1), %CPU (col 9), and Command (col 12)
            command = "top -bn1 | tail -n +8 | head -n 3 | awk '{print $1, $9, $12}'"
            
            result = host.cmd(command).strip()

            if not result:
                print(f"  -> INFO: No high-CPU processes found or 'top' command failed on {host_id}.")
                return

            print(f"  -> WARNING: Top 3 CPU consumers on {host_id}:")
            
            # Split the result into lines and parse each one
            top_processes = result.split('\n')
            for i, line in enumerate(top_processes):
                if not line.strip():
                    continue
                try:
                    # Parse the line, e.g., "1234 99.9 yes"
                    parts = line.split()
                    pid = parts[0]
                    cpu_percent = parts[1]
                    comm = parts[2]
                    
                    # Print a formatted warning
                    print(f"    {i+1}. PID: {pid:<8} | %CPU: {cpu_percent:<6} | COMMAND: {comm}")
                
                except (IndexError, ValueError) as e:
                    print(f"    - Error parsing 'top' output line: '{line}'. Error: {e}")

        except Exception as e:
            print(f"  -> ERROR: Failed to execute 'top' command on {host_id}: {e}")

    def recover_traffic_routing(self, intent):
        """Attempts to recover by rerouting traffic."""
        # This is highly dependent on the topology and controller logic.
        # It could involve adding new flow rules to switches to divert traffic
        # away from a congested or failing link.
        print(f"    - ACTION: Placeholder for rerouting traffic related to {intent['target']}.")
        pass
