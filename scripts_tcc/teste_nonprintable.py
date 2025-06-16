# esse script eh apenas para visualizacao de espacos non printable que poderiam afetar o resultado final
import pandas as pd

df = pd.read_excel("dados.xlsx");

def clean_and_report(cell):
    if pd.isnull(cell):
        return ""
    cleaned = str(cell).strip()

    non_printable = [c for c in cleaned if not c.isprintable()]
    if non_printable:
        print(f"non-printable characters found in cell: {non_printable}");
    if cleaned != str(cell):
        print(f"leading/trailing whitespace removed from cell: {cleaned}");
    return cleaned

for col in df.columns[1:]:
    df[col] = df[col].apply(clean_and_report)

df.to_excel("versao_teste.xlsx", index=False)
