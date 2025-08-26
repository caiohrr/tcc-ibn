import json

with open("/home/caio2409/Ufpr/TCC/tcc-ibn/Topology-simple_star.json") as json_file:
    json_data = json.load(json_file)


hosts_list = []
switches_list = []
controllers_list = []
ovsswitches_list = []
connections_list = []

# ID
topology_id = json_data["ID"].lower()


# COMPONENTS
components = json_data["COMPONENTS"]
hosts = components["HOSTS"]
for host in hosts:
    print(f"ID:{host["ID"]}")
    print(f"IP:{host["IP"]}")
    hosts_list.append(host)

switches = components["SWITCHES"]
for switch in switches:
    print(f"SWITCH:{switch}")
    switches_list.append(switch.lower())

controllers = components["CONTROLLERS"]
for controller in controllers:
    print(f"CONTROLLER:{controller}")
    controllers_list.append(controller.lower())

ovsswitches = components["OVSSWITCHES"]
for ovsswitch in ovsswitches:
    print(f"ID:{ovsswitch["ID"]}")
    print(f"CONTROLLER:{ovsswitch["CONTROLLER"]}")
    ovsswitches_list.append(ovsswitch)


# CONNECTIONS
connections = json_data["CONNECTIONS"]
for connection in connections:
    print(f"IN/OUT:{connection["IN/OUT"]}")
    print(f"OUT/IN:{connection["OUT/IN"]}")
    connections_list.append(connection)

print(hosts_list)
print(switches_list)
print(controllers_list)
print(ovsswitches_list)
print(connections_list)

with open("topology.py", "w+") as mn_file:
    mn_file.write(
"""
from mininet.net import Mininet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
"""
    )

    mn_file.write(f"def {topology_id}():\n\n")

    mn_file.write(f"\tnet = Mininet(controller=Controller, waitConnected=True)\n")

    
    mn_file.write(f"\tinfo('*** Adding {len(controllers_list)} controllers\\n')\n")
    for controller in controllers_list:
        mn_file.write(f"\t{controller} = net.addController('{controller}')\n")
    mn_file.write("\n")

    mn_file.write(f"\tinfo('*** Adding {len(hosts_list)} hosts\\n')\n")
    for host in hosts_list:
        id = host["ID"]
        ip = host["IP"]
        mn_file.write(f"\t{id} = net.addHost('{id}', ip='{ip}')\n")
    mn_file.write("\n")

    mn_file.write(f"\tinfo('*** Adding {len(switches_list)} switches\\n')\n")
    for switch in switches_list:
        mn_file.write(f"\t{switch} = net.addSwitch('{switch}')\n")
    mn_file.write("\n")

    mn_file.write(f"\tinfo('*** Creating {len(connections_list)} links\\n')\n")
    for connection in connections_list:
        in_out = connection["IN/OUT"]
        out_in = connection["OUT/IN"]
        mn_file.write(f"\tnet.addLink({in_out}, {out_in})\n")
    mn_file.write("\n")


    mn_file.write(f"\tinfo('*** Starting network\\n')\n")
    mn_file.write(f"\tnet.start()\n\n")

    mn_file.write(f"\tinfo('*** Running CLI\\n')\n")
    mn_file.write(f"\tCLI(net)\n\n")

    mn_file.write(f"\tinfo('*** Stopping network\\n')\n")
    mn_file.write(f"\tnet.stop()\n\n")

    mn_file.write(f"if __name__ == '__main__':\n")
    mn_file.write(f"\tsetLogLevel('info')\n")
    mn_file.write(f"\t{topology_id}()\n")
