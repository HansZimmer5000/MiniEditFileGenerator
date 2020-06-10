#!/bin/python

import json
import time

# nodeNum is a number!


def createHost(number, hostname, nodeNum, sched, x, y):
    return {
        "number": number,
        "opts": {
            "hostname": hostname,
            "nodeNum": nodeNum,
            "sched": sched
        },
        "x": x,
        "y": y
    }


def createLink(src, opts, dest):
    return {
        "src": src,
        "opts": opts,
        "dest": dest
    }

# nodeNum is a number!


def createSwitch(number, controller, hostname, nodeNum, switchType, x, y):
    return {
        "number": number,
        "opts": {
            "controllers": [
                controller
            ],
            "hostname": hostname,
            "nodeNum": nodeNum,
            "switchType": switchType
        },
        "x": x,
        "y": y
    }

# remotePort is a number!


def createController(hostname, remoteIP, remotePort):
    return {

        "opts": {
            "controllerProtocol": "tcp",
            "controllerType": "remote",
            "hostname": hostname,
            "remoteIP": remoteIP,
            "remotePort": remotePort
        },
        "x": "600.0",
        "y": "100.0"
    }


def createApplication():
    return {
        "dpctl": "",
        "ipBase": "10.0.0.0/8",
        "netflow": {
            "nflowAddId": "0",
            "nflowTarget": "",
            "nflowTimeout": "600"
        },
        "openFlowVersions": {
            "ovsOf10": "0",
            "ovsOf11": "0",
            "ovsOf12": "0",
            "ovsOf13": "0",
            "ovsOf14": "1",
        },
        "sflow": {
            "sflowHeader": "128",
            "sflowPolling": "30",
            "sflowSampling": "400",
            "sflowTarget": ""
        },
        "startCLI": "1",
        "switchType": "ovs",
        "terminalType": "xterm"
    }


def createSwitches(coreswitch_count):
    coreSwitches = []

    aggregatorPodCount = coreswitch_count
    aggregatorPodSwitchCount = int(coreswitch_count)
    aggregatorPods = []

    accessSwitchCount = coreswitch_count*coreswitch_count
    accessSwitches = []

    nextSwitchNum = 1

    print("Creating", coreswitch_count+accessSwitchCount*2, "Switches:", "Core(",
          coreswitch_count, ") Access & Aggregator Switch each(", accessSwitchCount, ")")

    # Create Core Switches
    for x in range(1, coreswitch_count+1):
        newCoreSwitch = createSwitch(str(nextSwitchNum), "c0", "cs" + str(
            nextSwitchNum), nextSwitchNum, "default", "500", str(100+(x-1)*40))
        coreSwitches.append(newCoreSwitch)
        nextSwitchNum += 1

    # Create Aggregator Pods
    nextTotalSwitchNum = nextSwitchNum
    nextSwitchNum = 1

    for x in range(1, aggregatorPodCount+1):
        toCore = []
        toAccess = []

        for y in range(1, int(aggregatorPodSwitchCount/2)+1):
            nextTotalSwitchNum = nextTotalSwitchNum + \
                coreswitch_count+(x-1)*aggregatorPodSwitchCount+(y-1)*2

            newToCoreSwitch = createSwitch(str(nextTotalSwitchNum), "c0", "acs" + str(
                nextSwitchNum), nextTotalSwitchNum, "default", "400", str(100+(x-1)*40))
            nextSwitchNum += 1

            nextTotalSwitchNum += 1
            newToAccessSwitch = createSwitch(str(nextTotalSwitchNum), "c0", "axs" + str(
                nextSwitchNum), nextTotalSwitchNum, "default", "300", str(100+(x-1)*40))
            nextSwitchNum += 1

            newToCoreSwitch.update({"pod": x})
            newToAccessSwitch.update({"pod": x})
            toCore.append(newToCoreSwitch)
            toAccess.append(newToAccessSwitch)

        newAggregatorPod = {"toCore": toCore, "toAccess": toAccess}

        aggregatorPods.append(newAggregatorPod)

    # Create Access Switches
    nextSwitchNum = 1
    for x in range(1, accessSwitchCount+1):
        nextTotalSwitchNum = nextTotalSwitchNum+coreswitch_count + \
            aggregatorPodCount*aggregatorPodSwitchCount

        newAccessSwitch = createSwitch(str(nextTotalSwitchNum), "c0", "xs" + str(
            nextSwitchNum), nextTotalSwitchNum, "default", "200", str(100+(x-1)*40))
        nextSwitchNum += 1

        accessSwitches.append(newAccessSwitch)

    return (coreSwitches, aggregatorPods, accessSwitches)


def createHosts(hostCount):
    hosts = []
    nextHostNum = 1

    for x in range(1, hostCount+1):
        newHost = createHost(str(nextHostNum), "h"+str(nextHostNum),
                             nextHostNum, "host", "100", str(100+(x-1)*40))
        nextHostNum += 1
        hosts.append(newHost)

    return hosts


corePrefix = "cs"
accessPrefix = "xs"
aggregatorAccessPrefix = "axs"
aggregatorCorePrefix = "acs"

'''
Will creat the Links between the Core Switches, begining at <corePrefix>0  with an interconnection degree of 3. It is expected that <coreswitch_count> is at least 4.
'''


def addUniqueLinks(links, new_link):
    orig_src = new_link.get("src")
    orig_dest = new_link.get("dest")
    for old_link in links:
        if old_link.get("src") == orig_dest and old_link.get("dest") == orig_src:
            return
    links.append(new_link)


