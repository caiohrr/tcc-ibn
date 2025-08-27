# tcc-ibn
TCC de IBN.

# Como Rodar o Programa
```bash
sudo -E uv run python run.py
```

## KPIs
Métricas para medir o assurance:
- [X] Delay
- [X] Throughput
- [X] Link Utilisation
- [ ] Packet Loss
- [ ] Packet Size
- [X] No of Failures
- [X] Comp. Res. Utilisation

## Exemplo de Intent (JSON)
```json
{
    "ID": "SimpleStar_Robust",
    "VERSION": "1.0",
    "DESCRIPTION": "Uma topologia estrela com parâmetros de link e recursos de host.",
    "COMPONENTS": {
        "HOSTS": [
            {
                "ID": "h1",
                "IP": "10.0.0.1/24",
                "MAC": "00:00:00:00:00:01"
            },
            {
                "ID": "h2",
                "IP": "10.0.0.2/24",
                "MAC": "00:00:00:00:00:02"
            },
            {
                "ID": "h3",
                "IP": "10.0.0.3/24",
                "MAC": "00:00:00:00:00:03"
            },
            {
                "ID": "h4",
                "IP": "10.0.0.4/24",
                "MAC": "00:00:00:00:00:04"
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
            "PARAMS": { "BANDWIDTH": 100, "DELAY": "5ms" }
        },
        {
            "ENDPOINTS": ["h2", "s1"],
            "PARAMS": { "BANDWIDTH": 50, "DELAY": "10ms", "LOSS": 1 }
        },
        {
            "ENDPOINTS": ["h3", "s1"],
            "PARAMS": { "BANDWIDTH": 100, "DELAY": "5ms" }
        },
        {
            "ENDPOINTS": ["h4", "s1"],
            "PARAMS": { "BANDWIDTH": 80, "DELAY": "7ms" }
        }
    ]
}
```

## Hosts
```json
"HOSTS": [
    {
        "ID": "h1",
        "IP": "10.0.0.1/24",
        "MAC": "00:00:00:00:00:01",
        "RESOURCES": {
            "CPU": 0.5,
            "MEMORY": "512m" # Precisa usar Containernet para gerenciar memória
        },
        "SCHEDULER": "cfs"
    }
]
```

## Connections
```json
"CONNECTIONS": [
    {
        "ENDPOINTS": ["h1", "s1"],
        "PARAMS": {
            "BANDWIDTH": 10,
            "DELAY": "10ms",
            "LOSS": 1,
            "MAX_QUEUE_SIZE": 1000,
            "JITTER": "1ms"
        }
    }
]
```

## Switches
```json
"SWITCHES": [
    {
        "ID": "s1",
        "TYPE": "OVSSwitch",
        "PARAMS": {
            "PROTOCOLS": "OpenFlow13",
            "DPCTL_LISTEN_PORT": 6634
        }
    },
    {
        "ID": "s2",
        "TYPE": "LinuxBridge"
    }
]
```

## Controllers
```json
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
```
