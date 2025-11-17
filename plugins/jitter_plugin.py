import re
from main import MonitorRecoveryPlugin
from typing import Dict, Callable, Any

class JitterMonitorPlugin(MonitorRecoveryPlugin):
    """
    Plugin para monitorar Jitter.
    Isto NÃO requer mais hacks ou registro.
    """

    def get_name(self) -> str:
        return "JITTER_MONITOR"

    def get_version(self) -> str:
        return "1.0"

    def get_description(self) -> str:
        return "Adiciona monitoramento de Jitter (variação de atraso) às intenções de link."

    def get_check_functions(self) -> Dict[str, Callable]:
        """
        Mapeia a chave 'JITTER' (que deve estar no JSON) para a função.
        """
        return {
            'JITTER': self.check_jitter
        }

    def get_recovery_functions(self) -> Dict[str, Callable]:
        """
        Mapeia a chave 'JITTER' para a função de recuperação.
        """
        return {
            'JITTER': self.recover_jitter
        }

    # --- Funções de Lógica do Plugin ---

    def check_jitter(self, monitor: Any, intent: Dict) -> bool:
        """
        Verifica se o jitter da rede está abaixo do limite da intenção.
        Recebe a instância 'monitor' e a 'intent'.
        """
        try:
            host1_id, host2_id = intent['target']
            # O valor do JSON é o 'value'
            max_jitter = float(intent['value']) 
            
            # Acessa o 'net' através da instância do monitor
            host1 = monitor.net.get(host1_id)
            host2 = monitor.net.get(host2_id)

            result = host1.cmd(f'ping -c 5 {host2.IP()}')
            match = re.search(r'rtt .* = .*?/.*?/.*?/([\d.]+) ms', result)
            
            if match:
                avg_jitter = float(match.group(1))
                print(f"[INFO] (JITTER) {host1_id}-{host2_id} Jitter = {avg_jitter:.3f} ms. Max = {max_jitter} ms")
                return avg_jitter <= max_jitter
            else:
                print(f"[WARN] (JITTER) Não foi possível parsear o RTT para {host1_id}-{host2_id}.")
                return True # Não falha se o ping falhar (provavelmente é CONNECTIVITY)

        except Exception as e:
            print(f"[ERROR] (JITTER) Erro ao verificar jitter: {e}")
            return False

    def recover_jitter(self, monitor: Any, intent: Dict):
        """
        A recuperação agora recebe a instância 'monitor' e a 'intent'.
        """
        host1_id, host2_id = intent['target']
        value = intent['value']
        print(f"  -> WARNING: Jitter alto (>{value}ms) detectado no link {host1_id}-{host2_id}.")
        print(f"  -> ACTION: Nenhuma recuperação automática para Jitter. O operador deve investigar.")
