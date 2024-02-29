import osmnx as ox
import networkx as nx
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt

ox.settings.use_cache = True

# get bounding box for lower Manhattan and northwestern Brooklyn
north, south, east, west = 40.73, 40.64, -73.93, -74.04
G = ox.graph_from_bbox(north, south, east, west, network_type='drive_service')

ox.add_edge_bearings(G)


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

    search_list = []
    if type(search_bearing) == list:
        for i in search_bearing:
            search_list.append(i)
            if perpendicular == True:
                for t in range(3):
                    search_list.append((i+(90*(t+1))) % 360)
            else:
                pass
    elif type(search_bearing) == int:
        search_list.append(search_bearing)
        if perpendicular == True:
            for t in range(3):
                search_list.append((search_bearing+(90*(t+1))) % 360)
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

    for u, v, a in G.edges(data=True):
        if 'bearing' in a:
            edge_bearing = a['bearing']
            rounded_edge_bearing = int(round(edge_bearing))
            modulo_edge_bearing = rounded_edge_bearing % 90
            a['rounded_bearing'] = rounded_edge_bearing
            a['modulo_bearing'] = modulo_edge_bearing
        else:
            a['rounded_bearing'] = None
            a['modulo_bearing'] = None


search_bearings = add_search_bearings(172)
add_more_edge_bearing_info(G)


# plots network with a different color for each group of edges who share prependicular and parallel bearings
def plot_perpendicular_edges():
    ec = ox.plot.get_edge_colors_by_attr(
        G, 'modulo_bearing', na_color='none', cmap='gist_rainbow')
    fig, ax = ox.plot.plot_graph(
        G, node_size=0, edge_color=ec, edge_linewidth=2.5, edge_alpha=1)


# plots network with all edges of desired bearing(s) the color red('r') and all others the color blue('b')
def plot_specific_bearing_edges():
    ec = ['r' if data['rounded_bearing'] in search_bearings else 'b' for u,
          v, key, data in G.edges(keys=True, data=True)]
    fig, ax = ox.plot.plot_graph(
        G, node_size=0, edge_color=ec, edge_linewidth=2.5, edge_alpha=1)
