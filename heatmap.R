install.packages("ggplot2")                               
library("ggplot2")  
install.packages("reshape")                         
library("reshape")

markers <- read.csv("/home/paola_user/Documenti/TERENCE.csv", header = TRUE, sep = "\t")
markers_melt <- melt(markers)                                           # Reorder data
head(markers_melt)

ggp <- ggplot(markers_melt, aes(X, variable)) +                           # Create heatmap with ggplot2
  geom_tile(aes(fill = value)) +
  scale_fill_gradient(low = "white", high = "red") +
  theme(text = element_text(size = 17)) #+ coord_fixed()
ggp

