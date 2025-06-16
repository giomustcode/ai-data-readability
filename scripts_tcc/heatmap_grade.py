import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# carrega a planilha
df = pd.read_excel("versao_final.xlsx")

# filtra colunas com os valores de Kincaid
kincaid_cols = [col for col in df.columns if col.endswith('_flesch_kincaid_grade')]

# cria dataframe 
kincaid_data = df[kincaid_cols]

# filtro de nomes
kincaid_data.columns = [col.replace('_flesch_kincaid_grade', '') for col in kincaid_data.columns]

# heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(kincaid_data, cmap="coolwarm", annot=True, linewidths=0.5)
plt.yticks(ticks=range(len(kincaid_data)), labels=[str(i+1) for i in range(len(kincaid_data))])
plt.title("Flesch-Kincaid Grade Level por pergunta e IA")
plt.xlabel("Fonte (IA)")
plt.ylabel("Pergunta")
plt.tight_layout()

# imagem
plt.savefig("heatmap_kincaid_grade.png", dpi=300)

# mostra o heatmap
plt.show()
