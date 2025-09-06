import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# === configurações principais ===
INPUT_XLSX   = "versao_finalPy.xlsx"
SUFFIX       = "_flesch_kincaid_grade"
PREFERRED_ORDER = [
    "OMS", "Deep Seek", "ChatGPT 4.0", "ChatGPT Vision",
    "ScholarGPT", "Gemini", "Llama3", "Bing AI (Copilot)",
    "Google Palm", "Claude", "ReKa Core"
]
OUTFILE_PNG  = "heatmap_kincaid_grade.png"

# === leitura e preparo dos dados ===
df = pd.read_excel(INPUT_XLSX)

# seleciona as colunas que terminam com o sufixo esperado
fkg_cols = [c for c in df.columns if c.endswith(SUFFIX)]
if not fkg_cols:
    raise RuntimeError(
        f"Nenhuma coluna com sufixo '{SUFFIX}' encontrada em {INPUT_XLSX}."
    )

# dataframe somente com as colunas alvo e nomes limpos (sem o sufixo)
heatmap_data = df[fkg_cols].rename(columns=lambda x: x.replace(SUFFIX, ""))

# normalização leve de nomes (remove espaços extras nas pontas)
heatmap_data.columns = [c.strip() for c in heatmap_data.columns]

# aplica ordem preferida, mas mantendo só as colunas existentes
available = [c for c in PREFERRED_ORDER if c in heatmap_data.columns]
missing   = [c for c in PREFERRED_ORDER if c not in heatmap_data.columns]

if available:
    heatmap_data = heatmap_data[available]
    if missing:
        print("Aviso: as seguintes fontes preferidas não foram encontradas e serão ignoradas:", missing)
else:
    print("Aviso: nenhuma das fontes da ordem preferida foi encontrada; usando todas as colunas disponíveis.")
    # mantém a ordem original do arquivo
    available = heatmap_data.columns.tolist()

print("Colunas usadas no heatmap (FKG):", available)

# === plot ===
sns.set_theme(style="whitegrid")

vmin = heatmap_data.min().min()
vmax = heatmap_data.max().max()

plt.figure(figsize=(12, 6))
ax = sns.heatmap(
    heatmap_data,
    cmap="RdYlBu",          # FKG: valores altos (mais difícil) = quentes
    annot=True,
    fmt=".1f",
    linewidths=0.5,
    vmin=vmin, vmax=vmax,
    cbar_kws={"label": "FKG"}
)

ax.set_title("Flesch-Kincaid Grade Level por pergunta e RNG",
             loc="center", fontsize=16, fontweight="bold")
ax.set_xlabel("Fonte (RNG)")
ax.set_ylabel("Pergunta")

# y = perguntas numeradas 1..n
ax.set_yticklabels([str(i+1) for i in range(len(heatmap_data))], rotation=0)

# x = RNGs a 45°
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig(OUTFILE_PNG, dpi=300, bbox_inches="tight")
plt.show()
