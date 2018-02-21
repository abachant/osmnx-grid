import osmnx as ox
import networkx as nx
import matplotlib.cm as cm
import matplotlib.colors as colors
import pandas as pd
ox.config(log_file=True, log_console=True, use_cache=True)
place = 'Lakeville, Massachusetts'
gdf = ox.gdf_from_place(place)
area = ox.project_gdf(gdf).unary_union.area
G = ox.graph_from_place(place, network_type='drive', simplify=False)

ox.utils.add_edge_bearings(G)
ec = ox.get_edge_colors_by_attr(G, attr='bearing')
ox.plot_graph(G, edge_color=ec)
# fig, ax = ox.plot_graph(G, node_color='w', node_edgecolor='k', node_size=0,
#                            node_zorder=3, edge_color=ec, edge_linewidth=3)
