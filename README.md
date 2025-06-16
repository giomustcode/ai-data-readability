# script-tcc
<div align="justify">
Scripts em Python para análise textual e geração de relatórios de legibilidade, utilizando as métricas Flesch Reading Ease e Flesch-Kincaid Grade Level.

### Objetivo

Este projeto compara a acessibilidade textual das respostas fornecidas por redes neurais generativas (RNGs) com os textos oficiais (fact sheets) da Organização Mundial da Saúde (OMS/WHO), relacionados aos riscos da exposição ao asbesto (amianto).

A análise inclui:

- Contagem de palavras, sílabas e sentenças;
- Cálculo de índices de legibilidade;
- Geração de mapas de calor para visualização comparativa.

Para otimização dos resultados, foi utilizado como base unicamente a língua inglesa (sobretudo diante das limitações das RNGs e biblioteca textstat para o português).

### Contexto

Este estudo é parte do Trabalho de Conclusão de Curso (TCC) do MBA em Gestão da Engenharia de Software, com foco multidisciplinar.

O tema foi motivado por minha formação inicial (Direito), a relevância do assunto para a saúde pública e área jurídica, especialmente considerando o julgamento das ADIs 4066 e 6200 pelo STF, e busca também dar visibilidade à cidade de Minaçu/GO, historicamente atrelada à mineração de amianto no Brasil. 

### Tecnologias

Python 3.13.3, com as bibliotecas: *pandas, seaborn, matplotlib, textstat* e *openpyxl*.

### Visualizações

O projeto inclui geração de *heatmaps* para análise visual das métricas de legibilidade.

### Licença

Este repositório utiliza informações de acesso público (fact sheets da WHO/OMS e RNGs hospedadas via Web) e é parte de um trabalho acadêmico. Pode ser utilizado livremente para fins educacionais e de pesquisa. :)
</div>

