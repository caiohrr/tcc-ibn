# intent_parser.py

import json

def parse_intent_file(filepath):
    """
    Lê um arquivo JSON de intenção e retorna seu conteúdo como um dicionário Python.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        # Validação básica
        if 'intents' not in data or not isinstance(data['intents'], list):
            raise ValueError("O arquivo de intenção deve conter uma chave 'intents' com uma lista de intenções.")
        return data
    except FileNotFoundError:
        print(f"Erro: Arquivo de intenção não encontrado em '{filepath}'")
        return None
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{filepath}' não é um JSON válido.")
        return None
    except ValueError as e:
        print(f"Erro de formato: {e}")
        return None
