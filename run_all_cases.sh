#!/bin/bash

# Diretório onde estão os JSONs de entrada
INPUT_DIR="experiments/exp1/json_outputs"

# Verifica se o diretório existe
if [ ! -d "$INPUT_DIR" ]; then
    echo "Erro: Diretório $INPUT_DIR não encontrado."
    exit 1
fi

echo "--- Iniciando geração em lote dos scripts Mininet ---"

# Loop por cada arquivo JSON que começa com "case_"
for json_file in "$INPUT_DIR"/case_*.json; do
    
    # 1. Pega apenas o nome do arquivo (remove o caminho)
    # Ex: case_01_lvl1.json
    filename=$(basename -- "$json_file")

    # 2. Extrai a parte "case_xx" (remove tudo a partir de "_lvl")
    # Ex: case_01
    case_name="${filename%%_lvl*}"

    # 3. Define o nome do arquivo de saída
    output_file="${case_name}.py"

    echo "Processando: $filename -> $output_file"

    # 4. Executa o main.py
    # Se o seu python for python3, mantenha assim. Se usar venv/uv, ajuste o comando.
    python3 main.py "$json_file" -o "$output_file" > /dev/null

    # Verifica se deu erro
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao gerar $output_file"
    fi
done

echo "--- Concluído! Arquivos .py gerados no diretório atual ---"
