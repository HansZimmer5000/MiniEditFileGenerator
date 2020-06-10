import unittest
import generator


class LinkTests(unittest.TestCase):

    def testCreateLink(self):
        self.assertEqual({"src": "a", "opts": {}, "dest": "b"},
                         generator.createLink("a", {}, "b"))

    def testCreateHostToAccessLinks(self):
        links = generator.createHostToAccessLinks(4)
        contains = [
            {"src": "h0", "opts": {}, "dest": "xs0"},
            {"src": "h1", "opts": {}, "dest": "xs1"},
            {"src": "h2", "opts": {}, "dest": "xs2"},
            {"src": "h8", "opts": {}, "dest": "xs8"},
            {"src": "h15", "opts": {}, "dest": "xs15"},
        ]

        not_contains = [
            {"src": "xs1", "opts": {}, "dest": "h1"},
        ]

        self.assertEqual(16, len(links))
        for elem in contains:
            self.assertTrue(elem in links, elem)

        for elem in not_contains:
            self.assertFalse(elem in links, elem)

    def testCreateAccessToAggregatorLinks(self):
        links = generator.createAccessToAggregatorLinks(4)
        contains = [
            {"src": "xs0", "opts": {}, "dest": "axs00"},
            {"src": "xs1", "opts": {}, "dest": "axs00"},
            {"src": "xs2", "opts": {}, "dest": "axs01"},
            {"src": "xs3", "opts": {}, "dest": "axs01"},

            {"src": "xs4", "opts": {}, "dest": "axs10"},
            {"src": "xs5", "opts": {}, "dest": "axs10"},
            {"src": "xs6", "opts": {}, "dest": "axs11"},
            {"src": "xs7", "opts": {}, "dest": "axs11"},

            {"src": "xs8", "opts": {}, "dest": "axs20"},
            {"src": "xs9", "opts": {}, "dest": "axs20"},
            {"src": "xs10", "opts": {}, "dest": "axs21"},
            {"src": "xs11", "opts": {}, "dest": "axs21"},

            {"src": "xs12", "opts": {}, "dest": "axs30"},
            {"src": "xs13", "opts": {}, "dest": "axs30"},
            {"src": "xs14", "opts": {}, "dest": "axs31"},
            {"src": "xs15", "opts": {}, "dest": "axs31"},
        ]

        self.assertEqual(16, len(links))
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

    def testCreateAggregatorToCoreLinks(self):
        links = generator.createAggregatorToCoreLinks(4)
        contains = [
            {"src": "acs00", "opts": {}, "dest": "cs0"},
            {"src": "acs00", "opts": {}, "dest": "cs1"},
            {"src": "acs01", "opts": {}, "dest": "cs1"},
            {"src": "acs01", "opts": {}, "dest": "cs2"},

            {"src": "acs10", "opts": {}, "dest": "cs2"},
            {"src": "acs10", "opts": {}, "dest": "cs3"},
            {"src": "acs11", "opts": {}, "dest": "cs3"},
            {"src": "acs11", "opts": {}, "dest": "cs0"},

            {"src": "acs20", "opts": {}, "dest": "cs0"},
            {"src": "acs20", "opts": {}, "dest": "cs1"},
            {"src": "acs21", "opts": {}, "dest": "cs1"},
            {"src": "acs21", "opts": {}, "dest": "cs2"},

            {"src": "acs30", "opts": {}, "dest": "cs2"},
            {"src": "acs30", "opts": {}, "dest": "cs3"},
            {"src": "acs31", "opts": {}, "dest": "cs3"},
            {"src": "acs31", "opts": {}, "dest": "cs0"},
        ]

        self.assertEqual(16, len(links))
        for elem in contains:
            self.assertTrue(elem in links, elem)

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

    def testCreateLinks(self):
        links = generator.createLinks(4)

        contains = [
            {"src": "h1", "opts": {}, "dest": "xs1"},
            {"src": "xs1", "opts": {}, "dest": "axs00"},
            {"src": "axs00", "opts": {}, "dest": "axs01"},
            {"src": "acs00", "opts": {}, "dest": "axs01"},
            {"src": "acs00", "opts": {}, "dest": "cs1"},
            {"src": "cs2", "opts": {}, "dest": "cs3"},
            {"src": "acs21", "opts": {}, "dest": "cs2"},
            {"src": "acs21", "opts": {}, "dest": "axs21"},
            {"src": "xs10", "opts": {}, "dest": "axs21"},
            {"src": "h10", "opts": {}, "dest": "xs10"},
        ]

        # Links are supposed to be always pointin to the right / inwards (host -> access -> aggregator -> core)
        not_contains = [
            {"src": "xs1", "opts": {}, "dest": "h1"},
            {"src": "axs00", "opts": {}, "dest": "xs1"},
            {"src": "axs00", "opts": {}, "dest": "acs00"},
            {"src": "cs0", "opts": {}, "dest": "acs00"},
        ]
    
        self.assertEqual(16+16+4*6+16+6, len(links))
        for elem in contains:
            self.assertTrue(elem in links, elem)

        for elem in not_contains:
            self.assertFalse(elem in links, elem)

if __name__ == "__main__":
    unittest.main()
