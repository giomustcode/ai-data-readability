from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# paths
THIS = Path(__file__).resolve()
BASE = THIS.parent.parent.parent   # .../projeto_tcc
DADOS = BASE / "dados"
OUT   = BASE / "resultados"
OUT_FIG = OUT / "figuras"
OUT_TAB = OUT / "tabelas"
for p in [OUT, OUT_FIG, OUT_TAB]:
    p.mkdir(parents=True, exist_ok=True)

INPUT_XLSX = DADOS / "respostas_completas.xlsx"
OUT_XLSX   = OUT_TAB / "similaridades_OMS_vs_RNGs.xlsx"

print(f"[INFO] Lendo: {INPUT_XLSX}")
df = pd.read_excel(INPUT_XLSX)

#  helpers 
def normalize_text(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s).lower()
    s = re.sub(r"http\S+|www\.\S+", " ", s)                         # remove urls
    s = re.sub(r"[^a-z0-9á-úà-ùâ-ûã-õä-üç\s]", " ", s, flags=re.I)  # mantem letras alfa latino
    s = re.sub(r"\s+", " ", s).strip()
    return s

def tokenize(s: str):
    return normalize_text(s).split()

def cosine_sim_bow(a: str, b: str) -> float:
    ta, tb = tokenize(a), tokenize(b)
    if not ta and not tb:
        return np.nan
    ca, cb = {}, {}
    for t in ta: ca[t] = ca.get(t, 0) + 1
    for t in tb: cb[t] = cb.get(t, 0) + 1
    keys = set(ca) | set(cb)
    if not keys:
        return np.nan
    va = np.array([ca.get(k, 0) for k in keys], float)
    vb = np.array([cb.get(k, 0) for k in keys], float)
    na, nb = np.linalg.norm(va), np.linalg.norm(vb)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(va, vb) / (na * nb))

def jaccard_tokens(a: str, b: str) -> float:
    sa, sb = set(tokenize(a)), set(tokenize(b))
    if not sa and not sb:
        return np.nan
    un = sa | sb
    return float(len(sa & sb) / len(un)) if un else np.nan

def levenshtein_distance(a: str, b: str) -> int:
    a, b = normalize_text(a), normalize_text(b)
    n, m = len(a), len(b)
    if n == 0: return m
    if m == 0: return n
    prev = list(range(m + 1))
    curr = [0] * (m + 1)
    for i in range(1, n + 1):
        curr[0] = i
        ai = a[i - 1]
        for j in range(1, m + 1):
            cost = 0 if ai == b[j - 1] else 1
            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
        prev, curr = curr, prev
    return prev[m]

def levenshtein_similarity(a: str, b: str) -> float:
    a_n, b_n = normalize_text(a), normalize_text(b)
    L = max(len(a_n), len(b_n))
    if L == 0:
        return np.nan
    d = levenshtein_distance(a_n, b_n)
    return 1.0 - (d / L)

# id colunas 
cols = list(df.columns)
id_col = cols[0]
oms_candidates = [c for c in cols if c.strip().lower() == "oms"] or [c for c in cols if "oms" in c.strip().lower()]
if not oms_candidates:
    raise RuntimeError("Coluna 'OMS' não encontrada. Verifique cabeçalhos.")
oms_col = oms_candidates[0]

# rm colunas
def is_raw_text(c):
    cl = c.lower()
    return not any(tag in cl for tag in ["_flesch", "_kincaid", "silab", "palavr", "sentenc"])
rng_cols = [c for c in cols if c not in (id_col, oms_col) and is_raw_text(c)]

print(f"[INFO] Coluna OMS: {oms_col}")
print(f"[INFO] RNGs detectadas: {rng_cols}")

#  calcular métricas linha a linha 
def compute_table(metric_fn, name):
    out = pd.DataFrame({id_col: df[id_col]})
    for col in rng_cols:
        vals = [metric_fn(a, b) for a, b in df[[oms_col, col]].itertuples(index=False, name=None)]
        out[col] = vals
    return out

tbl_cos = compute_table(cosine_sim_bow, "cosine_bow")
tbl_jac = compute_table(jaccard_tokens, "jaccard_tokens")
tbl_lev = compute_table(levenshtein_similarity, "levenshtein_sim")

with pd.ExcelWriter(OUT_XLSX, engine="openpyxl") as w:
    tbl_cos.to_excel(w, index=False, sheet_name="cosine_bow")
    tbl_jac.to_excel(w, index=False, sheet_name="jaccard_tokens")
    tbl_lev.to_excel(w, index=False, sheet_name="levenshtein_sim")

print(f"[OK] Tabelas salvas: {OUT_XLSX}")

# heatmaps (matplotlib, 1 fig per graph) 
def save_heatmap(df_vals: pd.DataFrame, title: str, out_png: Path):
    data = df_vals.drop(columns=[id_col])
    fig, ax = plt.subplots(figsize=(12, 6))
    hm = ax.imshow(data.values, aspect='auto')  # colormap padrão
    ax.set_title(title)
    ax.set_xlabel("Fonte (RNG)")
    ax.set_ylabel("Pergunta")
    ax.set_xticks(range(data.shape[1]))
    ax.set_xticklabels(list(data.columns), rotation=45, ha='right')
    ax.set_yticks(range(data.shape[0]))
    ax.set_yticklabels([str(i+1) for i in range(data.shape[0])])
    fig.colorbar(hm, ax=ax)
    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Figura salva: {out_png}")

save_heatmap(tbl_cos, "Similaridade do Cosseno (BoW) – OMS vs RNGs", OUT_FIG / "heatmap_cosine_bow.png")
save_heatmap(tbl_jac, "Similaridade de Jaccard (tokens) – OMS vs RNGs", OUT_FIG / "heatmap_jaccard_tokens.png")
save_heatmap(tbl_lev, "Similaridade de Levenshtein (normalizada) – OMS vs RNGs", OUT_FIG / "heatmap_levenshtein_sim.png")
