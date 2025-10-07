# Gerador de Scripts Mininet a partir de Topologias JSON

Este projeto oferece uma ferramenta para gerar automaticamente scripts Python para o emulador de redes [Mininet](http.mininet.org), a partir de arquivos de configuração declarativos no formato JSON. O objetivo é simplificar, padronizar e acelerar a criação de topologias de rede para simulações e experimentos.

O projeto foi desenvolvido a partir de conceitos explorados inicialmente em um trabalho relacionado, disponível no diretório `jmp/`.

## ✨ Funcionalidades

* **Definição Declarativa:** Descreva topologias de rede complexas de forma simples e intuitiva usando JSON.
* **Suporte aos Componentes Mininet:** Configure hosts, switches (Open vSwitch) e controladores remotos.
* **Parametrização de Links:** Especifique facilmente características dos links, como largura de banda (`bandwidth`), atraso (`delay`) e perda de pacotes (`loss`).
* **Geração Automática de Código:** Converta a definição JSON em um script Python (`.py`) standalone e executável.
* **Sistema de Plugins Extensível:** Adicione novas funcionalidades e componentes personalizados sem alterar o código principal.

## 📂 Estrutura do Projeto

```bash
/
├── jmp/                # Trabalho relacionado que serviu de base inicial
├── topologies/         # Diretório para armazenar os arquivos de topologia .json
├── plugins/            # Diretório onde ficam os plugins personalizados
├── main.py             # Script principal para gerar as topologias
├── README.md           # Este arquivo
├── pyproject.toml      # Definições do projeto e dependências (PEP 621)
└── uv.lock             # Arquivo de lock para dependências (gerado pelo uv)
```

## 🚀 Como Usar

### Pré-requisitos

