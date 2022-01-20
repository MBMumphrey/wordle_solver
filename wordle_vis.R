library(readr)
library(dplyr)
library(ggplot2)

positions <- read_csv("Projects/wordle/positions.txt") %>%
  group_by(letter) %>%
  mutate(freq = count/sum(count))

position_plot <- ggplot(data = positions,
                        aes(x = position, y = freq)) +
  geom_bar(stat = "identity") +
  ylab("Frequency") +
  xlab("Position") +
  facet_wrap(~ letter, ncol = 4)

position_plot

ggsave("Projects/wordle/position_plot.png", plot = position_plot,
       width = 5, height = 8, units = "in")
