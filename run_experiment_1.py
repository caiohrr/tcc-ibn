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

# --- Dataset de Intenções ---
DATASET = [
    # Nível 1
    (1, 1, "Crie uma rede simples com dois hosts, h1 e h2, conectados a um único switch s1."),
    (2, 1, "Quero uma topologia linear onde o host A conecta ao switch 1, e o host B conecta ao switch 1."),
    (3, 1, "Conecte três hosts (h1, h2, h3) ao switch s1."),
    (4, 1, "Gere uma rede com um switch central s1 e quatro hosts conectados a ele."),
    (5, 1, "Crie uma topologia ponto-a-ponto conectando h1 diretamente a h2."),
    (6, 1, "Adicione dois switches, s1 e s2, interligados. Conecte h1 em s1 e h2 em s2."),
    (7, 1, "Uma rede simples contendo apenas o switch s1 e o host h1."),
    (8, 1, "Conecte o host 'servidor' ao switch 'core' e o host 'cliente' ao switch 'core'."),
    (9, 1, "Preciso de uma topologia com 2 hosts e 1 switch, sem configurações especiais."),
    (10, 1, "Defina uma rede básica chamada RedeTeste com versão 1.0 contendo h1, h2 e s1."),
    # Nível 2
    (11, 2, "Conecte h1 e h2 ao switch s1. O link entre h1 e s1 deve ter 100Mbps de banda."),
    (12, 2, "Crie uma rede onde h1 tem o IP 10.0.0.1/24 e h2 tem o IP 10.0.0.2/24, ambos ligados ao s1."),
    (13, 2, "Quero uma conexão entre h1 e s1 com um atraso de 10ms."),
    (14, 2, "Conecte h1 ao s1 com 50Mbps de banda e 5ms de delay."),
    (15, 2, "Defina uma topologia onde o link entre h1 e s1 tenha 1% de perda de pacotes."),
    (16, 2, "O host h1 (192.168.0.5) deve conectar ao s1. O link deve ter 1000Mbps."),
    (17, 2, "Configure uma rede com h1 e h2. A conexão do h1 deve ter 20ms de latência e a do h2 10ms."),
    (18, 2, "Conecte h1 a s1 com banda de 10Mbps e perda de 0.5%."),
    (19, 2, "Crie uma rede com h1 e h2. Todos os links devem ter 100Mbps de largura de banda."),
    (20, 2, "Host h1 com mac 00:00:00:00:00:01 conectado ao s1 com delay de 2ms."),
    # Nível 3
    (21, 3, "Crie uma rede monitorada. Ative o monitoramento com intervalo de 5 segundos e recuperação automática. Conecte h1 e h2 ao s1."),
    (22, 3, "O host h1 é um servidor pesado. Defina o uso máximo de CPU dele para 80% (0.8) e conecte-o ao s1."),
    (23, 3, "Preciso limitar a memória do h1 para 512MB. Conecte-o ao s1."),
    (24, 3, "Configure um controlador remoto c0 no IP 127.0.0.1 porta 6653 controlando o switch s1 que conecta h1 e h2."),
    (25, 3, "Topologia completa: ative o monitoramento a cada 10s. Host h1 (CPU máx 50%) conectado ao s1 (OpenFlow13) com link de 100Mbps."),
    (26, 3, "Conecte h1 e h2 ao s1. Configure um controlador remoto e habilite a recuperação de falhas no monitoramento."),
    (27, 3, "Crie uma rede para teste de VoIP: links com 100Mbps e 5ms de delay, monitoramento ativado e h1 com prioridade de CPU (max 0.9)."),
    (28, 3, "Switch s1 do tipo OVSKernelSwitch conectado a h1 e h2. Defina o monitoramento como ativado mas sem recuperação automática (apenas alerta)."),
    (29, 3, "Host h1 com 256MB de RAM e IP 10.0.0.1 conectado ao s1. O link deve ter perda de 2%."),
    (30, 3, "Ambiente de alta disponibilidade: Controlador c0, monitoramento agressivo (intervalo 2s, com recuperação), h1 e h2 conectados ao s1.")
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
        
        start_time = time.time()
        
        try:
            # Chamada à API
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2 # Baixa temperatura para maior determinismo no JSON
                ),
                contents=prompt
            )
            
            end_time = time.time()
            duration_ms = round((end_time - start_time) * 1000, 2)
            
            # Processamento da Saída
            raw_text = response.text
            json_text = clean_json_response(raw_text)
            
            # Validação Sintática Básica
            is_valid_json = False
            try:
                parsed_json = json.loads(json_text)
                is_valid_json = True
            except json.JSONDecodeError:
                is_valid_json = False
            
            # Salvar JSON individual
            filename = f"case_{case_id}_lvl{level}.json"
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
            
            # Pausa curta para evitar rate limiting agressivo (opcional)
            time.sleep(1)

        except Exception as e:
            print(f"[FALHA API] - {e}")
            results.append({
                "ID": case_id,
                "Nivel": level,
                "Prompt": prompt,
                "Tempo_ms": 0,
                "JSON_Valido": f"Erro API: {str(e)}",
                "Arquivo": "N/A"
            })

    # Gerar Relatório CSV
    csv_file = OUTPUT_DIR / "report_summary.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Nivel", "Prompt", "Tempo_ms", "JSON_Valido", "Arquivo", "Acuracia_Semantica", "Obs"])
        writer.writeheader()
        for res in results:
            # Adicionamos colunas vazias para preenchimento manual posterior
            res["Acuracia_Semantica"] = "" 
            res["Obs"] = ""
            writer.writerow(res)

    print(f"\n--- Experimento Concluído ---")
    print(f"JSONs salvos em: {JSON_DIR.absolute()}")
    print(f"Relatório salvo em: {csv_file.absolute()}")

if __name__ == "__main__":
    run_experiment()
