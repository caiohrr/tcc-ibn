from Validator import Validator
from Executer import Executer

topo = Validator('Topology.json')
assert topo.STATUS == 0, f"Invalid topology (STATUS={topo.STATUS})"

exe = Executer(topo)
exe.executeTopology()   # opens the Mininet CLI
# TIP: after you exit the CLI, you should stop/cleanup (see note below)

