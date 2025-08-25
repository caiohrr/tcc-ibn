import json

with open("/home/caio2409/Ufpr/TCC/tcc-ibn/Topology.json") as json_file:
    json_data = json.load(json_file)


# ID
id = json_data["ID"]
print(id)


# COMPONENTS
components = json_data["COMPONENTS"]
hosts = components["HOSTS"]
for host in hosts:
    print(f"ID:{host["ID"]}")
    print(f"IP:{host["IP"]}")

switches = components["SWITCHES"]
for switch in switches:
    print(f"ID:{switch["ID"]}")
    print(f"SWITCH:{switch["SWITCH"]}")

controllers = components["CONTROLLERS"]
for controller in controllers:
    print(f"CONTROLLER:{controller}")

ovsswitches = components["OVSSWITCHES"]
for ovsswitch in ovsswitches:
    print(f"ID:{ovsswitch["ID"]}")
    print(f"CONTROLLER:{ovsswitch["CONTROLLER"]}")


# CONNECTIONS
connections = json_data["CONNECTIONS"]
for connection in connections:
    print(f"IN/OUT:{connection["IN/OUT"]}")
    print(f"OUT/IN:{connection["OUT/IN"]}")

