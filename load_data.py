import networkx as nx
import pickle
import pandas as pd

# Script for generating networkx graphs from a given dataset or loading them from pickled versions if they already exist
all_courts = ['cjeu', 'echr', 'ussc']
chosen_court = 'cjeu'

with open('Data/'+chosen_court + '-full-nodes.csv') as f:
	nodes = pd.read_csv(f, sep=' ').transpose()

with open('Data/'+chosen_court+'-full-edges.csv') as f:
	edges = pd.read_csv(f, sep=' ')

G = nx.DiGraph()

# Add all the nodes from the CSV file, using their node id as identifier including all metadata except the node_id which is already used
G.add_nodes_from([(v['node_id'], {k: vv for (k,vv) in v.iteritems() if k != 'node_id'}) for v in nodes.to_dict().itervalues()])
G.add_edges_from([(edge[1]['source_id'], edge[1]['target_id']) for edge in edges.iterrows()])

def jaccard_predictions(G):
    """
    Create a ranked list of possible new links based on the Jaccard similarity,
    defined as the intersection of nodes divided by the union of nodes
    
    parameters
    G: Directed or undirected nx graph
    returns
    list of linkbunches with the score as an attribute
    """
    potential_edges = []
    for non_edge in nx.non_edges(G):
        u = set(G.neighbors(non_edge[0]))
        v = set(G.neighbors(non_edge[1]))
        if len(u.union(v)) == 0:
            s = 0.0
        else:
            s = (1.0*len(u.intersection(v)))/len(u.union(v))
        non_edge = non_edge + ({'score': s},)
        potential_edges.append(non_edge)
        
    return potential_edges