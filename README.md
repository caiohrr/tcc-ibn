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
  "intent": {
    "name": "low_delay_communication",
    "source": {
      "host": "h1",
      "ip": "10.0.0.1"
    },
    "destination": {
      "host": "h2",
      "ip": "10.0.0.2"
    },
    "constraint": {
      "delay": {
        "max": 100,
        "unit": "ms"
      }
    },
    "action": "allow",
    "traffic_type": "all"
  }
}
```
