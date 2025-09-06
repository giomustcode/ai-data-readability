suppressPackageStartupMessages({
  library(readxl)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(RColorBrewer)
})

input <- "versao_finalR.xlsx"
df <- readxl::read_excel(input)

fkg_cols <- grep("_flesch_kincaid_grade$", names(df), value = TRUE)
fontes_order <- sub("_flesch_kincaid_grade$", "", fkg_cols)

heat_df <- df |>
  select(all_of(fkg_cols)) |>
  rename_with(~ sub("_flesch_kincaid_grade$", "", .x)) |>
  mutate(Pergunta = row_number()) |>
  pivot_longer(-Pergunta, names_to = "Fonte", values_to = "FKG") |>
  mutate(
    Fonte = factor(Fonte, levels = fontes_order),
    Pergunta = factor(Pergunta, levels = seq_len(max(Pergunta)))
  )

fkg_min <- min(heat_df$FKG, na.rm = TRUE)
fkg_max <- max(heat_df$FKG, na.rm = TRUE)

p_fkg <- ggplot(heat_df, aes(x = Fonte, y = Pergunta)) +
  geom_tile(aes(fill = FKG)) +
  geom_text(aes(label = sprintf("%.1f", FKG)), size = 3) +
  scale_fill_gradientn(
    colours = brewer.pal(11, "RdYlBu"),
    limits  = c(fkg_min, fkg_max),
    name    = "FKG"
  ) +
  labs(
    title = "Flesch-Kincaid Grade Level por pergunta e RNG",
    x = "Fonte (RNG)", y = "Pergunta"
  ) +
  theme_minimal() +
  theme(
    plot.title  = element_text(hjust = 0.5, size = 16, face = "bold"),
    axis.text.x = element_text(angle = 45, hjust = 1),   # <<< 45 graus
    axis.title.x= element_text(size = 12, face = "bold"),
    axis.title.y= element_text(size = 12, face = "bold"),
    legend.title= element_text(size = 12, face = "bold")
  )

p_fkg <- p_fkg + scale_y_discrete(limits = rev(levels(heat_df$Pergunta)))

ggsave("heatmap_kincaid_grade_R.png", p_fkg, width = 12, height = 6, dpi = 300)
