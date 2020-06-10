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

def addUniqueLinks(links,new_link):
    orig_src = new_link.get("src")
    orig_dest = new_link.get("dest")
    for old_link in links:
        if old_link.get("src") == orig_dest and old_link.get("dest") == orig_src:
            return
    links.append(new_link)

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
                addUniqueLinks(links,new_link)

    return links

def createInterAggregatorLinks(coreswitch_count):
    # Beware that links are always bidirectional!
    interconnection_degree = 3
    acs_count = int(coreswitch_count/2)
    axs_count = acs_count
    links = []
    print(axs_count,acs_count)

    if coreswitch_count >= 4:
        for current_group in range(0, coreswitch_count):

            # Create ACS Links
            for current_acs in range(0, acs_count):
                current_switch1 = "acs" + str(current_group) + str(current_acs)
                current_switch2 = "acs" + str(current_group) + str((current_acs+1) % acs_count)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

                for current_axs in range(0, axs_count):
                    current_switch2 = "axs" + str(current_group)+str(current_axs)
                    new_link = createLink(current_switch1, {}, current_switch2)
                    addUniqueLinks(links, new_link)

            # Create AXS Links
            for current_axs in range(0, axs_count):
                current_switch1 = "axs" + str(current_group) + str(current_axs)
                current_switch2 = "axs" + str(current_group) + str((current_axs+1)%axs_count)

                new_link = createLink(current_switch1, {}, current_switch2)
                addUniqueLinks(links, new_link)

                for current_acs in range(0, acs_count):
                    current_switch2 = "acs" + str(current_group)+str(current_acs)
                    new_link = createLink(current_switch1, {}, current_switch2)
                    addUniqueLinks(links, new_link)

    return links
       

def createLinks(coreswitch_count, hostCount, controllername):
    # Link Count with K=4
    # Links Host -> Access = 16     16
    # Links Access -> Aggr = 16     32
    # Links Aggr -> Core   = 16     48
    # Links Core -> Core   = 12     60
    # Links Pods -> Pods   = 12*4   108
    links = []

    # Create Links from Host to Access Switch
    for x in range(1, hostCount+1):
        newLink = createLink("h" + str(x), {}, "xs" + str(x))
        links.append(newLink)

    # Create Links from Access Switches to Aggregator Switches
    # "axs<num>" with num being >= 2 and square
    aggregatorAccessSwitchCount = int(coreswitch_count*2)
    nextXSNum = 1

    for x in range(2, (aggregatorAccessSwitchCount*2)+1):
        if (x % 2) == 0:
            newLink = createLink("xs" + str(nextXSNum), {}, "axs" + str(x))
            links.append(newLink)

            newLink = createLink("xs" + str(nextXSNum + 1), {}, "axs" + str(x))
            links.append(newLink)

            nextXSNum += 2

    # Create Links from Aggregator Switches to Core Switches
    # "acs<num>" with num being >= 1 and not square
    nextACSNum = 1
    for x in range(1, coreswitch_count+1):
        baseACSNum = nextACSNum
        for y in range(0, int((aggregatorAccessSwitchCount*2)/coreswitch_count)):
            nextACSNum = baseACSNum + (y * 2)
            if nextACSNum > (aggregatorAccessSwitchCount*2):
                nextACSNum %= (aggregatorAccessSwitchCount*2)

            newLink = createLink("acs" + str(nextACSNum), {}, "cs" + str(x))
            links.append(newLink)

        nextACSNum += 2

    # Create Links inside the Aggregator Pods
    # first acs is 1, axs is 2. Next two switches in this pod are acs 3 and axs 4 (Example for CoreSwitch=4)
    # TODO Are these links done twice? (acs15->acs13 && acs13->acs15)

    aggregatorSwitchCount = aggregatorAccessSwitchCount * 2
    for x in range(1, aggregatorSwitchCount + 1):
        podNumber = int(x / 4)
        if (x % coreswitch_count) != 0:
            podNumber += 1

        currentHighestNum = coreswitch_count * podNumber
        currentLowestNum = currentHighestNum - (coreswitch_count - 1)

        if (x % 2) == 0:
            currentSwitch = "axs" + str(x)
        else:
            currentSwitch = "acs" + str(x)

        for offset in range(1, 4):
            nextNum = x + offset
            if nextNum > currentHighestNum:
                nextNum %= currentHighestNum
                nextNum += (currentLowestNum - 1)

            if (nextNum % 2) == 0:
                links.append(createLink(
                    currentSwitch, {}, "axs" + str(nextNum)))
            else:
                links.append(createLink(
                    currentSwitch, {}, "acs" + str(nextNum)))

    # Create Links inside the Core Switches
    # TODO Are these links done twice? (cs1->cs2 && cs2->cs1)
    for x in range(1, coreswitch_count + 1):
        for y in range(1, 4):
            targetNum = x+y
            if targetNum > coreswitch_count:
                targetNum %= coreswitch_count

            newLink = createLink("cs" + str(x), {}, "cs" + str(targetNum))
            links.append(newLink)

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
    links = createLinks(coreswitch_count, hostsCount, controllername)

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
