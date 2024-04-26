def mdgJaccard(G, n1:str, n2:str):
  '''
  Function to compute a Jaccard-styled similarity index between node couples in a NetworkX multiDiGraph, calculated as:
  (# of common predecessors + # of common successors) / (TOT# of predecessors of either node + TOT# of successors of either node)
  - - -
  Inputs:
    G: the NetworkX multiDiGraph object of reference
    n1, n2: IDs of the two nodes to compute the similarity of
  Outputs:
    Similarity: a Jaccard-styled similarity index for nodes in multiDiGraphs
  - - -
  '''

  import networkx as nx

  setIn1 = {(u, k) for u,v,k in G.in_edges(nbunch=[n1], keys=True)}
  setOut1 = {(v, k) for u,v,k in G.out_edges(nbunch=[n1], keys=True)}
  setIn2 = {(u, k) for u,v,k in G.in_edges(nbunch=[n2], keys=True)}
  setOut2 = {(v, k) for u,v,k in G.out_edges(nbunch=[n2], keys=True)}

  return (len(setIn1 & setIn2)+len(setOut1 & setOut2))/(len(setIn1 | setIn2)+len(setOut1 | setOut2))