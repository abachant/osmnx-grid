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


def get_parallel_bearings(bearing):
    """
    Take a bearing and return its parallel counterpart.

    Parameters
    ----------
    bearing : integer

    Returns
    -------
    parallel_bearings : list of integers

    """
    parallel_bearings = [bearing]
    parallel_bearings.append((bearing + 180) % 360)
    return parallel_bearings


def get_perpendicular_bearings(bearing):
    """
    Take a bearing and return its perpendicular counterparts.

    Parameters
    ----------
    bearing : integer

    Returns
    -------
    perpendicular_bearings : list of integers

    """
    perpendicular_bearings = []
    perpendicular_bearings.append((bearing + 90) % 360)
    perpendicular_bearings.append((bearing + 270) % 360)
    return perpendicular_bearings


def add_search_bearings(search_bearing, include_perpendicular=True):
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
    search_list : list of integers

    """

    search_list = []
    if isinstance(search_bearing, list):
        for i in search_bearing:
            parallel_bearings = get_parallel_bearings(i)
            search_list.extend(parallel_bearings)
            if include_perpendicular:
                perpendicular_bearings = get_perpendicular_bearings(i)
                search_list.extend(perpendicular_bearings)
    elif isinstance(search_bearing, int):
        search_list.extend(get_parallel_bearings(search_bearing))
        if include_perpendicular:
            perpendicular_bearings = get_perpendicular_bearings(search_bearing)
            search_list.extend(perpendicular_bearings)
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
