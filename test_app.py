import unittest
from app import add_search_bearings

class TestAddSearchBearings(unittest.TestCase):

    def test_invalid_search_bearing_type(self):
        search_list = add_search_bearings("invalid bearing")
        self.assertEqual(search_list, [], 'The search_list is does not handle invalid input correctly.')

    def test_valid_search_bearing(self):
        search_list = add_search_bearings(90)
        self.assertEqual(search_list, [90, 180, 270, 0], 'The search_list does not contain perpendicular bearings.')

if __name__ == '__main__':
    unittest.main()