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

def add_search_bearings(search_bearing, perpendicular=True):
    """
    Take in a single bearing or list of bearings and returns it either as a list
    of itself if perpendicular is set to False or a list of itself and all its
    parallel and perpendicular bearings if perpendicular is kept set to True.
    Use for filtering objects by desired bearings.

    Parameters
    ----------
    search_bearing : list or integer
    perpendicular : boolean

    Returns
    -------
    search_list : list

    """

    search_list=[]
    if type(search_bearing) == list:
        for i in search_bearing:
            search.append(i)
            if perpendicular==True:
                for t in range(3):
                    search_list.append((i+(90*(t+1)))%360)
            else:
                pass
    elif type(search_bearing) == int:
        search_list.append(search_bearing)
        if perpendicular==True:
            for t in range(3):
                search_list.append((search_bearing+(90*(t+1)))%360)
        else:
            pass
    else:
        print("Please make sure the bearing(s) you are searching for are either an integer or a list of integers")
    return search_list

def add_more_edge_bearing_info(G):
    """
    Take compass bearing info from edges of a networkx multidigraph and adds
    new 2 attributes 'rounded_bearing' for their rounded bearing and
    'modulo_bearing' the rounded_bearing modulo 90, which allows edges to be
    organized into 90 distinct groups of parallel and perpendicular rounded
    bearings.
    Requires add_edge_bearings() first.

    Parameters
    ----------
    G : networkx multidigraph

    Returns
    -------
    G : networkx multidigraph
    """

    for u,v,a in G.edges(data=True):
        a['rounded_bearing']=int(round(a['bearing']))
        a['modulo_bearing']=a['rounded_bearing']%90

search_bearings = add_search_bearings(171, perpendicular=False)
add_more_edge_bearing_info(G)
print(search_bearings)
# ec = ox.get_edge_colors_by_attr(G, 'modulo_bearing', num_bins=5, cmap='rainbow', start=0, stop=1)
# fig, ax = ox.plot_graph(G, node_size=0.3, edge_color=ec, edge_linewidth=2.5, edge_alpha=1)

# ec = ['r' if data['rounded_bearing'] in search_bearings else 'b' for u, v, key, data in G.edges(keys=True, data=True)]
# fig, ax = ox.plot_graph(G, node_size=0.3, edge_color=ec, edge_linewidth=2.5, edge_alpha=1)
