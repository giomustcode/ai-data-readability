library(readxl)
library(writexl)
library(dplyr)
library(tidyr)
library(stringr)
library(quanteda)
library(quanteda.textstats)

input <- "R/respostas_completas.xlsx"
output <- "versao_finalR.xlsx"

df <- readxl::read_excel(input)

# colunas de fontes (da 2ª em diante)
fontes <- names(df)[-1]

# helper: calcula métricas para um vetor de textos
calc_metrics <- function(txt_vec) {
  # corpus para readability
  corp <- quanteda::corpus(txt_vec)

  # Flesch Reading Ease
  fre  <- textstat_readability(corp, measure = "Flesch")
  # Flesch-Kincaid Grade
  fkg  <- textstat_readability(corp, measure = "Flesch.Kincaid")

  # contagem de palavras (tokens word)
  n_pal <- lengths(quanteda::tokens(txt_vec, what = "word", remove_punct = FALSE))
  # contagem de sentenças
  n_sent <- lengths(quanteda::tokens(txt_vec, what = "sentence"))

  # opcional: estimativa simples de sílabas por palavra (heurística)
  syllable_est <- function(word) {
    w <- tolower(gsub("[^a-z]", "", word))
    if (nchar(w) == 0) return(0L)
    # conta grupos de vogais (aproximação)
    s <- str_count(w, "[aeiouy]+")
    # correções comuns
    s <- s - as.integer(grepl("e$", w)) # silent e
    s <- ifelse(s < 1, 1L, s)
    as.integer(s)
  }
  n_sil <- vapply(txt_vec, function(t) {
    words <- unlist(str_extract_all(tolower(t), "[a-zA-Z]+"))
    sum(vapply(words, syllable_est, integer(1)))
  }, integer(1))

  tibble(
    n_palavras             = n_pal,
    n_sentencas            = n_sent,
    n_silabas_est          = n_sil,                 # opcional/heurística
    flesch_reading_ease    = fre$Flesch,
    flesch_kincaid_grade   = fkg$Flesch.Kincaid
  )
}

# para cada fonte, calcula e anexa colunas
for (fonte in fontes) {
  m <- calc_metrics(df[[fonte]] %>% replace_na(""))
  names(m) <- paste0(fonte, "_", names(m))
  df <- bind_cols(df, m)
}

writexl::write_xlsx(df, output)
