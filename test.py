import unittest
import generator


class LinkTests(unittest.TestCase):

    def testCreateLink(self):
        self.assertEqual({"src": "a", "opts": {}, "dest": "b"},
                         generator.createLink("a", {}, "b"))

    def testCreateInterCoreLinks(self):
        links = generator.createInterCoreLinks(4)
        contains = [
            {"src": "cs0", "opts": {}, "dest": "cs1"},
            {"src": "cs0", "opts": {}, "dest": "cs2"},
            {"src": "cs0", "opts": {}, "dest": "cs3"},
            {"src": "cs1", "opts": {}, "dest": "cs2"},
            {"src": "cs1", "opts": {}, "dest": "cs3"},
            {"src": "cs2", "opts": {}, "dest": "cs3"},

        ]

        self.assertEqual(6, len(links))
        for elem in contains:
            self.assertTrue(elem in links, elem)

    def testCreateInterAggregatorLinks(self):
        links = generator.createInterAggregatorLinks(4)
        contains = [
            {"src": "acs00", "opts": {}, "dest": "acs01"},
            {"src": "acs00", "opts": {}, "dest": "axs00"},
            {"src": "acs00", "opts": {}, "dest": "axs01"},

            #{"src": "acs01", "opts": {}, "dest": "acs00"},
            {"src": "acs01", "opts": {}, "dest": "axs00"},
            {"src": "acs01", "opts": {}, "dest": "axs01"},

            #{"src": "axs00", "opts": {}, "dest": "acs00"},
            #{"src": "axs00", "opts": {}, "dest": "acs01"},
            {"src": "axs00", "opts": {}, "dest": "axs01"},

            #{"src": "axs01", "opts": {}, "dest": "acs00"},
            #{"src": "axs01", "opts": {}, "dest": "acs01"},
            #{"src": "axs01", "opts": {}, "dest": "axs00"}


            {"src": "acs10", "opts": {}, "dest": "acs11"},
            {"src": "acs10", "opts": {}, "dest": "axs10"},
            {"src": "acs10", "opts": {}, "dest": "axs11"},
            {"src": "acs11", "opts": {}, "dest": "axs10"},
            {"src": "acs11", "opts": {}, "dest": "axs11"},
            {"src": "axs10", "opts": {}, "dest": "axs11"},

            {"src": "acs20", "opts": {}, "dest": "acs21"},
            {"src": "acs20", "opts": {}, "dest": "axs20"},
            {"src": "acs20", "opts": {}, "dest": "axs21"},
            {"src": "acs21", "opts": {}, "dest": "axs20"},
            {"src": "acs21", "opts": {}, "dest": "axs21"},
            {"src": "axs20", "opts": {}, "dest": "axs21"},

            {"src": "acs30", "opts": {}, "dest": "acs31"},
            {"src": "acs30", "opts": {}, "dest": "axs30"},
            {"src": "acs30", "opts": {}, "dest": "axs31"},
            {"src": "acs31", "opts": {}, "dest": "axs30"},
            {"src": "acs31", "opts": {}, "dest": "axs31"},
            {"src": "axs30", "opts": {}, "dest": "axs31"},
        ]

        self.assertEqual(24, len(links))
        for elem in contains:
            self.assertTrue(elem in links, elem)


if __name__ == "__main__":
    unittest.main()
