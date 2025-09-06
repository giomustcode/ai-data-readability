suppressPackageStartupMessages({
  library(readxl)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(RColorBrewer)
})

input <- "versao_finalR.xlsx"
df <- readxl::read_excel(input)

fre_cols <- grep("_flesch_reading_ease$", names(df), value = TRUE)
fontes_order <- sub("_flesch_reading_ease$", "", fre_cols)

heat_df <- df |>
  select(all_of(fre_cols)) |>
  rename_with(~ sub("_flesch_reading_ease$", "", .x)) |>
  mutate(Pergunta = row_number()) |>
  pivot_longer(-Pergunta, names_to = "Fonte", values_to = "FRE") |>
  mutate(
    Fonte = factor(Fonte, levels = fontes_order),
    Pergunta = factor(Pergunta, levels = seq_len(max(Pergunta)))
  )

fre_min <- min(heat_df$FRE, na.rm = TRUE)
fre_max <- max(heat_df$FRE, na.rm = TRUE)

p_fre <- ggplot(heat_df, aes(x = Fonte, y = Pergunta)) +
  geom_tile(aes(fill = FRE)) +
  geom_text(aes(label = sprintf("%.1f", FRE)), size = 3) +
  scale_fill_gradientn(
    colours = rev(brewer.pal(11, "RdYlBu")),
    limits  = c(fre_min, fre_max),
    name    = "FRE"
  ) +
  labs(
    title = "Flesch Reading Ease por pergunta e RNG",
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

p_fre <- p_fre + scale_y_discrete(limits = rev(levels(heat_df$Pergunta)))

ggsave("heatmap_flesch_reading_R.png", p_fre, width = 12, height = 6, dpi = 300)

