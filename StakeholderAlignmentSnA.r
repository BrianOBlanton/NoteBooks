
library(igraph)

links <- read.csv("testedges.csv", header=T, as.is=T)

nodes <- read.csv(file="Rtestedges.csv", header=T, as.is=T)

links <- as.matrix(links)

dim(links)
dim(nodes)

net <- graph_from_data_frame(d=links, vertices=nodes, directed=T)

class(net)

net

plot(net, edge.arrow.size=.6,vertex.label=NA, vertex.size=3)








