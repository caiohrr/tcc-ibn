import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Carregar os dados
# Certifique-se de que seu arquivo é um CSV separado por vírgulas
try:
    df = pd.read_csv('report_summary.csv')
except:
    # Caso tenha problemas de encoding (comum em Excel/Windows)
    df = pd.read_csv('report_summary.csv', encoding='latin1')

# 2. Configurar o estilo visual
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 12))

# Tempo por Caso de Teste Individual (Barplot) ---
plt.subplot(2, 1, 2) # 2 linhas, 1 coluna, gráfico 2
# O parâmetro 'hue' colore as barras de acordo com o nível
sns.barplot(x='ID', y='Tempo_ms', hue='Nivel', data=df, palette="viridis", dodge=False)
plt.title('Tempo de Resposta por Caso de Teste (ID)', fontsize=14)
plt.ylabel('Tempo (ms)')
plt.xlabel('ID do Caso')
plt.legend(title='Nível', loc='upper right')

# Ajustar layout para não sobrepor textos
plt.tight_layout()

# Salvar ou mostrar
plt.savefig('analise_experimento_1.png')
plt.show()
