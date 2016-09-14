library(reshape2)
library(ggplot2)

setwd("~/Desktop/P1")
df <- read.csv('stroopdata.csv')

summary(df)

mean(df$Congruent)
mean(df$Incongruent)

sd(df$Congruent)
sd(df$Incongruent)

df_long <- melt(df)
names(df_long) <- c("condition", "time")
head(df_long)

ggplot(data = df_long, aes(x = time, color = condition)) +
  geom_density()


df$diff <- df$Congruent - df$Incongruent
mean(df$diff)
sd(df$diff)

t.test(df$Congruent, df$Incongruent, paired=TRUE)
