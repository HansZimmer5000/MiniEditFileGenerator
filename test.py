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

        checkList(links, 16, contains, not_contains, self)

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

        checkList(links, 16, contains, [], self)

    def testCreateInterAggregatorLinks(self):
        links = generator.createInterAggregatorLinks(4)
        contains = [
            {"src": "acs00", "opts": {}, "dest": "acs01"},
            {"src": "acs00", "opts": {}, "dest": "axs00"},
            {"src": "acs00", "opts": {}, "dest": "axs01"},

            # {"src": "acs01", "opts": {}, "dest": "acs00"},
            {"src": "acs01", "opts": {}, "dest": "axs00"},
            {"src": "acs01", "opts": {}, "dest": "axs01"},

            # {"src": "axs00", "opts": {}, "dest": "acs00"},
            # {"src": "axs00", "opts": {}, "dest": "acs01"},
            {"src": "axs00", "opts": {}, "dest": "axs01"},

            # {"src": "axs01", "opts": {}, "dest": "acs00"},
            # {"src": "axs01", "opts": {}, "dest": "acs01"},
            # {"src": "axs01", "opts": {}, "dest": "axs00"}


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

        checkList(links, 24, contains, [], self)

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

        checkList(links, 16, contains, [], self)

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

        checkList(links, 6, contains, [], self)

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

        checkList(links, 16+16+4*6+16+6, contains, not_contains, self)


class NodeTests(unittest.TestCase):
    def testCreateHosts(self):
        hosts = generator.createHosts(16)

        contains = [
            {
                "number": "0",
                "opts": {
                    "hostname": "h0",
                    "nodeNum": 0,
                    "sched": "host"
                },
                "x": "100",
                "y": "100"
            },
            {
                "number": "1",
                "opts": {
                    "hostname": "h1",
                    "nodeNum": 1,
                    "sched": "host"
                },
                "x": "100",
                "y": "140"
            },
            {
                "number": "15",
                "opts": {
                    "hostname": "h15",
                    "nodeNum": 15,
                    "sched": "host"
                },
                "x": "100",
                "y": "700"
            }
        ]

        not_contains = [
            {
                "number": "16",
                "opts": {
                    "hostname": "16",
                                "nodeNum": 16,
                                "sched": "host"
                },
                "x": "100",
                "y": "740"
            }
        ]

        checkList(hosts, 16, contains, not_contains, self)

    def testCreateSwitches(self):
        switches = generator.createSwitches(4)

        core_contains = [
            {
                "number": "0",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "1",
                    "hostname": "cs0",
                    "nodeNum": 0,
                    "switchType": "default"
                },
                "x": "500",
                "y": "100"
            },            {
                "number": "15",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "24",
                    "hostname": "axs31",
                    "nodeNum": 35,
                    "switchType": "default"
                },
                "x": "300",
                "y": "380"
            }
        ]
        
        core_not_contains = []

        checkList(switches, 4+16+16, core_contains, core_not_contains, self)

    def testCreateCoreSwitches(self):
        (core_switches, global_next_switch_num) = generator.createCoreSwitches(4, 0)

        core_contains = [
            {
                "number": "0",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "1",
                    "hostname": "cs0",
                    "nodeNum": 0,
                    "switchType": "default"
                },
                "x": "500",
                "y": "100"
            },
            {
                "number": "1",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "2",
                    "hostname": "cs1",
                    "nodeNum": 1,
                    "switchType": "default"
                },
                "x": "500",
                "y": "140"
            },
            {
                "number": "2",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "3",
                    "hostname": "cs2",
                    "nodeNum": 2,
                    "switchType": "default"
                },
                "x": "500",
                "y": "180"
            },
            {
                "number": "3",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "4",
                    "hostname": "cs3",
                    "nodeNum": 3,
                    "switchType": "default"
                },
                "x": "500",
                "y": "220"
            }
        ]
        core_not_contains = []

        self.assertEqual(4, global_next_switch_num)
        checkList(core_switches, 4, core_contains, core_not_contains, self)

        (core_switches, global_next_switch_num) = generator.createCoreSwitches(4, 4)

        core_contains = [
            {
                "number": "0",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "5",
                    "hostname": "cs0",
                    "nodeNum": 4,
                    "switchType": "default"
                },
                "x": "500",
                "y": "100"
            },
            {
                "number": "1",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "6",
                    "hostname": "cs1",
                    "nodeNum": 5,
                    "switchType": "default"
                },
                "x": "500",
                "y": "140"
            },
            {
                "number": "2",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "7",
                    "hostname": "cs2",
                    "nodeNum": 6,
                    "switchType": "default"
                },
                "x": "500",
                "y": "180"
            },
            {
                "number": "3",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "8",
                    "hostname": "cs3",
                    "nodeNum": 7,
                    "switchType": "default"
                },
                "x": "500",
                "y": "220"
            }
        ]
        core_not_contains = []

        self.assertEqual(8, global_next_switch_num)
        checkList(core_switches, 4, core_contains, core_not_contains, self)

    def testCreateAccessSwitches(self):
        (access_switches, global_next_switch_num) = generator.createAccessSwitches(4, 0)

        core_contains = [
            {
                "number": "0",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "1",
                    "hostname": "xs0",
                    "nodeNum": 0,
                    "switchType": "default"
                },
                "x": "200",
                "y": "100"
            },
            {
                "number": "1",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "2",
                    "hostname": "xs1",
                    "nodeNum": 1,
                    "switchType": "default"
                },
                "x": "200",
                "y": "140"
            },
            {
                "number": "2",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "3",
                    "hostname": "xs2",
                    "nodeNum": 2,
                    "switchType": "default"
                },
                "x": "200",
                "y": "180"
            },
            {
                "number": "3",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "4",
                    "hostname": "xs3",
                    "nodeNum": 3,
                    "switchType": "default"
                },
                "x": "200",
                "y": "220"
            }
        ]
        core_not_contains = [{
            "number": "16",
            "opts": {
                "controllers": [
                    "c0"
                ],
                    "dpid": "11",
                "hostname": "xs16",
                "nodeNum": 16,
                "switchType": "default"
            },
            "x": "200",
            "y": "740"
        }]
        self.assertEqual(16, global_next_switch_num)
        checkList(access_switches, 16, core_contains, core_not_contains, self)

        (access_switches, global_next_switch_num) = generator.createAccessSwitches(4, 4)
        core_contains = [
            {
                "number": "0",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "5",
                    "hostname": "xs0",
                    "nodeNum": 4,
                    "switchType": "default"
                },
                "x": "200",
                "y": "100"
            },
            {
                "number": "1",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "6",
                    "hostname": "xs1",
                    "nodeNum": 5,
                    "switchType": "default"
                },
                "x": "200",
                "y": "140"
            },
            {
                "number": "2",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "7",
                    "hostname": "xs2",
                    "nodeNum": 6,
                    "switchType": "default"
                },
                "x": "200",
                "y": "180"
            },
            {
                "number": "3",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "8",
                    "hostname": "xs3",
                    "nodeNum": 7,
                    "switchType": "default"
                },
                "x": "200",
                "y": "220"
            }
        ]
        core_not_contains = [{
            "number": "16",
            "opts": {
                "controllers": [
                    "c0"
                ],
                    "dpid": "15",
                "hostname": "xs16",
                "nodeNum": 20,
                "switchType": "default"
            },
            "x": "200",
            "y": "740"
        }]

        self.assertEqual(20, global_next_switch_num)
        checkList(access_switches, 16, core_contains, core_not_contains, self)

    def testCreateAggregatorSwitches(self):
        (aggregator_switches,
         global_next_switch_num) = generator.createAggregatorSwitches(4, 0)

        core_contains = [
            {
                "number": "0",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "1",
                    "hostname": "acs00",
                    "nodeNum": 0,
                    "switchType": "default"
                },
                "x": "400",
                "y": "100"
            },
            {
                "number": "1",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "2",
                    "hostname": "acs01",
                    "nodeNum": 1,
                    "switchType": "default"
                },
                "x": "400",
                "y": "140"
            },
            {
                "number": "2",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "3",
                    "hostname": "axs00",
                    "nodeNum": 2,
                    "switchType": "default"
                },
                "x": "300",
                "y": "100"
            },
            {
                "number": "3",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "4",
                    "hostname": "axs01",
                    "nodeNum": 3,
                    "switchType": "default"
                },
                "x": "300",
                "y": "140"
            },
            {
                "number": "12",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "d",
                    "hostname": "acs30",
                    "nodeNum": 12,
                    "switchType": "default"
                },
                "x": "400",
                "y": "340"
            },
            {
                "number": "13",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "e",
                    "hostname": "acs31",
                    "nodeNum": 13,
                    "switchType": "default"
                },
                "x": "400",
                "y": "380"
            },
            {
                "number": "14",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "f",
                    "hostname": "axs30",
                    "nodeNum": 14,
                    "switchType": "default"
                },
                "x": "300",
                "y": "340"
            },
            {
                "number": "15",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "10",
                    "hostname": "axs31",
                    "nodeNum": 15,
                    "switchType": "default"
                },
                "x": "300",
                "y": "380"
            }
        ]
        core_not_contains = []
        self.assertEqual(16, global_next_switch_num)
        checkList(aggregator_switches, 16,
                  core_contains, core_not_contains, self)

        (aggregator_switches,
         global_next_switch_num) = generator.createAggregatorSwitches(4, 4)
        core_contains = [
            {
                "number": "0",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "5",
                    "hostname": "acs00",
                    "nodeNum": 4,
                    "switchType": "default"
                },
                "x": "400",
                "y": "100"
            },
            {
                "number": "1",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "6",
                    "hostname": "acs01",
                    "nodeNum": 5,
                    "switchType": "default"
                },
                "x": "400",
                "y": "140"
            },
            {
                "number": "2",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "7",
                    "hostname": "axs00",
                    "nodeNum": 6,
                    "switchType": "default"
                },
                "x": "300",
                "y": "100"
            },
            {
                "number": "3",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "8",
                    "hostname": "axs01",
                    "nodeNum": 7,
                    "switchType": "default"
                },
                "x": "300",
                "y": "140"
            },
            {
                "number": "12",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "11",
                    "hostname": "acs30",
                    "nodeNum": 16,
                    "switchType": "default"
                },
                "x": "400",
                "y": "340"
            },
            {
                "number": "13",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "12",
                    "hostname": "acs31",
                    "nodeNum": 17,
                    "switchType": "default"
                },
                "x": "400",
                "y": "380"
            },
            {
                "number": "14",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "13",
                    "hostname": "axs30",
                    "nodeNum": 18,
                    "switchType": "default"
                },
                "x": "300",
                "y": "340"
            },
            {
                "number": "15",
                "opts": {
                    "controllers": [
                        "c0"
                    ],
                    "dpid": "14",
                    "hostname": "axs31",
                    "nodeNum": 19,
                    "switchType": "default"
                },
                "x": "300",
                "y": "380"
            }
        ]
        core_not_contains = []

        self.assertEqual(20, global_next_switch_num)
        checkList(aggregator_switches, 16,
                  core_contains, core_not_contains, self)


def checkList(test_list, expected_length, contains, not_contains, test):
    test.assertEqual(expected_length, len(test_list))

    for elem in contains:
        test.assertTrue(elem in test_list, elem)

    for elem in not_contains:
        test.assertFalse(elem in test_list, elem)


if __name__ == "__main__":
    unittest.main()
