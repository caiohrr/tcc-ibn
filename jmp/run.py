from Validator import Validator
from Executer import Executer
from Viewer import Viewer

# Load and validate topology
topo_input = input('Topology: ')
# print(f'{topo_input}.json')
topo = Validator(f'{topo_input}.json')
assert topo.STATUS == 0, f"Invalid topology (STATUS={topo.STATUS})"

# Launch viewer
# viewer = Viewer(topo.MNHOSTS, topo.MNSWITCHES, topo.MNOVSES, topo.MNCONTROLLER, topo.CONNECTIONS)
# viewer.view()

# If you still want to execute it in Mininet after closing the viewer:
exe = Executer(topo)
exe.executeTopology()
