# main.py

from network_manager import NetworkManager
from intent_parser import parse_intent_file
from mininet.log import setLogLevel, info

def execute_intents(network_manager, intents_data):
    """
    Processa a lista de intenções e as aplica na rede.
    """
    if not intents_data or 'intents' not in intents_data:
        info('*** Nenhuma intenção para executar.\n')
        return

    for intent in intents_data['intents']:
        if intent.get('type') == 'set_link_metric':
            params = intent.get('parameters', {})
            metric = params.get('metric')
            nodes = params.get('nodes')
            value = params.get('value')

            # Por enquanto, só implementamos a métrica 'delay'
            if metric == 'delay' and len(nodes) == 2:
                info(f"--- Processando Intenção ID: {intent.get('id')} ---\n")
                # NOTA: Esta lógica assume um link direto. Para TCCs mais avançados,
                # seria necessário encontrar o *caminho* entre os nós e aplicar
                # o delay em um ou mais links desse caminho.
                network_manager.apply_delay(nodes[0], nodes[1], value)
            else:
                info(f"*** Intenção com métrica '{metric}' ou # de nós != 2 não suportada ainda.\n")
        else:
            info(f"*** Tipo de intenção '{intent.get('type')}' não suportado.\n")

def verify_network_state(net_manager):
    """
    Executa comandos de verificação para confirmar se as intenções foram aplicadas.
    """
    info('*** Verificando o estado da rede (pings)...\n')
    net = net_manager.net
    
    # Ping sem delay artificial (deve ser rápido)
    h1, h2 = net.get('h1', 'h2')
    info(f'*** Ping: {h1.name} -> {h2.name} (delay de 50ms foi aplicado no caminho s1-s2)\n')
    # O ping precisa encontrar o caminho h1 -> s1 -> s2 -> h3, por exemplo.
    # Vamos pingar entre nós que *não* tiveram delay aplicado diretamente, mas cujo
    # caminho passa pelo link modificado.
    
    h1, h3 = net.get('h1', 'h3')
    # O caminho é h1-s1-s2-h3. A intenção aplica delay entre s1 e s2.
    # Portanto, este ping deve refletir o delay.
    info(f"Pinging {h3.name} from {h1.name} (caminho passa por s1-s2 com delay de 50ms)...\n")
    result = h1.cmd(f'ping -c 3 {h3.IP()}')
    print(result)

    h3, h4 = net.get('h3', 'h4')
    info(f"Pinging {h4.name} from {h3.name} (caminho h3-s2-h4, sem delay aplicado)...\n")
    result = h3.cmd(f'ping -c 3 {h4.IP()}')
    print(result)


if __name__ == '__main__':
    setLogLevel('info')

    # 1. Crie o gerenciador da rede
    network = NetworkManager()
    
    # Modificação para nosso exemplo: aplicar delay entre os switches
    # Crie o arquivo intent.json com este conteúdo:
    # {
    #   "intents": [{
    #     "id": "intent-sw-delay", "type": "set_link_metric",
    #     "parameters": { "nodes": ["s1", "s2"], "metric": "delay", "value": "50ms" }
    #   }]
    # }
    intent_file = 'intent.json'
    intents = parse_intent_file(intent_file)
    
    # 2. Inicie a rede
    network.start_network()

    # 3. Execute as intenções
    execute_intents(network, intents)
    
    # 4. Verifique se funcionou
    verify_network_state(network)
    
    # 5. Abra a CLI para exploração manual
    network.run_cli()
    
    # 6. Pare a rede ao sair da CLI
    network.stop_network()
