#!/bin/python

import json

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


def createLink(dest, opts, src):
    return {
        "dest": dest,
        "opts": opts,
        "src": src
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
            "controllerType": "ref",
            "hostname": hostname,
            "remoteIP": remoteIP,
            "remotePort": remotePort 
        },
        "x": "760.0",
        "y": "175.0"
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

def createSwitches(coreSwitchCount):
    coreSwitches=[]

    aggregatorPodCount=coreSwitchCount
    aggregatorPodSwitchCount=int(coreSwitchCount)
    aggregatorPods=[]

    accessSwitchCount=coreSwitchCount*coreSwitchCount
    accessSwitches=[]

    nextSwitchNum = 1

    print("Creating Switches: Core(%d) Aggregator(%d * %d) Access (%d) ", coreSwitchCount, aggregatorPodCount, aggregatorPodSwitchCount, accessSwitchCount)

    # Create Core Switches
    for x in range(1, coreSwitchCount+1):
        newCoreSwitch = createSwitch(str(nextSwitchNum),"c0", "cs" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
        coreSwitches.append(newCoreSwitch)
        nextSwitchNum += 1
    
    # Create Aggregator Pods
    for x in range(1, aggregatorPodCount+1):
        toCore=[]
        toAccess=[]

        for y in range(1, int(aggregatorPodSwitchCount/2)+1):
            #nextSwitchNum=nextNodeNum+coreSwitchCount+(x-1)*aggregatorPodSwitchCount+(y-1)*2

            newToCoreSwitch=createSwitch(str(nextSwitchNum),"c0", "acs" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
            nextSwitchNum += 1

            newToAccessSwitch=createSwitch(str(nextSwitchNum),"c0", "axs" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
            nextSwitchNum += 1

            newToCoreSwitch.update({"pod":x})
            newToAccessSwitch.update({"pod":x})
            toCore.append(newToCoreSwitch)
            toAccess.append(newToAccessSwitch)

        newAggregatorPod={"toCore":toCore,"toAccess":toAccess}

        aggregatorPods.append(newAggregatorPod)
    
    # Create Access Switches
    for x in range(1, accessSwitchCount+1):
        #nextSwitchNum=nextNodeNum+coreSwitchCount+aggregatorPodCount*aggregatorPodSwitchCount

        newAccessSwitch=createSwitch(str(nextSwitchNum),"c0", "xs" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
        nextSwitchNum += 1

        accessSwitches.append(newAccessSwitch)

    return (coreSwitches, aggregatorPods, accessSwitches)

def createHosts(hostCount):
    hosts = []
    nextHostNum = 1

    for x in range(1,hostCount+1):
        newHost = createHost(str(nextHostNum), "h"+str(nextHostNum), nextHostNum, "host", "300", "200")
        nextHostNum += 1
        hosts.append(newHost)

    return hosts

def createLinks(coreSwitchCount, hostCount, controllername):
    links=[]

    # Create Links from Host to Access Switch
    for x in range(1, hostCount+1):
        newLink = createLink("h" + str(x), {}, "xs" + str(x))
        links.append(newLink)
    
    # Create Links from Access Switches to Aggregator Switches
    # "axs<num>" with num being >= 2 and square
    aggregatorAccessSwitchCount=int(coreSwitchCount*2)
    nextXSNum=1

    for x in range(1,aggregatorAccessSwitchCount+1):
        newLink = createLink("xs" + str(nextXSNum), {}, "axs" + str(x))
        links.append(newLink)

        newLink = createLink("xs" + str(nextXSNum + 1), {}, "axs" + str(x))
        links.append(newLink)

        nextXSNum += 2

    # Create Links from Aggregator Switches to Core Switches
    # "acs<num>" with num being >= 1 and not square
    nextACSNum=1

    for x in range(1,coreSwitchCount+1):
        newLink = createLink("acs" + str(nextACSNum), {}, "cs" + str(x))
        links.append(newLink)

        newLink = createLink("acs" + str(nextACSNum+4), {}, "cs" + str(x))
        links.append(newLink)

        nextACSNum += 2

    # Create Links inside the Aggregator Pods
    # first acs is 1, axs is 2. Next two switches in this pod are acs 3 and axs 4 (Example for CoreSwitch=4)
    aggregatorSwitchCount = aggregatorAccessSwitchCount * 2
    for x in range(1, aggregatorSwitchCount + 1):
        if (x % 2) == 0:
            currentSwitch = "axs" + str(x)
            links.append(createLink(currentSwitch, {}, "acs" + str(x+1)))
            links.append(createLink(currentSwitch, {}, "axs" + str(x+2)))
            links.append(createLink(currentSwitch, {}, "acs" + str(x+3)))
        else:
            currentSwitch = "acs" + str(x)
            links.append(createLink(currentSwitch, {}, "axs" + str(x+1)))
            links.append(createLink(currentSwitch, {}, "acs" + str(x+2)))
            links.append(createLink(currentSwitch, {}, "axs" + str(x+3)))
        

    # Create Links inside the Core Switches
    for x in range(1, coreSwitchCount + 1):
        for y in range (1,4): 
            targetNum = x+y
            if targetNum > coreSwitchCount:
                targetNum %= coreSwitchCount

            newLink = createLink("cs" + str(x), {}, "cs" + str(targetNum))
            links.append(newLink)

    return links

def createSmall():
    coreSwitchCount=4

    # Create Controllers
    controllername = "c0"
    controllers = [createController(controllername, "127.0.0.1", 6653)]

    # Create Switches
    (coreSwitches,aggregatorPods,accessSwitches) = createSwitches(coreSwitchCount)

    switches = []
    switches += coreSwitches
    for aggregatorPod in aggregatorPods:
        switches += aggregatorPod["toCore"]
        switches += aggregatorPod["toAccess"]
    switches += accessSwitches

    
    # Create Hosts
    hostsCount = pow(coreSwitchCount, 2)
    hosts = createHosts(hostsCount)

    # Create Links
    links = createLinks(coreSwitchCount, hostsCount, controllername)

    # CreateApplication
    application = createApplication()

    # Gather the parts
    with open('small_export.json', 'w') as outfile:
        json.dump({
            "application": application,
            "controllers": controllers,
            "hosts": hosts,
            "links": links,
            "switches": switches,
            "version": "2"
        }, outfile)

if __name__ == "__main__":
    print("hallo")

    createSmall()