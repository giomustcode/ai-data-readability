import pandas as pd
import textstat

# carrega a planilha
df = pd.read_excel("respostas_completas.xlsx")

# define as colunas partindo da 2
fontes = df.columns[1:]

# analisa cada celula
for fonte in fontes:
    df[f'{fonte}_n_palavras'] = df[fonte].apply(lambda x: len(str(x).split()) if pd.notnull(x) else 0)
    df[f'{fonte}_n_sentencas'] = df[fonte].apply(lambda x: textstat.sentence_count(str(x)) if pd.notnull(x) else 0)
    df[f'{fonte}_n_silabas'] = df[fonte].apply(lambda x: textstat.syllable_count(str(x)) if pd.notnull(x) else 0)
    df[f'{fonte}_flesch_reading_ease'] = df[fonte].apply(lambda x: textstat.flesch_reading_ease(str(x)) if pd.notnull(x) else 0)
    df[f'{fonte}_flesch_kincaid_grade'] = df[fonte].apply(lambda x: textstat.flesch_kincaid_grade(str(x)) if pd.notnull(x) else 0)

# exportar a planilha com os resultados
df.to_excel("versao_finalPy.xlsx", index=False)
