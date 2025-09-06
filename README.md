### ai-data-readability

#### Segurança de Redes Neurais Generativas (LLMs) Aplicadas às Doenças Relacionadas à Exposição ao Asbesto

Este repositório contém os códigos, planilhas e resultados utilizados no Trabalho de Conclusão de Curso (TCC) que analisou a **acessibilidade e segurança da informação** de textos gerados por redes neurais generativas (RNGs) em comparação com documentos da Organização Mundial da Saúde (OMS) sobre exposição ao asbesto (amianto).

#### Objetivo 🔍
O objetivo do trabalho foi avaliar a legibilidade de textos em saúde ocupacional por meio das métricas Flesch Reading Ease (FRE) e Flesch-Kincaid Grade Level (FKG). A análise foi conduzida em dois ambientes distintos (Python e R) para verificar a robustez dos resultados e identificar limitações técnicas nas bibliotecas de cada linguagem.

#### Motivação e Relevância 
A escolha do tema foi principalmente feita por conta do constante crescimento de popularidade das fontes de IA como informação. 
Os LLMs mais populares são facilmente acessados via browser ou até mesmo via apps de redes sociais (Meta via WhatsApp, Grok via Twitter). Mas deve haver cautela na obtenção e utilização de informações sobre temas sensíveis, e saúde pública é um deles. <br>
A motivação pessoal da escolha do tema, especialmente direcionada para os [*fact sheets* sobre o Amianto publicados pela OMS](https://www.who.int/news-room/fact-sheets/detail/asbestos), se deu por conta do contexto ao qual cresci - a cidade onde ainda opera a maior mina de Amianto da América Latina, visando trazer visibilidade a um tema de relevância que quebra as barreiras regionais. <br>
Esta, inclusive, foi a motivação das ADIs 3406 e 3470 do STF no Brasil, tema do [TCC](https://drive.google.com/file/d/16uWC9KESXRM_itIwFiK9xQn24QT6OExL/view?usp=drive_link) da minha primeira graduação, em Direito.

##### Links úteis para compreensão sobre o tema:
###### Amianto no Brasil:
[# AMIANTO: Brasil é o terceiro maior exportador, mesmo com banimento](https://www.brasilmineral.com.br/noticias/brasil-e-o-terceiro-maior-exportador-mesmo-com-banimento) (2025) <br>
[# Banido no país, amianto volta a ser pauta no STF por causa de lei em Goiás](https://noticias.uol.com.br/politica/ultimas-noticias/2025/03/06/stf-volta-a-julgar-lei-que-permite-exploracao-de-amianto-em-goias.htm) (2025) <br>
[# Cancerígeno e banido em 60 países, amianto brasileiro continua a abastecer o mercado mundial](https://protecao.com.br/geral/cancerigeno-e-banido-em-60-paises-amianto-brasileiro-continua-a-abastecer-o-mercado-mundial/) (2024) <br>
[# Amianto em Goiás: entenda a disputa jurídica](https://g1.globo.com/go/goias/noticia/2020/11/23/amianto-em-goias-entenda-a-disputa-juridica.ghtml) (2020) <br>
[# Saúde ou emprego? O dilema do amianto, que fez Goiás desafiar STF](https://www.bbc.com/portuguese/brasil-49589925) (2019) <br>

###### Qualidade e acessibilidade de informações provenientes de LLMs (Science Direct):
[# Readability of Pediatric Otolaryngology Information: Comparing AI-Generated Content With Google Search Results](https://aao-hnsfjournals.onlinelibrary.wiley.com/doi/abs/10.1002/ohn.70011) *"ChatGPT4o-generated patient education materials are generally more difficult to read than Google-sourced content, especially for less complex conditions. **Given the importance of readability in patient education, AI-generated materials may require further refinement to improve accessibility without compromising accuracy**."* (2025) <br>
[# Evaluating the Quality and Readability of AI-Generated Ophthalmic Surgery Education: A Four Model Comparison](https://www.sciencedirect.com/science/article/pii/S2773160X25000212) (2025) <br>
[# A comparison of quality and readability of Artificial Intelligence chatbots in triage for head and neck cancer](https://www.sciencedirect.com/science/article/pii/S0196070925001139) (2025) <br>

#### Estrutura do Projeto

```
projeto_tcc/
├── dados/
│   ├── respostas_completas.xlsx          # planilha original com as respostas
│   ├── versao_finalPy.xlsx               # resultados calculados em Python
│   ├── versao_finalR.xlsx                # resultados calculados em R
│   └── versao_teste.xlsx                 # planilha auxiliar de teste
│
├── scripts/
│   ├── python/
│   │   ├── 00_teste_nonprintable.py      # limpeza de caracteres não imprimíveis
│   │   ├── 01_main_planilha.py           # leitura da planilha e pré-processamento
│   │   ├── 02_heatmap_readingease.py     # geração de heatmap FRE
│   │   ├── 03_heatmap_grade.py           # geração de heatmap FKG
│   │   ├── heatmap_flesch_reading_Py.png # gráfico gerado em Python (FRE)
│   │   └── heatmap_kincaid_grade_Py.png  # gráfico gerado em Python (FKG)
│   │
│   └── r/
│       ├── 00_teste_nonprintable.R       # limpeza de caracteres não imprimíveis
│       ├── 01_metricas_readability.R     # cálculo das métricas de legibilidade
│       ├── 02_heatmap_readingease.R      # geração de heatmap FRE
│       ├── 03_heatmap_kincaid.R          # geração de heatmap FKG
│       ├── heatmap_flesch_reading_R.png  # gráfico gerado em R (FRE)
│       └── heatmap_kincaid_grade_R.png   # gráfico gerado em R (FKG)

```

#### Requisitos

##### Python
Python 3.13.7 <br>
Bibliotecas: _pandas, matplotlib, seaborn, textstat, openpyxl_
<br>
Instalação via `pip install pandas matplotlib seaborn textstat openpyxl`

##### R
R 4.5.1 <br>
Pacotes: _readxl, tidyverse, quanteda, ggplot2, reshape2_
<br>
Instalação via `install.packages(c("readxl", "tidyverse", "quanteda", "ggplot2", "reshape2"))`

#### Como executar?

##### Python

Colocar a planilha respostas_completas.xlsx na pasta dados/.

###### OBS.: Essa planilha foi obtida inserindo perguntas em língua inglesa nos LLMs, baseadas no Fact Sheets correspondente da OMS, cuja fonte já foi linkada acima.

Executar:
python scripts/python/01_main_planilha.py <br>
python scripts/python/03_heatmap_grade.py <br>
python scripts/python/02_heatmap_readingease.py <br>

Os resultados serão salvos em planilhas .xlsx e gráficos .png.

##### R

Executar:
source("scripts/r/01_metricas_readability.R") <br>
source("scripts/r/03_heatmap_kincaid.R") <br>
source("scripts/r/02_heatmap_readingease.R") <br>

Os resultados serão salvos em planilhas .xlsx e gráficos .png.

#### Resultados

Heatmaps comparativos da legibilidade dos textos por pergunta e fonte (OMS vs RNGs).
Interpretação dos resultados utilizada no TCC.
###### OBS.: Os PNGs (heatmap_flesch_reading_*, heatmap_kincaid_grade_*) já estão incluídos no repositório como exemplos de saída, para facilitar a leitura de quem não quiser rodar o código.

#### Limitações

Existem diferenças metodológicas na contagem de sílabas entre Python e R, ocasionando pequenas variações nos valores absolutos.
Isso ocorre pois a linguagem Python, ao contrário do R, possui biblioteca com dicionários fonéticos como o `textstat` para palavras conhecidas, utilizando de regras heurísticas somente como "Plano B", uma espécie de *fallback*.
Sendo assim, a linguagem R possui, de certa forma, maior limitação metodológica neste estudo.
<br>
Dando um *zoom out* da metodologia técnica, as métricas clássicas de legibilidade não capturam nuances semânticas ou culturais do texto e do leitor, o que também deve se ter em mente ao realizar análises de dados neste sentido.

#### Licença

Uso acadêmico/educacional sem fins lucrativos. 