def createHostToAccessLinks(coreswitch_count):
    host_count = coreswitch_count**2
    links = []

    for host in range(0, host_count):
        current_host = "h" + str(host)
        current_access = "xs" + str(host)
        new_link = createLink(current_host, {}, current_access)
        # No Duplicate check needed as no can be created.
        links.append(new_link)

    return links


def createAccessToAggregatorLinks(coreswitch_count):
    access_count = coreswitch_count**2
    axs_count = int(coreswitch_count/2)
    links = []

    for access in range(0, access_count):
        agg_group = int(access/4)  # 4=#PodElems
        agg_axs = int(access/axs_count) % axs_count
        current_access = "xs" + str(access)
        current_axs = "axs" + str(agg_group) + str(agg_axs)
        new_link = createLink(current_access, {}, current_axs)
        # No Duplicate check needed as no can be created.
        links.append(new_link)

    return links


def createInterAggregatorLinks(coreswitch_count):
    # Beware that links are always bidirectional!
    interconnection_degree = 3
    acs_count = int(coreswitch_count/2)
    axs_count = acs_count
    links = []

    if coreswitch_count >= 4:
        for current_group in range(0, coreswitch_count):

            # Create ACS Links
            for current_acs in range(0, acs_count):
                current_switch1 = "acs" + str(current_group) + str(current_acs)
                current_switch2 = "acs" + \
                    str(current_group) + str((current_acs+1) % acs_count)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

                for current_axs in range(0, axs_count):
                    current_switch2 = "axs" + \
                        str(current_group)+str(current_axs)
                    new_link = createLink(current_switch1, {}, current_switch2)
                    addUniqueLinks(links, new_link)

            # Create AXS Links
            for current_axs in range(0, axs_count):
                current_switch1 = "axs" + str(current_group) + str(current_axs)
                current_switch2 = "axs" + \
                    str(current_group) + str((current_axs+1) % axs_count)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

                for current_acs in range(0, acs_count):
                    current_switch2 = "acs" + \
                        str(current_group)+str(current_acs)
                    new_link = createLink(current_switch1, {}, current_switch2)
                    addUniqueLinks(links, new_link)

    return links


def createAggregatorToCoreLinks(coreswitch_count):
    links = []
    acs_count_per_agg = int(coreswitch_count/2)
    connections_to_core = 2

    for aggregator in range(0, coreswitch_count):
        for acs in range(0, acs_count_per_agg):
            current_acs = "acs" + str(aggregator) + str(acs)

            cs1 = ((aggregator * 2) + acs) % coreswitch_count
            current_cs1 = "cs" + str(cs1)
            new_link = createLink(current_acs, {}, current_cs1)
            links.append(new_link)

            cs2 = ((aggregator * 2) + acs + 1) % coreswitch_count
            current_cs2 = "cs" + str(cs2)
            new_link = createLink(current_acs, {}, current_cs2)
            links.append(new_link)

    return links


def createInterCoreLinks(coreswitch_count):
    interconnection_degree = 3
    links = []

    if coreswitch_count >= 4:
        for current_index1 in range(0, coreswitch_count):
            current_switch1 = "cs" + str(current_index1)

            for current_index2 in range(1, interconnection_degree+1):
                current_switch2 = "cs" + \
                    str((current_index2 + current_index1) % coreswitch_count)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

    return links


def createLinks(coreswitch_count):
    links = []
    # TODO How to link switches to controller, normal link or are they alredy connected due to "remote" key/value in switch?

    host_links = createHostToAccessLinks(coreswitch_count)
    access_links = createAccessToAggregatorLinks(coreswitch_count)
    inter_agg_links = createInterAggregatorLinks(coreswitch_count)
    agg_links = createAggregatorToCoreLinks(coreswitch_count)
    inter_core_links = createInterCoreLinks(coreswitch_count)

    links += host_links
    links += access_links
    links += inter_agg_links
    links += agg_links
    links += inter_core_links

    return links


def createTopology(coreswitch_count, exportFile):
    startTime = time.time()

    # Create Controllers
    controllername = "c0"
    controllers = [createController(controllername, "127.0.0.1", 6653)]

    # Create Switches
    (coreSwitches, aggregatorPods, accessSwitches) = createSwitches(coreswitch_count)

    switches = []
    switches += coreSwitches
    for aggregatorPod in aggregatorPods:
        switches += aggregatorPod["toCore"]
        switches += aggregatorPod["toAccess"]
    switches += accessSwitches

    # Create Hosts
    hostsCount = pow(coreswitch_count, 2)
    hosts = createHosts(hostsCount)

    # Create Links
    links = createLinks(coreswitch_count)

    # CreateApplication
    application = createApplication()

    # Gather the parts
    with open(exportFile, 'w') as outfile:
        json.dump({
            "application": application,
            "controllers": controllers,
            "hosts": hosts,
            "links": links,
            "switches": switches,
            "version": "2"
        }, outfile)

    endTime = time.time()
    duration = endTime - startTime
    durationSec = int(duration)
    print("Generation took ", durationSec, "Seconds")


if __name__ == "__main__":
    print("Beware! This generator is currently quite hardcoded to work with the topolgy described in 'SDN on ACIDs'!\n")

    createTopology(4, 'small.json')
    createTopology(8, 'medium.json')
    createTopology(12, 'large.json')
