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

def add_perpendicular_bearings(search_bearing):
    """Take in a single bearing or list of bearings and return all of their parallel and perpendicular bearings in a list"""
    final_list=[]
    if type(search_bearing) == list:
        for i in search_bearing:
            final_list.append(i)
            for t in range(3):
                final_list.append((i+(90*(t+1)))%360)
    elif type(search_bearing) == int:
        final_list.append(search_bearing)
        for t in range(3):
            final_list.append((search_bearing+(90*(t+1)))%360)
    else:
        print("Please make sure the bearing(s) you are searching for are either an integer or a list of integers")
    return final_list

search_bearing = add_perpendicular_bearings(search_bearing=45)
def add_more_edge_bearing_info(G):
    #should go in ox.utils
    #requires add_edge_bearings() first
    for u,v,a in G.edges(data=True):
        a['rounded_bearing']=int(round(a['bearing']))
        a['modulo_bearing']=a['rounded_bearing']%90

# ec = ['r' if data['rounded_bearing'] in search_bearing else 'b' for u, v, key, data in G.edges(keys=True, data=True)]
# fig, ax = ox.plot_graph(G, node_size=0.3, edge_color=ec, edge_linewidth=2.5, edge_alpha=1)
print(search_bearing)
# for u,v,a in G.edges(data=True):
#     print(a)
