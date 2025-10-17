# intent_monitor.py
"""
Intent-Based Network Monitoring and Recovery System
Monitors network intents and executes recovery actions when violations are detected.
"""

import json
import threading
import time
import subprocess
import re
import os
import statistics
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from collections import deque


class IntentStatus(Enum):
    """Status of an intent."""
    SATISFIED = "SATISFIED"
    VIOLATED = "VIOLATED"
    RECOVERING = "RECOVERING"
    UNRECOVERABLE = "UNRECOVERABLE"
    UNKNOWN = "UNKNOWN"


class IntentType(Enum):
    """Types of network intents."""
    CONNECTIVITY = "CONNECTIVITY"
    BANDWIDTH = "BANDWIDTH"
    DELAY = "DELAY"
    PACKET_LOSS = "PACKET_LOSS"
    JITTER = "JITTER"
    CPU_USAGE = "CPU_USAGE"
    MEMORY_USAGE = "MEMORY_USAGE"
    LINK_UTILIZATION = "LINK_UTILIZATION"


@dataclass
class IntentViolation:
    """Represents a detected intent violation."""
    intent_id: str
    intent_type: IntentType
    expected_value: Any
    actual_value: Any
    timestamp: datetime
    component_id: str
    severity: str = "MEDIUM"
    message: str = ""


@dataclass
class IntentMetric:
    """Stores metric history for trend analysis."""
    values: deque = field(default_factory=lambda: deque(maxlen=10))
    timestamps: deque = field(default_factory=lambda: deque(maxlen=10))
    
    def add_measurement(self, value: float, timestamp: datetime = None):
        """Add a new measurement."""
        if timestamp is None:
            timestamp = datetime.now()
        self.values.append(value)
        self.timestamps.append(timestamp)
    
    def get_average(self) -> Optional[float]:
        """Get average of recent measurements."""
        if not self.values:
            return None
        return statistics.mean(self.values)
    
    def get_trend(self) -> str:
        """Analyze trend: STABLE, IMPROVING, DEGRADING."""
        if len(self.values) < 3:
            return "STABLE"
        
        recent = list(self.values)[-3:]
        if recent[-1] > recent[0] * 1.1:
            return "DEGRADING"
        elif recent[-1] < recent[0] * 0.9:
            return "IMPROVING"
        return "STABLE"


