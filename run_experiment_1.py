import os
import time
import json
import csv
import re
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- Configuração Inicial ---
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key não encontrada. Verifique seu arquivo .env")

client = genai.Client(api_key=api_key)

# Diretórios de saída
OUTPUT_DIR = Path("experiments/exp1")
JSON_DIR = OUTPUT_DIR / "json_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
JSON_DIR.mkdir(parents=True, exist_ok=True)

# --- System Instruction (Cópia exata do intent_translator.py para consistência) ---
SYSTEM_INSTRUCTION = """
You are a network topology assistant. Your task is to generate a new network topology in JSON format. This JSON file will be parsed by a custom Python script that defines a specific schema.

You must follow the schema rules outlined below. You must also use the "Full Schema Template" as a reference for the structure. You must only output the raw JSON, with no other text, comments, or explanations.

*You must not add a controller to the JSON unless it is explicitely defined.*

*You must not add connection parameters (e.g. Delay) unless explicitely defined.*

### Schema Rules

1.  **Top-Level Keys:**
    * `ID`: (String) A unique, simple identifier for the topology (e.g., "MyTestNet").
    * `VERSION`: (String) The topology version (e.g., "1.0").
    * `DESCRIPTION`: (String) A brief description of the topology.

2.  **`MONITORING` Block (Optional):**
    * This block controls the `IntentMonitor`.
    * `enabled`: (Boolean) `true` to run the monitor, `false` to disable.
    * `interval`: (Number) The time in seconds between monitoring checks.
    * `recovery_enabled`: (Boolean) `true` to allow the monitor to attempt recovery actions, `false` to only report issues.

3.  **`COMPONENTS` Block:**
    * This block defines all network devices.
    * **`HOSTS`:** (List)
        * `ID`: (String) Host identifier (e.g., "h1").
        * `IP`: (String, Optional) IP address with subnet (e.g., "10.0.0.1/24").
        * `MAC`: (String, Optional) MAC address.
        * `MAX_CPU`: (Number, Optional) Creates a CPU Intent. A float from 0.0 to 1.0 (e.g., 0.8 for 80%).
        * `MAX_RAM`: (Number, Optional) Creates a Memory Intent. An integer for max RAM in MB (e.g., 512).
    * **`SWITCHES`:** (List)
        * `ID`: (String) Switch identifier (e.g., "s1").
        * `TYPE`: (String, Optional) The class to use (e.g., "OVSSwitch", "OVSKernelSwitch").
        * `PARAMS`: (Object, Optional) Parameters for the switch (e.g., `{"PROTOCOLS": "OpenFlow13"}`).
    * **`CONTROLLERS`:** (List)
        * `ID`: (String) Controller identifier (e.g., "c0").
        * `TYPE`: (String, Optional) The class to use (e.g., "RemoteController").
        * `PARAMS`: (Object, Optional) Parameters (e.g., `{"IP": "127.0.0.1", "PORT": 6653}`).

4.  **`CONNECTIONS` Block:**
    * This block defines the links between components.
    * `ENDPOINTS`: (List) A list of two `ID` strings to link (e.g., `["h1", "s1"]`).
    * `PARAMS` (Optional): This object creates Link Intents.
        * `BANDWIDTH`: (Number) Link speed limit in Mbps (e.g., 100).
        * `DELAY`: (String) Link delay (e.g., "5ms", "100us").
        * `LOSS`: (Number) Packet loss percentage (e.g., 1 for 1%).

---
### Full Schema Template JSON (for reference)
```json
{
  "ID": "my_new_topology",
  "VERSION": "1.0",
  "DESCRIPTION": "A description of the new topology.",
  "MONITORING": {
    "enabled": true,
    "interval": 10,
    "recovery_enabled": true
  },
  "COMPONENTS": {
    "HOSTS": [
      {
        "ID": "h1",
        "IP": "10.0.0.1/24",
        "MAC": "00:00:00:00:00:01",
        "MAX_CPU": 0.5,
        "MAX_RAM": 256
      },
      {
        "ID": "h2",
        "IP": "10.0.0.2/24"
      }
    ],
    "SWITCHES": [
      {
        "ID": "s1",
        "TYPE": "OVSSwitch",
        "PARAMS": {
          "PROTOCOLS": "OpenFlow13"
        }
      }
    ],
    "CONTROLLERS": [
      {
        "ID": "c0",
        "TYPE": "RemoteController",
        "PARAMS": {
          "IP": "127.0.0.1",
          "PORT": 6653
        }
      }
    ]
  },
  "CONNECTIONS": [
    {
      "ENDPOINTS": ["h1", "s1"],
      "PARAMS": {
        "BANDWIDTH": 100,
        "DELAY": "5ms",
        "LOSS": 1
      }
    },
    {
      "ENDPOINTS": ["h2", "s1"],
      "PARAMS": {
        "BANDWIDTH": 50
      }
    }
  ]
}
"""

