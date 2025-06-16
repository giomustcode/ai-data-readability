# importa bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# carrega a planilha
df = pd.read_excel("versao_final.xlsx")

# filtrar colunas reading ease
reading_cols = [col for col in df.columns if col.endswith('_flesch_reading_ease')]

# cria dataframe
heatmap_data = df[reading_cols]

# ajuste de nomes
heatmap_data.columns = [col.replace('_flesch_reading_ease', '') for col in heatmap_data.columns]

# renomeia indice vertical
heatmap_data.index = [f"Pergunta {i+1}" for i in range(len(heatmap_data))]

# cria heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="coolwarm_r", annot=True, linewidths=0.5)
plt.title("Flesch Reading Ease por pergunta e RNG")
plt.xlabel("Fonte (RNG)")
plt.ylabel("Pergunta")
plt.tight_layout()

# salva como imagem
plt.savefig("heatmap_flesch_reading2.png", dpi=300)

#mostra ao fim da execucao
plt.show()