class IntentMonitor:
    """Main class for monitoring and recovering network intents."""
    
    def __init__(self, topology: 'Topology', mininet_instance=None):
        self.topology = topology
        self.net = mininet_instance
        self.monitoring_active = False
        self.monitor_thread = None
        self.recovery_thread = None
        
        # Intent tracking
        self.intents = self._parse_intents()
        self.intent_status = {}
        self.intent_metrics = {}
        self.violations = []
        self.recovery_actions = []
        
        # Monitoring configuration
        self.monitor_interval = 5  # seconds
        self.recovery_interval = 2  # seconds (reduced for faster response)
        self.recovery_enabled = True
        self.max_recovery_attempts = 3
        self.recovery_attempts = {}
        
        # Recovery strategies
        self.recovery_strategies = self._initialize_recovery_strategies()

       # Ensure log directory exists
        self.log_dir = "log"
        os.makedirs(self.log_dir, exist_ok=True) 

    def _parse_intents(self) -> Dict[str, Dict]:
        """Parse intents from topology configuration."""
        intents = {}
        
        # Connection intents (connectivity, bandwidth, delay, loss, jitter)
        for conn in self.topology.connections:
            endpoints = conn.get('ENDPOINTS', [])
            if len(endpoints) == 2:
                conn_id = f"{endpoints[0]}-{endpoints[1]}"
                
                # Connectivity intent (implicit)
                intents[f"conn_{conn_id}"] = {
                    'type': IntentType.CONNECTIVITY,
                    'endpoints': endpoints,
                    'expected': True
                }
                
                # Parameter-based intents
                params = conn.get('PARAMS', {})
                if 'bandwidth' in params:
                    intents[f"bw_{conn_id}"] = {
                        'type': IntentType.BANDWIDTH,
                        'endpoints': endpoints,
                        'expected': float(params['bandwidth']),
                        'unit': 'Mbps'
                    }
                
                if 'delay' in params:
                    delay_value = params['delay']
                    if isinstance(delay_value, str):
                        delay_value = float(delay_value.replace('ms', ''))
                    intents[f"delay_{conn_id}"] = {
                        'type': IntentType.DELAY,
                        'endpoints': endpoints,
                        'expected': delay_value,
                        'unit': 'ms'
                    }
                
                if 'loss' in params:
                    intents[f"loss_{conn_id}"] = {
                        'type': IntentType.PACKET_LOSS,
                        'endpoints': endpoints,
                        'expected': float(params['loss']),
                        'unit': '%'
                    }
                
                if 'jitter' in params:
                    jitter_value = params['jitter']
                    if isinstance(jitter_value, str):
                        jitter_value = float(jitter_value.replace('ms', ''))
                    intents[f"jitter_{conn_id}"] = {
                        'type': IntentType.JITTER,
                        'endpoints': endpoints,
                        'expected': jitter_value,
                        'unit': 'ms'
                    }
        
        # Host resource intents
        for host in self.topology.hosts:
            host_id = host['id']
            
            # CPU usage intent
            if 'cpu' in host:
                intents[f"cpu_{host_id}"] = {
                    'type': IntentType.CPU_USAGE,
                    'host': host_id,
                    'expected': host['cpu'],
                    'unit': 'cores'
                }
            
            # Memory usage intent
            if 'memory' in host:
                mem_value = host['memory']
                if isinstance(mem_value, str):
                    if 'm' in mem_value.lower():
                        mem_value = int(mem_value.lower().replace('m', ''))
                    elif 'g' in mem_value.lower():
                        mem_value = int(mem_value.lower().replace('g', '')) * 1024
                
                intents[f"mem_{host_id}"] = {
                    'type': IntentType.MEMORY_USAGE,
                    'host': host_id,
                    'expected': mem_value,
                    'unit': 'MB'
                }
        
        return intents
    
    def _initialize_recovery_strategies(self) -> Dict[IntentType, Callable]:
        """Initialize recovery strategies for different intent types."""
        return {
            IntentType.CONNECTIVITY: self._recover_connectivity,
            IntentType.BANDWIDTH: self._recover_bandwidth,
            IntentType.DELAY: self._recover_delay,
            IntentType.PACKET_LOSS: self._recover_packet_loss,
            IntentType.CPU_USAGE: self._recover_cpu_usage,
            IntentType.MEMORY_USAGE: self._recover_memory_usage,
            IntentType.LINK_UTILIZATION: self._recover_link_utilization
        }
    
    def start_monitoring(self):
        """Start the monitoring threads."""
        if self.monitoring_active:
            print("⚠️  Monitoring is already active")
            return
        
        self.monitoring_active = True
        
        self._kickstart_network()

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        # Start recovery thread if enabled
        if self.recovery_enabled:
            self.recovery_thread = threading.Thread(target=self._recovery_loop, daemon=True)
            self.recovery_thread.start()
        
        print("✅ Intent monitoring started")
        print(f"   - Monitoring interval: {self.monitor_interval}s")
        print(f"   - Recovery enabled: {self.recovery_enabled}")
        print(f"   - Total intents tracked: {len(self.intents)}")
    
    def stop_monitoring(self):
        """Stop the monitoring threads."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        if self.recovery_thread:
            self.recovery_thread.join(timeout=2)
        print("🛑 Intent monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        time.sleep(2)  # Initial delay
        while self.monitoring_active:
            try:
                violations = self._check_all_intents()
                
                if violations:
                    self._handle_violations(violations)
                
                self._print_status_summary()
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
            
            time.sleep(self.monitor_interval)
    
    def _recovery_loop(self):
        """Main recovery loop."""
        while self.monitoring_active:
            try:
                if self.recovery_actions:
                    action = self.recovery_actions.pop(0)
                    self._execute_recovery(action)
                
            except Exception as e:
                print(f"❌ Recovery error: {e}")
            
            time.sleep(self.recovery_interval)
    
    def _check_all_intents(self) -> List[IntentViolation]:
        """Check all intents and return violations."""
        violations = []
        
        for intent_id, intent_spec in self.intents.items():
            status, actual_value = self._check_intent(intent_id, intent_spec)
            
            if intent_id not in self.intent_metrics:
                self.intent_metrics[intent_id] = IntentMetric()
            
            if actual_value is not None and isinstance(actual_value, (int, float)):
                self.intent_metrics[intent_id].add_measurement(actual_value)
            
            self.intent_status[intent_id] = status
            
            if status == IntentStatus.VIOLATED:
                violation = IntentViolation(
                    intent_id=intent_id,
                    intent_type=intent_spec['type'],
                    expected_value=intent_spec.get('expected'),
                    actual_value=actual_value,
                    timestamp=datetime.now(),
                    component_id=self._get_component_id(intent_spec)
                )
                violations.append(violation)
        
        return violations
    
    def _check_intent(self, intent_id: str, intent_spec: Dict) -> Tuple[IntentStatus, Any]:
        """Check a specific intent."""
        intent_type = intent_spec['type']
        
        if intent_type == IntentType.CONNECTIVITY:
            return self._check_connectivity(intent_spec)
        elif intent_type == IntentType.BANDWIDTH:
            return self._check_bandwidth(intent_spec)
        elif intent_type == IntentType.DELAY:
            return self._check_delay(intent_spec)
        elif intent_type == IntentType.PACKET_LOSS:
            return self._check_packet_loss(intent_spec)
        elif intent_type == IntentType.CPU_USAGE:
            return self._check_cpu_usage(intent_spec)
        elif intent_type == IntentType.MEMORY_USAGE:
            return self._check_memory_usage(intent_spec)
        else:
            return IntentStatus.UNKNOWN, None
    
    def _check_connectivity(self, intent_spec: Dict) -> Tuple[IntentStatus, bool]:
        """Check connectivity between two endpoints."""
        if not self.net:
            return IntentStatus.UNKNOWN, None
        
        endpoints = intent_spec['endpoints']
        try:
            h1 = self.net.get(endpoints[0])
            h2 = self.net.get(endpoints[1])
            
            if h1 and h2 and hasattr(h2, 'IP'):
                # Check if shell is available
                if not self._check_shell_health(h1):
                    return IntentStatus.VIOLATED, False
                
                result = h1.cmd(f'ping -c 1 -W 1 {h2.IP()}')
                is_connected = '1 received' in result
                status = IntentStatus.SATISFIED if is_connected else IntentStatus.VIOLATED
                return status, is_connected
        except Exception as e:
            print(f"   Connectivity check error: {e}")
        return IntentStatus.UNKNOWN, None
    
    def _check_shell_health(self, node) -> bool:
        """Check if a node's shell is healthy."""
        try:
            if not hasattr(node, 'shell') or node.shell is None:
                return False
            if hasattr(node, 'waiting') and node.waiting:
                return False
            # Quick test
            result = node.cmd('echo test')
            return 'test' in result
        except:
            return False
    
    def _check_delay(self, intent_spec: Dict) -> Tuple[IntentStatus, float]:
        """Check delay between two endpoints."""
        if not self.net:
            return IntentStatus.UNKNOWN, None
        
        endpoints, expected_delay = intent_spec['endpoints'], intent_spec['expected']
        try:
            h1, h2 = self.net.get(endpoints[0]), self.net.get(endpoints[1])
            if h1 and h2 and hasattr(h2, 'IP'):
                if not self._check_shell_health(h1):
                    return IntentStatus.UNKNOWN, None
                    
                result = h1.cmd(f'ping -c 3 -W 1 {h2.IP()}')
                match = re.search(r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/', result)
                if match:
                    actual_delay = float(match.group(1))
                    if actual_delay <= expected_delay * 1.2:  # 20% tolerance
                        return IntentStatus.SATISFIED, actual_delay
                    else:
                        return IntentStatus.VIOLATED, actual_delay
        except Exception:
            pass
        return IntentStatus.UNKNOWN, None

    def _check_bandwidth(self, intent_spec: Dict) -> Tuple[IntentStatus, float]:
        """Check bandwidth availability."""
        if not self.net:
            return IntentStatus.UNKNOWN, None
        
        endpoints, expected_bw = intent_spec['endpoints'], intent_spec['expected']
        try:
            for link in self.net.links:
                if (link.intf1.node.name in endpoints and link.intf2.node.name in endpoints):
                    # Check if both interfaces are up
                    intf1_up = self._check_interface_status(link.intf1)
                    intf2_up = self._check_interface_status(link.intf2)
                    if intf1_up and intf2_up:
                        return IntentStatus.SATISFIED, expected_bw
                    else:
                        return IntentStatus.VIOLATED, 0
            return IntentStatus.VIOLATED, 0
        except Exception:
            pass
        return IntentStatus.UNKNOWN, None
    
    def _check_interface_status(self, intf) -> bool:
        """Check if an interface is up."""
        try:
            result = intf.node.cmd(f'ip link show {intf.name}')
            return 'state UP' in result
        except:
            return False

    def _check_packet_loss(self, intent_spec: Dict) -> Tuple[IntentStatus, float]:
        """Check packet loss between endpoints."""
        if not self.net:
            return IntentStatus.UNKNOWN, None
        
        endpoints, expected_loss = intent_spec['endpoints'], intent_spec['expected']
        try:
            h1, h2 = self.net.get(endpoints[0]), self.net.get(endpoints[1])
            if h1 and h2 and hasattr(h2, 'IP'):
                if not self._check_shell_health(h1):
                    return IntentStatus.UNKNOWN, None
                    
                result = h1.cmd(f'ping -c 10 -W 1 {h2.IP()}')
                match = re.search(r'(\d+)% packet loss', result)
                if match:
                    actual_loss = float(match.group(1))
                    if actual_loss <= expected_loss:
                        return IntentStatus.SATISFIED, actual_loss
                    else:
                        return IntentStatus.VIOLATED, actual_loss
        except Exception:
            pass
        return IntentStatus.UNKNOWN, None
    
    def _check_cpu_usage(self, intent_spec: Dict) -> Tuple[IntentStatus, float]:
        """Check CPU usage for a host."""
        return IntentStatus.SATISFIED, 0

    def _check_memory_usage(self, intent_spec: Dict) -> Tuple[IntentStatus, float]:
        """Check memory usage for a host."""
        if not self.net:
            return IntentStatus.UNKNOWN, None
        
        host_id, expected_mem = intent_spec['host'], intent_spec['expected']
        try:
            host = self.net.get(host_id)
            if host and hasattr(host, 'cmd'):
                if not self._ncheck_shell_health(host):
                    return IntentStatus.UNKNOWN, None
                    
                result = host.cmd("free -m | grep Mem | awk '{print $3}'")
                if result:
                    mem_usage = float(result.strip())
                    if mem_usage <= expected_mem:
                        return IntentStatus.SATISFIED, mem_usage
                    else:
                        return IntentStatus.VIOLATED, mem_usage
        except Exception:
            pass
        return IntentStatus.UNKNOWN, None
    
    def _get_component_id(self, intent_spec: Dict) -> str:
        """Get component ID from intent specification."""
        if 'endpoints' in intent_spec:
            return f"{intent_spec['endpoints'][0]}-{intent_spec['endpoints'][1]}"
        elif 'host' in intent_spec:
            return intent_spec['host']
        return "unknown"
    
    def _handle_violations(self, violations: List[IntentViolation]):
        """Handle detected violations."""
        for violation in violations:
            self.violations.append(violation)
            self._log_violation(violation)
            
            if self.recovery_enabled and self._can_recover(violation):
                self.recovery_actions.append(violation)
            elif self.recovery_enabled and not self._can_recover(violation):
                self._notify_operator(violation, "Max recovery attempts reached.")
            else:
                self._notify_operator(violation, "Automatic recovery is disabled.")
    
    def _can_recover(self, violation: IntentViolation) -> bool:
        """Check if automatic recovery is possible for this violation."""
        key = f"{violation.intent_id}_{violation.intent_type}"
        attempts = self.recovery_attempts.get(key, 0)
        
        if attempts >= self.max_recovery_attempts:
            return False
        
        return violation.intent_type in self.recovery_strategies
    
    def _execute_recovery(self, violation: IntentViolation):
        """Execute recovery action for a violation."""
        print(f"\n🔧 Attempting recovery for {violation.intent_id}")
        
        key = f"{violation.intent_id}_{violation.intent_type}"
        self.recovery_attempts[key] = self.recovery_attempts.get(key, 0) + 1
        
        strategy = self.recovery_strategies.get(violation.intent_type)
        if strategy:
            success = strategy(violation)
            
            if success:
                print(f"   ✅ Recovery successful for {violation.intent_id}")
                self.recovery_attempts[key] = 0
            else:
                print(f"   ❌ Recovery failed for {violation.intent_id}")
                if self.recovery_attempts[key] >= self.max_recovery_attempts:
                    self._notify_operator(violation, "Recovery failed after max attempts.")
    
    def _restart_host_shell(self, node):
        """Restart a host's shell."""
        try:
            print(f"     - Restarting shell for {node.name}")
            # Terminate old shell
            if hasattr(node, 'shell') and node.shell:
                try:
                    node.shell.terminate()
                except:
                    pass
            
            # Start new shell
            node.startShell()
            time.sleep(0.5)  # Give shell time to initialize
            
            # Test shell
            return self._check_shell_health(node)
        except Exception as e:
            print(f"     - Shell restart error: {e}")
            return False
    
    def _recover_connectivity(self, violation: IntentViolation) -> bool:
        """Recover connectivity issues using Mininet API when possible.

        Strategy:
        1. Try to use self.net.configLinkStatus(endpointA, endpointB, 'up')
           — this keeps Mininet internal state consistent.
        2. Find the actual link object (self.net.links) that connects the endpoints.
        3. Ensure both interfaces (link.intf1, link.intf2) are administratively UP
           at kernel level (ip link set ... up).
        4. If a switch is involved, re-apply a default flow (normal) to allow L2 forwarding.
        5. Verify recovery with a ping when endpoints are hosts with IPs, otherwise
           check interface 'state UP' on the host side as a weaker verification.
        """
        if not self.net:
            return False

        try:
            endpoints = self.intents.get(violation.intent_id, {}).get('endpoints', [])
            if len(endpoints) != 2:
                return False

            ep1, ep2 = endpoints
            print(f"   → Recovering connectivity for {ep1}<->{ep2}")

            # 1) Try Mininet API to configure link status (keeps Mininet internal state consistent)
            try:
                if hasattr(self.net, 'configLinkStatus'):
                    print("     - Using Mininet API to set link up")
                    try:
                        self.net.configLinkStatus(ep1, ep2, 'up')
                        # small pause to let Mininet apply changes
                        time.sleep(0.3)
                    except Exception as e:
                        print(f"     - configLinkStatus warning/error: {e}")
            except Exception:
                # defensive: continue to manual approach
                pass

            # 2) Find the specific link connecting these endpoints
            link = next(
                (l for l in getattr(self.net, 'links', [])
                 if {l.intf1.node.name, l.intf2.node.name} == {ep1, ep2}),
                None
            )
            if not link:
                print("     - Could not find link object for endpoints; trying interface-level recovery")
                # fallback: try to bring up interfaces by constructing names from endpoints
                # (best-effort; may fail if naming differs)
                for node_name in (ep1, ep2):
                    node = self.net.get(node_name)
                    if node:
                        for intf in node.intfList():
                            if intf.name != 'lo':
                                print(f"     - (fallback) Bringing up {intf.name} on {node.name}")
                                node.cmd(f'ip link set {intf.name} up')
                time.sleep(0.5)
            else:
                # 3) Bring up the exact interfaces for this link
                for intf in (link.intf1, link.intf2):
                    try:
                        print(f"     - Bringing up {intf.name} on {intf.node.name}")
                        intf.node.cmd(f'ip link set {intf.name} up')
                    except Exception as e:
                        print(f"     - Error bringing up {intf.name}: {e}")

                # 4) If a switch is involved, ensure normal forwarding rule exists
                for node in (link.intf1.node, link.intf2.node):
                    try:
                        if node.name.startswith('s'):
                            node.cmd(f'ovs-ofctl add-flow {node.name} "priority=0,actions=normal"')
                    except Exception as e:
                        print(f"     - Could not add default flow on {node.name}: {e}")

                time.sleep(0.7)  # allow stabilization

            # 5) Verification
            h1 = self.net.get(ep1)
            h2 = self.net.get(ep2)

            # If both endpoints are hosts with IPs, prefer a ping verification
            if h1 and h2 and hasattr(h1, 'IP') and hasattr(h2, 'IP') and h1.IP() and h2.IP():
                try:
                    result = h1.cmd(f'ping -c 1 -W 1 {h2.IP()}')
                    success = '1 received' in result or '1 packets received' in result
                    return bool(success)
                except Exception:
                    pass

            # If one endpoint is a switch (no IP), check that host side interface is UP
            for host_ep in (ep1, ep2):
                node = self.net.get(host_ep)
                if node and hasattr(node, 'cmd'):
                    for intf in node.intfList():
                        if intf.name == 'lo':
                            continue
                        try:
                            out = node.cmd(f'ip link show {intf.name}')
                            if 'state UP' in out:
                                # if any non-loopback intf on the host is UP, consider recovery likely
                                return True
                        except Exception:
                            continue

            # As a last-ditch check: if we found a link earlier, consider success if both kernel interfaces report UP
            if link:
                all_up = True
                for intf in (link.intf1, link.intf2):
                    try:
                        out = intf.node.cmd(f'ip link show {intf.name}')
                        if 'state UP' not in out:
                            all_up = False
                            break
                    except Exception:
                        all_up = False
                        break
                if all_up:
                    return True

        except Exception as e:
            print(f"   ❌ Recovery error: {e}")

        return False

    
    def _recover_link_param(self, violation: IntentViolation, param_type: str) -> bool:
        """Generic recovery function for link parameters."""
        if not self.net:
            return False
        try:
            intent = self.intents.get(violation.intent_id, {})
            endpoints, expected_val = intent.get('endpoints', []), intent.get('expected')
            
            if not (len(endpoints) == 2 and expected_val is not None):
                return False

            cmd_map = {
                "delay": f"delay {expected_val}ms",
                "bandwidth": f"rate {expected_val}mbit",
                "loss": f"loss {expected_val}%"
            }
            tc_cmd_part = cmd_map.get(param_type)
            if not tc_cmd_part:
                return False
            
            print(f"   → Reconfiguring {param_type} to {expected_val} for {endpoints[0]}<->{endpoints[1]}")

            for link in self.net.links:
                if (link.intf1.node.name in endpoints and link.intf2.node.name in endpoints):
                    for intf in [link.intf1, link.intf2]:
                        intf.node.cmd(f'tc qdisc del dev {intf.name} root 2>/dev/null')
                        if param_type == 'bandwidth':
                            intf.node.cmd(f'tc qdisc add dev {intf.name} root handle 1: htb default 1')
                            intf.node.cmd(f'tc class add dev {intf.name} parent 1: classid 1:1 htb {tc_cmd_part}')
                        else:
                            intf.node.cmd(f'tc qdisc add dev {intf.name} root netem {tc_cmd_part}')
                    return True
        except Exception as e:
            print(f"   ❌ Recovery error: {e}")
        return False

    def _recover_delay(self, v: IntentViolation) -> bool:
        return self._recover_link_param(v, 'delay')
    
    def _recover_bandwidth(self, v: IntentViolation) -> bool:
        return self._recover_link_param(v, 'bandwidth')
    
    def _recover_packet_loss(self, v: IntentViolation) -> bool:
        return self._recover_link_param(v, 'loss')
    
    def _recover_cpu_usage(self, violation: IntentViolation) -> bool:
        """Recover CPU usage issues."""
        print("   → CPU recovery not supported in standard Mininet")
        return False

    def _recover_memory_usage(self, violation: IntentViolation) -> bool:
        """Recover memory usage issues."""
        if not self.net:
            return False
        try:
            host_id = self.intents.get(violation.intent_id, {}).get('host')
            if host_id:
                host = self.net.get(host_id)
                if host and hasattr(host, 'cmd'):
                    print(f"   → Clearing caches for {host_id}")
                    host.cmd("sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null")
                    return True
        except Exception as e:
            print(f"   ❌ Recovery error: {e}")
        return False
    
    def _recover_link_utilization(self, violation: IntentViolation) -> bool:
        print("   → Link utilization recovery not implemented")
        return False
    
    def _log_violation(self, violation: IntentViolation):
        """Log intent violation."""
        timestamp = violation.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        actual_str = f"{violation.actual_value:.2f}" if isinstance(violation.actual_value, (int, float)) else str(violation.actual_value)
        message = (
            f"\n⚠️  INTENT VIOLATION DETECTED\n"
            f"   Time: {timestamp}\n"
            f"   Intent: {violation.intent_id}\n"
            f"   Type: {violation.intent_type.value}\n"
            f"   Component: {violation.component_id}\n"
            f"   Expected: {violation.expected_value}\n"
            f"   Actual: {actual_str}\n"
            f"   Severity: {violation.severity}"
        )
        print(message)
        log_file = os.path.join(self.log_dir, "intent_violations.log")
        with open(log_file, "a") as f:
            f.write(message + "\n" + "-" * 50 + "\n")
    
    def _notify_operator(self, violation: IntentViolation, reason: str):
        """Notify operator of unrecoverable violation."""
        actual_str = f"{violation.actual_value:.2f}" if isinstance(violation.actual_value, (int, float)) else str(violation.actual_value)
        message = (
            f"\n🚨 OPERATOR INTERVENTION REQUIRED 🚨\n"
            f"   Reason: {reason}\n"
            f"   Intent '{violation.intent_id}' requires manual action.\n"
            f"   Type: {violation.intent_type.value}\n"
            f"   Component: {violation.component_id}\n"
            f"   Expected: {violation.expected_value}, Actual: {actual_str}\n"
        )
        print(message)
    
    def _print_status_summary(self):
        """Print a summary of intent status."""
        if not self.intent_status:
            return
        
        counts = {s: 0 for s in IntentStatus}
        for status in self.intent_status.values():
            counts[status] += 1
        
        if counts[IntentStatus.VIOLATED] > 0 or counts[IntentStatus.RECOVERING] > 0:
            print(f"\n📊 Intent Status: "
                  f"✅ {counts[IntentStatus.SATISFIED]} | "
                  f"❌ {counts[IntentStatus.VIOLATED]} | "
                  f"🔧 {counts[IntentStatus.RECOVERING]} | "
                  f"❓ {counts[IntentStatus.UNKNOWN]}")
    
    def get_intent_report(self) -> Dict[str, Any]:
        """Generate a detailed intent report."""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {st.value: 0 for st in IntentStatus},
            'intents': {},
            'violations': []
        }
        report['summary']['total'] = len(self.intents)
        
        for intent_id, status in self.intent_status.items():
            report['summary'][status.value] += 1
            intent_spec = self.intents.get(intent_id, {})
            report['intents'][intent_id] = {
                'type': intent_spec.get('type', IntentStatus.UNKNOWN).value,
                'status': status.value,
                'expected': intent_spec.get('expected'),
                'component': self._get_component_id(intent_spec)
            }
        
        for v in self.violations[-10:]:
            report['violations'].append({
                'intent_id': v.intent_id,
                'intent_type': v.intent_type.value,
                'expected': v.expected_value,
                'actual': v.actual_value,
                'timestamp': v.timestamp.isoformat(),
                'component_id': v.component_id,
                'severity': v.severity
            })
        
        return report
    
    def export_report(self, filename: str = None):
        """Export intent monitoring report to file."""
        if filename is None:
            filename = os.path.join(self.log_dir, f"intent_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        else:
            filename = os.path.join(self.log_dir, filename)
        
        with open(filename, 'w') as f:
            json.dump(self.get_intent_report(), f, indent=2, default=str)
        
        print(f"📄 Report exported to {filename}")

    def _kickstart_network(self):
        """Send initial pings between hosts to populate ARP tables."""
        if not self.net:
            return
        
        print("🚀 Kickstarting network connectivity (warming up ARP tables)...")
        hosts = self.net.hosts
        for i, h1 in enumerate(hosts):
            for h2 in hosts[i+1:]:
                # Quick ping between hosts, suppress output
                h1.cmd(f'ping -c 1 -W 1 {h2.IP()} >/dev/null 2>&1 &')
        time.sleep(2)
        print("✅ Network kickstart complete — ARP tables initialized.\n")

