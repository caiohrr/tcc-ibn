from Validator import Validator
from Translator import Translator
from Executer import Executer
from Viewer import Viewer
import sys

# O caminho para o arquivo de topologia JSON
json_file = "Topology.json"

# 1. Validar a topologia
print("Validando a topologia de " + json_file + "...")
topology = Validator(json_file)

# Verificar se a validacao foi bem-sucedida
if topology.STATUS != 0:
    print("Erro na validacao! Status: " + str(topology.STATUS))
    sys.exit(1)

print("Validacao concluida com sucesso.")

# 2. Traduzir a topologia para scripts Mininet (Arquivos Intermediarios)
print("\nGerando arquivos de traducao...")
translator = Translator(topology)
translator.lowLevelTranslation()
translator.midLevelTranslation()
print("Arquivos 'LLTOPOLOGY01.py' e 'MLTOPOLOGY01.py' gerados.")

# --- A partir daqui, escolha uma das acoes ---

# 3. Para EXECUTAR a topologia no Mininet (requer privilegios de root)
# Descomente as linhas abaixo para executar
# print("\nExecutando a topologia no Mininet...")
# executer = Executer(topology)
# executer.executeTopology()

# 4. Para VISUALIZAR a topologia
# Descomente as linhas abaixo para visualizar
print("\nIniciando o visualizador de topologia...")
viewer = Viewer(topology.MNHOSTS, topology.MNSWITCHES, topology.MNOVSES, topology.MNCONTROLLER, topology.CONNECTIONS)
viewer.view()