* [Python 3.8+](https://www.python.org/)
* [Mininet](http://mininet.org/download/)
* Gerenciador de pacotes `uv` (recomendado): `pip install uv`

### Passos para Geração

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/caiohrr/tcc-ibn
   cd tcc-ibn
   ```

2. **Instale as dependências:**

   ```bash
   uv pip install -r requirements.txt
   ```

3. **Crie sua topologia:** Crie um arquivo `.json` dentro da pasta `topologies/` seguindo a estrutura detalhada na seção abaixo.

4. **Execute o gerador:**

   ```bash
   sudo -E uv run python main.py
   ```

   Ao ser solicitado, digite o nome do arquivo de topologia (ex: `03_simple_star_new`).

5. **Execute o script gerado:**

   ```bash
   sudo python <nome_do_script_gerado>.py
   ```

---

## 📄 Formato do Arquivo de Topologia JSON

O arquivo JSON é a base para a criação da rede. Ele descreve todos os componentes, conexões e plugins a serem utilizados.

### Estrutura Geral

```json
{
  "ID": "exemplo_topologia",
  "VERSION": "1.0",
  "DESCRIPTION": "Topologia de exemplo com dois hosts e um switch.",
  "COMPONENTS": {
    "HOSTS": [ { "ID": "h1", "IP": "10.0.0.1/24" }, { "ID": "h2" } ],
    "SWITCHES": [ { "ID": "s1", "TYPE": "OVSKernelSwitch" } ],
    "CONTROLLERS": [ { "ID": "c0", "TYPE": "RemoteController", "PARAMS": { "IP": "127.0.0.1", "PORT": 6653 } } ]
  },
  "CONNECTIONS": [ { "ENDPOINTS": ["h1", "s1"], "PARAMS": { "BANDWIDTH": 10 } } ],
  "PLUGINS": [ { "name": "SamplePlugin", "params": { "option": true } } ]
}
```

### Principais Campos

| Campo         | Tipo   | Obrigatório | Descrição                                                           |
| ------------- | ------ | ----------- | ------------------------------------------------------------------- |
| `ID`          | String | ❌           | Identificador da topologia.                                         |
| `VERSION`     | String | ❌           | Versão do arquivo.                                                  |
| `DESCRIPTION` | String | ❌           | Descrição da topologia.                                             |
| `COMPONENTS`  | Objeto | ✅           | Define hosts, switches, controladores e componentes personalizados. |
| `CONNECTIONS` | Array  | ✅           | Define links entre os componentes.                                  |
| `PLUGINS`     | Array  | ❌           | Lista de plugins aplicados à topologia.                             |

### COMPONENTS

O campo `COMPONENTS` pode conter as chaves `HOSTS`, `SWITCHES`, `CONTROLLERS` e componentes personalizados adicionados por plugins.

#### HOSTS

```json
"HOSTS": [ { "ID": "h1", "IP": "10.0.0.1/24", "MAC": "00:00:00:00:00:01" } ]
```

| Campo | Tipo     | Obrigatório | Descrição                                  |
| ----- | -------- | ----------- | ------------------------------------------ |
| `ID`  | String   | ✅           | Nome único do host.                        |
| `IP`  | String   | ❌           | Endereço IP.                               |
| `MAC` | String   | ❌           | Endereço MAC.                              |
| ...   | Qualquer | ❌           | Parâmetros extras passados ao `addHost()`. |

#### SWITCHES

```json
"SWITCHES": [ { "ID": "s1", "TYPE": "OVSKernelSwitch", "PARAMS": { "PROTOCOLS": "OpenFlow13" } } ]
```

| Campo    | Tipo   | Obrigatório | Descrição                                 |
| -------- | ------ | ----------- | ----------------------------------------- |
| `ID`     | String | ✅           | Identificador do switch.                  |
| `TYPE`   | String | ❌           | Tipo (`OVSKernelSwitch` ou `UserSwitch`). |
| `PARAMS` | Objeto | ❌           | Parâmetros extras.                        |

#### CONTROLLERS

```json
"CONTROLLERS": [ { "ID": "c0", "TYPE": "RemoteController", "PARAMS": { "IP": "127.0.0.1", "PORT": 6653 } } ]
```

| Campo    | Tipo   | Obrigatório | Descrição                                  |
| -------- | ------ | ----------- | ------------------------------------------ |
| `ID`     | String | ✅           | Identificador do controlador.              |
| `TYPE`   | String | ❌           | Tipo (`Controller` ou `RemoteController`). |
| `PARAMS` | Objeto | ❌           | Parâmetros extras (IP, PORT, etc.).        |

#### Componentes Personalizados

```json
"FIREWALLS": [ { "ID": "fw1", "RULES": ["allow tcp", "deny udp"] } ]
```

Requer um plugin registrado que implemente `ComponentPlugin` e declare o nome `FIREWALLS`.

### CONNECTIONS

```json
"CONNECTIONS": [ { "ENDPOINTS": ["h1", "s1"], "PARAMS": { "BANDWIDTH": 10, "DELAY": "5ms" } } ]
```

| Campo       | Tipo     | Obrigatório | Descrição                                                 |
| ----------- | -------- | ----------- | --------------------------------------------------------- |
| `ENDPOINTS` | Array(2) | ✅           | IDs dos elementos conectados.                             |
| `PARAMS`    | Objeto   | ❌           | Configurações do link (ex: `BANDWIDTH`, `DELAY`, `LOSS`). |

---

## 🔌 Arquitetura de Plugins

O sistema de plugins permite estender o gerador de scripts sem modificar o código principal. Ele é carregado automaticamente a partir do diretório `plugins/`.

### Tipos de Plugins

| Tipo                      | Classe Base             | Função Principal                                                                           |
| ------------------------- | ----------------------- | ------------------------------------------------------------------------------------------ |
| **TopologyPlugin**        | `TopologyPlugin`        | Modifica a topologia após o carregamento (ex: atribuição automática de IPs).               |
| **ScriptGeneratorPlugin** | `ScriptGeneratorPlugin` | Injeta código no script Mininet gerado (antes/depois da criação ou inicialização da rede). |
| **ComponentPlugin**       | `ComponentPlugin`       | Adiciona novos tipos de componentes (ex: NATs, Firewalls).                                 |

### Estrutura de um Plugin

Cada plugin deve herdar de uma das classes base e implementar os métodos obrigatórios:

```python
from typing import Dict, Any, List
from main import ScriptGeneratorPlugin, Topology

class MeuPlugin(ScriptGeneratorPlugin):
    def get_name(self):
        return "MeuPlugin"

    def get_version(self):
        return "1.0.0"

    def get_description(self):
        return "Exemplo de plugin personalizado"

    def generate_imports(self):
        return ["import os"]

    def generate_pre_network_code(self, topology: Topology, params: Dict[str, Any]):
        return ["# Código executado antes da criação da rede"]

    def generate_post_network_code(self, topology: Topology, params: Dict[str, Any]):
        return ["# Código executado após a criação da rede"]

    def generate_post_start_code(self, topology: Topology, params: Dict[str, Any]):
        return ["# Código executado após o início da rede"]
```

### Uso em Arquivo JSON

Adicione uma seção `PLUGINS` no seu arquivo de topologia:

```json
"PLUGINS": [
  {
    "name": "QoS",
    "params": {
      "enable_htb": true,
      "default_queue_size": 2000
    }
  },
  {
    "name": "Monitoring",
    "params": {
      "interval": 10,
      "duration": 300
    }
  }
]
```

Os nomes em `name` devem coincidir com o valor retornado por `get_name()` no código do plugin.

### Execução e Ciclo de Vida

1. **Carregamento:** O `PluginManager` procura automaticamente por plugins em `plugins/`.
2. **Execução:** Plugins são executados conforme sua categoria:

   * `ComponentPlugin` → durante o parsing dos componentes JSON.
   * `TopologyPlugin` → após o carregamento da topologia.
   * `ScriptGeneratorPlugin` → durante a geração do código Python (antes, depois e após iniciar a rede).
3. **Integração:** O código gerado pelos plugins é inserido no script Mininet resultante.

### Boas Práticas

* Use nomes únicos para evitar conflitos.
* Valide os parâmetros recebidos em `params`.
* Trate erros de forma segura e informativa.
* Documente claramente a função e versão do plugin.
* Teste seus plugins com diferentes topologias antes de uso em produção.

---

Com esse sistema, o projeto permite adicionar recursos avançados como **QoS**, **monitoramento de rede**, **NAT**, **balanceadores de carga** e muito mais — tudo sem modificar o núcleo da aplicação.
