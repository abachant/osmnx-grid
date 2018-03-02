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

def add_perpendicular_bearings(search_bearing):
    for i in range(3):
        search_bearing.append((search_bearing[-1]+90)%360)
    return search_bearing

search_bearing = add_perpendicular_bearings([171])

for u,v,a in G.edges(data=True):
    a['rounded_bearing']=int(round(a['bearing']))
    a['modulo_bearing']=a['rounded_bearing']%90

ec = ['r' if data['rounded_bearing'] in search_bearing else 'b' for u, v, key, data in G.edges(keys=True, data=True)]
fig, ax = ox.plot_graph(G, node_size=0.3, edge_color=ec, edge_linewidth=2.5, edge_alpha=1)

# for u,v,a in G.edges(data=True):
#     print(a)
