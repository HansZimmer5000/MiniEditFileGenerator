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


def createSwitch(number, controller, hostname, nodeNum, switchType, x, y, dpid):
    return {
        "number": number,
        "opts": {
            "controllers": [
                controller
            ],
            "dpid": dpid,
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


def __createSwitchesOf(prefix, count, global_next_switch_num, x, y=100, start_number=0):
    switches = []

    for current_number in range(0, count):
        current_name = prefix + str(current_number)
        current_y = str(y+(40*current_number))
        current_switch_num = str(current_number + start_number)
        current_dpid = hex(global_next_switch_num+1).replace("0x", "")

        new_switch = createSwitch(
            current_switch_num, "c0", current_name, global_next_switch_num, "default", x, current_y, current_dpid)
        switches.append(new_switch)

        global_next_switch_num += 1

    return (switches, global_next_switch_num)


def createCoreSwitches(coreswitch_count, global_next_switch_num):
    return __createSwitchesOf("cs", coreswitch_count, global_next_switch_num, "500")


def createAccessSwitches(coreswitch_count, global_next_switch_num):
    access_count = coreswitch_count ** 2
    return __createSwitchesOf("xs", access_count, global_next_switch_num, "200")


def createAggregatorSwitches(coreswitch_count, global_next_switch_num):
    agg_switches = []
    acs_count = int(coreswitch_count/2)
    axs_count = acs_count
    pod_count = coreswitch_count
    pod_switches_count = coreswitch_count
    acs_x = "400"
    acs_y = 100
    axs_x = "300"
    axs_y = 100

    for current_pod in range(0, pod_count):
        current_num = current_pod * pod_switches_count
        (tmp_switches, global_next_switch_num) = __createSwitchesOf(
            "acs" + str(current_pod), acs_count, global_next_switch_num, acs_x, acs_y, current_num)
        acs_y += 40 * acs_count

        agg_switches += tmp_switches

        current_num += acs_count
        (tmp_switches, global_next_switch_num) = __createSwitchesOf(
            "axs" + str(current_pod), axs_count, global_next_switch_num, axs_x, axs_y, current_num)
        axs_y += 40 * axs_count

        agg_switches += tmp_switches

    return (agg_switches, global_next_switch_num)


def createSwitches(coreswitch_count):
    switches = []
    global_next_switch_num = 0

    (core_switches, global_next_switch_num) = createCoreSwitches(
        coreswitch_count, global_next_switch_num)
    (acc_switches, global_next_switch_num) = createAccessSwitches(
        coreswitch_count, global_next_switch_num)
    (agg_switches, global_next_switch_num) = createAggregatorSwitches(
        coreswitch_count, global_next_switch_num)

    switches += core_switches
    switches += acc_switches
    switches += agg_switches

    return switches


def createHosts(hostCount):
    hosts = []

    for nodeNum in range(0, hostCount):
        newHost = createHost(str(nodeNum), "h"+str(nodeNum),
                             nodeNum, "host", "100", str(100+(nodeNum*40)))
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
    pod_elems = coreswitch_count
    xs_per_axs = 2
    links = []

    for access in range(0, access_count):
        agg_group = int(access/pod_elems)
        agg_axs = int(access/xs_per_axs) % axs_count
        current_access = "xs" + str(access)
        current_axs = "axs" + str(agg_group) + str(agg_axs)
        new_link = createLink(current_access, {}, current_axs)
        # No Duplicate check needed as no can be created.
        links.append(new_link)

    return links


def createInterAggregatorLinks(coreswitch_count):
    group_acs_count = 2
    group_axs_count = group_acs_count
    links = []

    for current_pod in range(0, coreswitch_count):

        for group in range(0, int(coreswitch_count/4)):
            group_offset = group*2

            # Create ACS Links
            for current_acs in range(group_offset, group_acs_count + group_offset):
                current_switch1 = "acs" + str(current_pod) + str(current_acs)
                current_switch2_num = current_acs + 1
                if current_switch2_num >= group_offset+2:
                    current_switch2_num -= 2

                current_switch2 = "acs" + \
                    str(current_pod) + str(current_switch2_num)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

                for current_axs in range(group_offset, group_axs_count + group_offset):
                    current_switch2 = "axs" + \
                        str(current_pod)+str(current_axs)
                    new_link = createLink(current_switch1, {}, current_switch2)
                    addUniqueLinks(links, new_link)

            # Create AXS Links
            for current_axs in range(group_offset, group_axs_count + group_offset):
                current_switch1 = "axs" + str(current_pod) + str(current_axs)
                current_switch2_num = current_axs + 1
                if current_switch2_num >= group_offset+2:
                    current_switch2_num -= 2

                current_switch2 = "axs" + \
                    str(current_pod) + str(current_switch2_num)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

                for current_acs in range(group_offset, group_acs_count + group_offset):
                    current_switch2 = "acs" + \
                        str(current_pod)+str(current_acs)
                    new_link = createLink(current_switch1, {}, current_switch2)
                    addUniqueLinks(links, new_link)

    return links


def createAggregatorToCoreLinks(coreswitch_count):
    links = []
    acs_count_per_agg = int(coreswitch_count/2)
    pod_count = coreswitch_count

    for pod in range(0, pod_count):
        for acs in range(0, acs_count_per_agg):
            current_acs = "acs" + str(pod) + str(acs)

            cs1 = ((pod * 2) + acs) % coreswitch_count
            current_cs1 = "cs" + str(cs1)
            new_link = createLink(current_acs, {}, current_cs1)
            links.append(new_link)

            cs2 = ((pod * 2) + acs + 1) % coreswitch_count
            current_cs2 = "cs" + str(cs2)
            new_link = createLink(current_acs, {}, current_cs2)
            links.append(new_link)

    return links


def createInterCoreLinks(coreswitch_count):
    interconnection_degree = 3
    links = []

    for group in range(0, int(coreswitch_count/4)):
        group_offset = group*4
        for current_index in range(group_offset, 4+group_offset):
            current_switch1 = "cs" + str(current_index)

            for current_offset in range(1, interconnection_degree+1):
                current_switch2_num = current_offset+current_index
                if (current_switch2_num >= 4+group_offset):
                    current_switch2_num -= 4

                current_switch2 = "cs" + \
                    str(current_switch2_num)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

    return links


def createLinks(coreswitch_count):
    links = []

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
    switches = createSwitches(coreswitch_count)

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
    durationSec = round(duration, 2)
    print("Generation took", durationSec, "Seconds")


if __name__ == "__main__":
    print("Beware! This generator is currently quite hardcoded to work with the topolgy described in 'SDN on ACIDs'!\n")

    createTopology(4, 'small.json')
    createTopology(8, 'medium.json')
    createTopology(12, 'large.json')