DATASET = [
    # Nível 1: Topologias Estruturadas (Médio Porte)
    (1, 1, "Crie uma topologia estrela com um switch central s1 e 8 hosts (h1 a h8) conectados a ele. Todas as conexões devem ter 100Mbps de banda."),
    (2, 1, "Gere uma rede linear com 3 switches (s1, s2, s3) conectados em série. Conecte 2 hosts em cada switch. Defina o delay de todos os links para 10ms."),
    (3, 1, "Preciso de uma rede com 10 hosts conectados ao switch s1. Os hosts h1 a h5 devem ter o IP na sub-rede 10.0.1.0/24 e os hosts h6 a h10 na sub-rede 10.0.2.0/24."),
    (4, 1, "Configure uma rede com 6 hosts e 1 switch. Habilite o monitoramento com intervalo de 5 segundos e recuperação automática para garantir conectividade."),
    (5, 1, "Crie uma rede com 5 hosts. O host h1 é o servidor e deve ter MAX_CPU de 1.0 (100%) e 1024MB de RAM. Os outros (h2-h5) devem ter CPU limitada a 20%."),
    (6, 1, "Topologia com dois switches, s1 e s2. Conecte h1, h2, h3 em s1 e h4, h5, h6 em s2. O link entre os switches deve ser de alta velocidade (1000Mbps)."),
    (7, 1, "Gere uma rede com 8 hosts ligados ao s1. Todos os links devem ter 1% de perda de pacotes simulada para teste de robustez."),
    (8, 1, "Conecte 4 hosts ao s1. Configure um controlador remoto no IP 192.168.56.1, porta 6633. Todos os hosts devem ter 512MB de RAM."),
    (9, 1, "Crie uma rede em anel com 4 switches (s1-s2-s3-s4-s1). Conecte um host em cada switch. Defina a banda dos links entre switches como 500Mbps."),
    (10, 1, "Rede simples com 10 hosts no switch s1. Porém, quero que o monitoramento esteja ativado apenas para reportar falhas, sem tentar recuperar (recovery_enabled false)."),

    # Nível 2: Segmentação e Regras Condicionais
    (11, 2, "Crie uma rede com 12 hosts conectados ao switch s1. Os primeiros 6 hosts são 'Legacy' e devem ter links de 10Mbps. Os últimos 6 são 'Modern' com links de 1Gbps."),
    (12, 2, "Gere uma topologia com 15 hosts divididos em 3 switches (5 por switch). O Switch 1 é o Core e seus hosts devem ter prioridade de CPU (80%). Os outros não têm limite."),
    (13, 2, "Topologia DataCenter: 2 switches Core (s1, s2) interligados. 8 hosts no s1 e 8 hosts no s2. Todos os hosts do s1 devem ter 2048MB de RAM. Os do s2 apenas 512MB."),
    (14, 2, "Crie uma rede com 20 hosts em um único switch. Os hosts com ID de h1 a h10 devem ter atraso de 5ms. Os hosts de h11 a h20 devem ter atraso de 50ms."),
    (15, 2, "Sistema de Vigilância: 10 câmeras (h1-h10) e 1 servidor (h11) no switch s1. As câmeras têm banda limitada a 5Mbps. O servidor tem banda de 1000Mbps e CPU livre."),
    (16, 2, "Rede com 16 hosts. Divida-os em 4 switches (s1, s2, s3, s4). Ative o monitoramento com intervalo agressivo (2s). Apenas os hosts do s1 precisam de limite de memória (256MB)."),
    (17, 2, "Conecte 10 hosts ao s1. Configure IPs sequenciais começando de 192.168.0.10 até 192.168.0.19. O link de todos deve ter 0.5% de perda."),
    (18, 2, "Simulação VoIP: 14 hosts no switch s1. Hosts pares devem ter configuração de Jitter simulado (Delay 20ms). Hosts ímpares devem ter conexão perfeita (Delay 1ms)."),
    (19, 2, "Rede de 18 hosts distribuídos em 2 switches. O link entre os switches deve ser gargalo (10Mbps). Os links dos hosts devem ser rápidos (100Mbps). Monitoramento ligado."),
    (20, 2, "Crie uma rede com 12 hosts. Hosts h1, h5 e h9 são gateways e precisam de MACs fixos (00:00:00:00:00:01, etc). O restante pode ser automático."),

    # Nível 3: Lógica Abstrata e Alta Escala
    (21, 3, "Gostaria de uma rede com um total de 30 hosts. Eles devem ser conectados em 3 switches, dividindo igualmente entre a quantidade de switches. No primeiro grupo, defina uma largura de banda maxima de 256 MB para todas as conexoes. No segundo, limite o cpu em 75%. Para o ultimo, as maquinas de numrero par devem ter sua memoria limitada em 100MB."),
    (22, 3, "Crie uma simulação de escritório com 40 hosts divididos em 4 departamentos (4 switches). Departamento A (h1-h10) precisa de alta CPU (90%). Departamento B (h11-h20) precisa de alta RAM (1024MB). Departamentos C e D são padrão. Todos conectados a um switch central s_core."),
    (23, 3, "Gere uma rede massiva com 50 hosts conectados a um switch s1. A cada 10 hosts, o link deve ter uma degradação diferente: 1-10 (0% loss), 11-20 (1% loss), 21-30 (2% loss), e assim por diante."),
    (24, 3, "Topologia em Árvore Binária: Switch Raiz conecta a 2 switches, que conectam a mais 2 cada (Total 7 switches). Coloque 3 hosts em cada switch da ponta (folhas). Total de 12 hosts. Monitoramento com recuperação ativado."),
    (25, 3, "Rede com 30 hosts. Os hosts com ID múltiplo de 5 (h5, h10, etc.) são servidores críticos: CPU 100%, RAM 2048MB e Link 1Gbps. O restante são clientes com CPU 20% e Link 10Mbps."),
    (26, 3, "Crie 3 grupos de 8 hosts (Total 24). Grupo 1 (Switch 1) é 'Voz' (Delay 2ms). Grupo 2 (Switch 2) é 'Dados' (Banda 1000Mbps). Grupo 3 (Switch 3) é 'IoT' (Banda 1Mbps). Conecte os 3 switches em anel."),
    (27, 3, "Desafio de endereçamento: 25 hosts no switch s1. O IP deve seguir a regra: 10.0.X.1, onde X é o número do host (ex: h1 = 10.0.1.1, h25 = 10.0.25.1). Limite a CPU de todos em 50%."),
    (28, 3, "Rede com 32 hosts divididos em 2 switches. No primeiro switch, todos os hosts devem ter MAC terminando em número par. No segundo switch, MAC terminando em ímpar. Monitoramento a cada 10s."),
    (29, 3, "Crie uma rede com 20 hosts onde a largura de banda decresce. h1 tem 100Mbps, h2 tem 95Mbps, h3 tem 90Mbps... até h20. Conectados ao s1."),
    (30, 3, "Cenário de Falha em Cascata: 30 hosts, 3 switches em cadeia. O switch do meio (s2) tem 10 hosts e deve ter seus links configurados com 50% de perda de pacotes (simulando falha). Os switches das pontas (s1, s3) funcionam normal.")
]

