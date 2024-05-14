import unittest
import logging
from WordPathKeeperFile import WordPathKeeper

class MyTestCase(unittest.TestCase):

    def test_1_num_mismatched(self):
        my_WPK = WordPathKeeper()
        logging.info("Testing num mismatched.")
        # TODO: Write some appropriate tests to make sure that my_WPK.num_mismatched_letters() is working correctly.
        #  You might use "self.assertTrue()", "self.assertFalse()", "self.assertEqual()" or other methods that you have
        #  seen in previous unittests.


        pass

    def test_2_build_edges(self):
        my_WPK = WordPathKeeper()
        my_WPK.load_words_from_file("Four_letters_nodes_subset.txt")
        my_WPK.build_edges()

        # TODO: you should write this test!
        #  you might check that you get the correct number of edges; you might also check that a few word pairs, like
        #     ["line","tine"], are found in my_WPK.edges. You might also check that some words that are in the list but
        #     shouldn't be connected are NOT in my_WPK.edges.

        # Note: with the four letters nodes subset, you should get either 25 undirected edges or 50 directed edges.
        # Note: with the four letters nodes full file, you should get 19384 undirected edges or 38768 directed edges.


        pass

    def test_3_get_neighbors(self):
        my_WPK = WordPathKeeper()
        my_WPK.load_words_from_file("Four_letters_nodes.txt")
        my_WPK.build_edges()

        # TODO: you should write this test!
        # Here are a few things to try: search for the neighbors of a word near the start of your list of words, from
        #      the end of the list, and in the middle.

        # Note: for the subset, 'bins" should have 4 neighbors, 'bind' should have 3, and 'bots' should have 4
        # Note: for the full set of four-letter words, 'bins" should have 26 neighbors, 'bind' should have 14, and 'bots' should have 27
        # Note: for the full set of four-letter words, 'acid' should have 4 neighbors, and 'zoom' should have 7 neighbors.

        # You might also wish to hand check that the neighbors really are neighbors of the source words!

if __name__ == '__main__':
    unittest.main()
