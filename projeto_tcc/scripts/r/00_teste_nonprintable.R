library(readxl)
library(writexl)
library(dplyr)
library(stringr)

# paths
input  <- "R/respostas_completas.xlsx"
output <- "versao_teste.xlsx"

# carrega
df <- readxl::read_excel(input)

# função de limpeza e relatório (stdout)
clean_and_report <- function(x) {
  if (is.na(x)) return("")
  s <- as.character(x)
  s_trim <- str_trim(s)

  # detecta não-imprimíveis (qualquer char fora de [:print:] ou \t\r\n)
  non_printable <- str_extract_all(s_trim, "[^[:print:]\t\r\n]")[[1]]
  if (length(non_printable) > 0) {
    message("non-printable characters found: ",
            paste(unique(non_printable), collapse = " "))
  }
  if (!identical(s, s_trim)) {
    message("leading/trailing whitespace removed: '", s_trim, "'")
  }
  s_trim
}

# aplica da 2ª coluna em diante (1ª é a pergunta)
cols <- names(df)[-1]
df[cols] <- lapply(df[cols], function(col) vapply(col, clean_and_report, ""))

# salva
writexl::write_xlsx(df, output)