def clean_json_response(text):
    """Remove blocos de código markdown (```json ... ```) se existirem."""
    cleaned = re.sub(r"```json\s*", "", text)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()


def run_experiment():
    print(f"--- Iniciando Experimento 1: {len(DATASET)} Casos de Teste ---\n")
    
    results = []
    
    for case_id, level, prompt in DATASET:
        print(f"Processando Caso {case_id} (Nível {level})... ", end="", flush=True)
        
        # Loop de tentativa (Retry Logic)
        max_retries = 3
        retry_delay = 20  # Segundos para esperar se der erro 429
        
        for attempt in range(max_retries):
            start_time = time.time()
            try:
                # Chamada à API
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.1
                    ),
                    contents=prompt
                )
                
                # --- SUCESSO ---
                end_time = time.time()
                duration_ms = round((end_time - start_time) * 1000, 2)
                
                raw_text = response.text
                json_text = clean_json_response(raw_text)
                
                is_valid_json = False
                try:
                    parsed_json = json.loads(json_text)
                    is_valid_json = True
                except json.JSONDecodeError:
                    is_valid_json = False
                
                # Formatação correta com zeros (ex: case_01)
                filename = f"case_{case_id:02d}_lvl{level}.json"
                
                with open(JSON_DIR / filename, "w", encoding="utf-8") as f:
                    f.write(json_text)
                
                status = "SUCESSO" if is_valid_json else "ERRO JSON"
                print(f"[{status}] - {duration_ms}ms")
                
                results.append({
                    "ID": case_id,
                    "Nivel": level,
                    "Prompt": prompt,
                    "Tempo_ms": duration_ms,
                    "JSON_Valido": "Sim" if is_valid_json else "Não",
                    "Arquivo": filename
                })
                
                # Pausa de segurança entre sucessos (para não estourar o limite de novo)
                time.sleep(4) 
                break # Sai do loop de retry e vai para o próximo caso

            except Exception as e:
                # Se for erro de cota (429), espera e tenta de novo
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    if attempt < max_retries - 1:
                        print(f"\n   [COTA EXCEDIDA] Aguardando {retry_delay}s antes de tentar novamente...", end="", flush=True)
                        time.sleep(retry_delay)
                        print(" Retomando.")
                        continue # Tenta de novo
                    else:
                        print(f"[FALHA FINAL APÓS RETRIES] - {e}")
                else:
                    # Se for outro erro, falha imediatamente
                    print(f"[FALHA API] - {e}")
                
                # Registra o erro se esgotou as tentativas
                if attempt == max_retries - 1 or "429" not in str(e):
                    results.append({
                        "ID": case_id,
                        "Nivel": level,
                        "Prompt": prompt,
                        "Tempo_ms": 0,
                        "JSON_Valido": f"Erro API: {str(e)}",
                        "Arquivo": "N/A"
                    })
                    break

    # Gerar Relatório CSV (mantido igual)
    csv_file = OUTPUT_DIR / "report_summary.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Nivel", "Prompt", "Tempo_ms", "JSON_Valido", "Arquivo", "Acuracia_Semantica", "Obs"])
        writer.writeheader()
        for res in results:
            res["Acuracia_Semantica"] = "" 
            res["Obs"] = ""
            writer.writerow(res)

    print(f"\n--- Experimento Concluído ---")
    print(f"JSONs salvos em: {JSON_DIR.absolute()}")
    print(f"Relatório salvo em: {csv_file.absolute()}")


if __name__ == "__main__":
    run_experiment()
