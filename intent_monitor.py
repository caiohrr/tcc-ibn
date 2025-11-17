# intent_monitor.py
import threading
import time
import json
import re
import os
from datetime import datetime
from pathlib import Path

# Assuming main.py is in the same directory or accessible in the path
# We need the PluginManager and the MonitorRecoveryPlugin interface
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
        }
        self.recovery_functions = {
            'CONNECTIVITY': self.recover_connectivity,
            'BANDWIDTH': self.recover_link_params,
            'DELAY': self.recover_link_params,
            'PACKET_LOSS': self.recover_link_params,
            'CPU_USAGE': self.recover_cpu_usage,
            'MEMORY_USAGE': self.recover_memory_usage,
        }

    def _register_plugin_functions(self):
        """Discovers and registers check/recovery functions from plugins."""
        # The 'MonitorRecoveryPlugin' type is defined in main.py
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
            params = conn.get('PARAMS', {})
            endpoints = tuple(conn.get('ENDPOINTS', []))
            
            for key, value in params.items():
                if key in self.check_functions:
                    self.intents.append({
                        'type': key,
                        'target': endpoints,
                        'value': value,
                        'description': f"{key} <= {value} for link {endpoints[0]}-{endpoints[1]}",
                        'status': 'UNKNOWN'
                    })

        # --- Host Resource Intents ---
        for host_data in self.topology.hosts:
            for key, value in host_data.items():
                if key in self.check_functions:
                    self.intents.append({
                        'type': key,
                        'target': host_data['id'],
                        'value': value,
                        'description': f"{key} <= {value} for host {host_data['id']}",
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
                is_ok = check_function(self, intent)
                
                if not is_ok:
                    intent['status'] = 'BROKEN'
                    log_entry = f"  [✗] BROKEN: {intent['description']}"
                    print(log_entry)
                    self.report.append({'timestamp': timestamp, 'log': log_entry, 'intent': intent})
                    
                    if self.recovery_enabled:
                        recovery_function = self.recovery_functions.get(intent['type'])
                        if recovery_function:
                            print(f"    -> Attempting recovery for '{intent['type']}'...")
                            recovery_function(self, intent)
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
        """
        Exports the monitoring report to a JSON file in the 'logs' directory
        and sets correct ownership if run with sudo.
        """
        try:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)

            report_filename = f"intent_report_{self.topology.id}_{datetime.now():%Y%m%d_%H%M%S}.json"
            report_path = log_dir / report_filename

            with open(report_path, 'w') as f:
                json.dump(self.report, f, indent=4)
            
            print(f"✔ Intent monitoring report saved to '{report_path}'")

            # If script was run with sudo, change ownership of the log file and directory
            # back to the original user to avoid permission issues.
            sudo_uid_str = os.environ.get('SUDO_UID')
            sudo_gid_str = os.environ.get('SUDO_GID')

            if sudo_uid_str and sudo_gid_str:
                sudo_uid = int(sudo_uid_str)
                sudo_gid = int(sudo_gid_str)
                
                os.chown(log_dir, sudo_uid, sudo_gid)
                os.chown(report_path, sudo_uid, sudo_gid)
                print(f"  -> Ownership of '{report_path.parent}' and its contents restored to the original user.")
            
        except Exception as e:
            print(f"✗ ERROR: Failed to export report: {e}")
        
# --- Monitoring functions ---
    
    def check_connectivity(self, monitor, intent):
        """Checks if two hosts can ping each other."""
        host1_id, host2_id = intent['target']
        host1 = monitor.net.get(host1_id)
        host2 = monitor.net.get(host2_id)
        result = host1.cmd(f'ping -c 1 {host2.IP()}')
        is_successful = '0% packet loss' in result
        return is_successful

    def check_bandwidth(self, monitor, intent):
        """Checks if a link exceeds its configured bandwidth cap."""
        host1_id, host2_id = intent['target']
        max_bw_mbps = intent['value']
        host1 = monitor.net.get(host1_id)
        iface = host1.intfNames()[0]

        # Measure tx bytes over a precise time window
        tx_bytes_1 = int(host1.cmd(f"cat /sys/class/net/{iface}/statistics/tx_bytes").strip())
        t1 = time.time()
        time.sleep(1)
        tx_bytes_2 = int(host1.cmd(f"cat /sys/class/net/{iface}/statistics/tx_bytes").strip())
        t2 = time.time()

        elapsed = t2 - t1
        bw_bps = (tx_bytes_2 - tx_bytes_1) * 8 / elapsed
        bw_mbps = bw_bps / 1_000_000

        #print(f"Elapsed = {elapsed} s; bw bps = {bw_bps}")
        print(f"[INFO] ({host1_id}-{host2_id}) Current bandwidth = ({bw_mbps:.8f} Mbps. Max = {max_bw_mbps} Mbps)")

        # Warn if usage is within 10% of max
        if bw_mbps >= 0.9 * max_bw_mbps:
            print(f"[WARN] Bandwidth usage is high: {bw_mbps:.2f} Mbps (≥ 90% of limit {max_bw_mbps} Mbps)")

        if bw_mbps > max_bw_mbps:  
            print(f"[WARN] Bandwidth exceeds cap! ({bw_mbps:.8f} Mbps > {max_bw_mbps} Mbps)")
            return False
        else:
            print(f"[OK] Bandwidth within limit ({bw_mbps:.8f} Mbps ≤ {max_bw_mbps} Mbps)")
            return True

    def check_delay(self, monitor, intent):
        """Checks if a link's delay is within the acceptable limit."""
        host1_id, host2_id = intent['target']
        max_delay_match = re.match(r"(\d+(?:\.\d+)?)ms", intent['value'])
        max_delay = float(max_delay_match.group(1))
        host1 = monitor.net.get(host1_id)
        host2 = monitor.net.get(host2_id)
        result = host1.cmd(f'ping -c 3 {host2.IP()}')
        match = re.search(r'rtt .* = .*?/([\d.]+)/.* ms', result)
        if match:
            avg_delay = float(match.group(1))
            if avg_delay <= max_delay:
                return True
            else:
                print(f"[WARN] Delay exceeded threshold ({max_delay} ms)!")
                return False
        else:
            print(f"[ERROR] Could not parse ping output:\n{result}")
            return False

    def check_packet_loss(self, monitor, intent):
        """Checks if a link's packet loss is below the threshold."""
        host1_id, host2_id = intent['target']
        max_loss = intent['value']
        host1 = monitor.net.get(host1_id)
        host2 = monitor.net.get(host2_id)
        result = host1.cmd(f'ping -c 5 {host2.IP()}')
        match = re.search(r'(\d+)% packet loss', result)
        if match:
            loss = int(match.group(1))
            return loss <= max_loss
        else:
            print("[ERROR] Could not parse ping output")
        return False
    
    def check_cpu_usage(self, monitor, intent):
        """Checks a host's CPU usage."""
        host_id = intent['target']
        max_cpu = intent.get('value', 80) * 100
        host = monitor.net.get(host_id)
        result = host.cmd("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        try:
            cpu_usage = float(result.strip().replace('%', ''))
            if cpu_usage <= max_cpu:
                return True
            else:
                print(f"[WARN] CPU usage exceeded threshold ({max_cpu}%)!")
                return False
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Could not parse CPU usage for {host_id}: {e}")
        return False
       
    def check_memory_usage(self, monitor, intent):
        """Checks a host's memory usage."""
        host_id = intent['target']
        max_ram_mb = intent.get('value') # This value is in MB from the topology
        
        host = monitor.net.get(host_id)
        
        result = host.cmd("free -m | grep 'Mem:' | awk '{print $3}'")
        
        try:
            # The result is already in MiB (Mebibytes)
            used_mb = float(result.strip())
            
            print(f"[INFO] Memory usage for {host_id}: {used_mb:.2f} MB / {max_ram_mb} MB")
            
            if used_mb <= max_ram_mb:
                return True
            else:
                print(f"[WARN] Memory usage exceeded threshold ({max_ram_mb} MB)!")
                return False
        except (ValueError, IndexError) as e:
            print(f"[ERROR] Could not parse Memory usage for {host_id}: {e}")
        return False
        
    def recover_connectivity(self, monitor, intent):
        """Attempts to recover connectivity by ensuring host interfaces are 'UP'."""
        host1_id, host2_id = intent['target']
        host1 = monitor.net.get(host1_id)
        host2 = monitor.net.get(host2_id)
        try:
            iface1 = host1.intfNames()[0]
            iface2 = host2.intfNames()[0]
            print(f"  -> ACTION: Ensuring interfaces are UP for {host1_id}({iface1}) and {host2_id}({iface2}).")
            host1.cmd(f"ip link set {iface1} up")
            host2.cmd(f"ip link set {iface2} up")
        except Exception as e:
            print(f"  -> ERROR: Failed to bring interfaces up for {host1_id}-{host2_id}: {e}")        


    def recover_link_params(self, monitor, intent):
        """
        Resets the link parameters to *all* of its defined intents.
        """
        # Get the nodes and link
        node1_id, node2_id = intent['target']
        target_link = tuple(sorted(intent['target'])) # Use sorted tuple for easy comparison

        node1 = monitor.net.get(node1_id)
        node2 = monitor.net.get(node2_id)

        links = monitor.net.linksBetween(node1, node2)
        if not links:
            print(f"  -> ERROR: Could not find link between {node1_id} and {node2_id}.")
            return

        link = links[0]
        intf1, intf2 = link.intf1, link.intf2
        
        # 1. Find ALL intents related to this link and build a param dict
        link_params = {}
        for i in monitor.intents:
            # Check if the intent's target matches our link
            if 'target' in i and tuple(sorted(i.get('target', ()))) == target_link:
                if i['type'] == 'BANDWIDTH':
                    link_params['bw'] = i['value']
                elif i['type'] == 'DELAY':
                    link_params['delay'] = i['value']
                elif i['type'] == 'PACKET_LOSS':
                    link_params['loss'] = i['value'] 
                    
        if not link_params:
            # If no params are defined, reset the link to default (no rules)
            print(f"  -> INFO: No defined params for link {target_link}. Resetting to default.")
            try:
                # We use tc qdisc del to be certain all rules are gone.
                intf1.node.cmd(f"tc qdisc del dev {intf1.name} root")
                intf2.node.cmd(f"tc qdisc del dev {intf2.name} root")
            except Exception as e:
                # This fails if no rules exist, which is fine.
                print(f"  -> INFO: No existing TC rules to delete on {target_link}.") 
            return

        # 2. Apply all found parameters at once using keyword arguments
        print(f"  -> ACTION: Re-applying all intents {link_params} to link {target_link}.")
        for intf in [intf1, intf2]:
            intf.config(**link_params)
            
        print(f"  -> INFO: Link parameters for {node1_id}-{node2_id} have been restored.")

    def recover_memory_usage(self, monitor, intent):
        """
        Identifies the top 3 Memory-consuming processes on the host and
        prints a warning to the network operator. (Recovery for MEMORY_USAGE)
        """
        host_id = intent['target']
        intent_type = intent['type']
        value = intent['value']
        host = monitor.net.get(host_id)

        print(f"  -> RECOVERY: High {intent_type} detected on host {host_id} (threshold: {value} MB).")
        print(f"  -> ACTION: Identifying top 3 Memory-consuming processes on {host_id}...")

        try:
            command = "top -bn1 | tail -n +8 | sort -k 10 -r -n | head -n 3 | awk '{print $1, $10, $12}'"
            
            result = host.cmd(command).strip()

            if not result:
                print(f"  -> INFO: No high-memory processes found or 'top' command failed on {host_id}.")
                return

            print(f"  -> WARNING: Top 3 Memory consumers on {host_id}:")
            
            top_processes = result.split('\n')
            for i, line in enumerate(top_processes):
                if not line.strip():
                    continue
                try:
                    parts = line.split()
                    pid = parts[0]
                    mem_percent = parts[1]
                    comm = parts[2]
                    
                    print(f"    {i+1}. PID: {pid:<8} | %MEM: {mem_percent:<6} | COMMAND: {comm}")
                
                except (IndexError, ValueError) as e:
                    print(f"    - Error parsing 'top' output line: '{line}'. Error: {e}")

        except Exception as e:
            print(f"  -> ERROR: Failed to execute 'top' command on {host_id}: {e}")

    def recover_cpu_usage(self, monitor, intent):
        """Identifies top CPU-consuming processes as a warning."""
        host_id = intent['target']
        host = monitor.net.get(host_id)
        print(f"  -> ACTION: Identifying top 3 CPU-consuming processes on {host_id}...")
        try:
            command = "top -bn1 | tail -n +8 | head -n 3 | awk '{print $1, $9, $12}'"
            result = host.cmd(command).strip()
            if not result:
                print(f"  -> INFO: No high-CPU processes found or 'top' command failed on {host_id}.")
                return
            print(f"  -> WARNING: Top 3 CPU consumers on {host_id}:")
            for i, line in enumerate(result.split('\n')):
                if line.strip():
                    parts = line.split()
                    print(f"    {i+1}. PID: {parts[0]:<8} | %CPU: {parts[1]:<6} | COMMAND: {parts[2]}")
        except Exception as e:
            print(f"  -> ERROR: Failed to execute 'top' command on {host_id}: {e}")
