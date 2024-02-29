import unittest
import networkx as nx
from app import add_search_bearings, add_more_edge_bearing_info


class TestAddSearchBearings(unittest.TestCase):
    def test_invalid_search_bearing_type(self):
        search_list = add_search_bearings("invalid bearing")
        self.assertEqual(
            search_list, [], 'The search_list is does not handle invalid input correctly.')

    def test_valid_search_bearing(self):
        search_list = add_search_bearings(90)
        self.assertEqual(
            search_list, [90, 270, 180, 0], 'The search_list does not contain perpendicular bearings.')


class TestAddMoreEdgeBearingInfo(unittest.TestCase):
    def test_edges_bearing_rounding(self):
        G = nx.MultiDiGraph()
        G.add_edge(1, 2, bearing=45.6)
        add_more_edge_bearing_info(G)
        edge_data = G.get_edge_data(1, 2, 0)
        self.assertEqual(
            edge_data['rounded_bearing'], 46, 'The bearing was not rounded correctly')

    def test_edges_bearing_modulo(self):
        G = nx.MultiDiGraph()
        G.add_edge(1, 2, bearing=181.6)
        add_more_edge_bearing_info(G)
        edge_data = G.get_edge_data(1, 2, 0)
        self.assertEqual(
            edge_data['modulo_bearing'], 2, 'The bearing was not modulo correctly')


if __name__ == '__main__':
    unittest.main()
