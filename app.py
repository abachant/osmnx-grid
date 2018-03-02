import osmnx as ox
import networkx as nx
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd

ox.config(log_file=True, log_console=True, use_cache=True)

place = 'Mattapoisett, Massachusetts'
gdf = ox.gdf_from_place(place)
area = ox.project_gdf(gdf).unary_union.area
G = ox.graph_from_place(place, network_type='bike', simplify=False)

ox.utils.add_edge_bearings(G)

search_bearing = [220]

for u,v,a in G.edges(data=True):
    a['rounded_bearing']=int(round(a['bearing']))

ec = ['r' if data['rounded_bearing'] in search_bearing else 'b' for u, v, key, data in G.edges(keys=True, data=True)]
fig, ax = ox.plot_graph(G, node_size=0.3, edge_color=ec, edge_linewidth=2.5, edge_alpha=1)
