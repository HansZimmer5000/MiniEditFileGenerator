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
    aggregatorPodSwitchCount=int(coreSwitchCount/2)
    aggregatorPods=[]

    accessSwitchCount=coreSwitchCount*coreSwitchCount
    accessSwitches=[]

    nextSwitchNum = 1

    print("Creating Switches: Core(%d) Aggregator(%d * %d) Access (%d) ", coreSwitchCount, aggregatorPodCount, aggregatorPodSwitchCount, accessSwitchCount)

    # Create Core Switches
    for x in range(1, coreSwitchCount):
        newCoreSwitch = createSwitch(str(nextSwitchNum),"c0", "s" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
        coreSwitches.append(newCoreSwitch)
        nextSwitchNum += 1
    
    # Create Aggregator Pods
    for x in range(1, aggregatorPodCount):
        toCore=[]
        toAccess=[]

        for y in range(1, int(aggregatorPodSwitchCount/2)):
            #nextSwitchNum=nextNodeNum+coreSwitchCount+(x-1)*aggregatorPodSwitchCount+(y-1)*2

            newToCoreSwitch=createSwitch(str(nextSwitchNum),"c0", "s" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
            nextSwitchNum +=1

            newToAccessSwitch=createSwitch(str(nextSwitchNum),"c0", "s" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
            nextSwitchNum += 1

            toCore.append(newToCoreSwitch)
            toAccess.append(newToAccessSwitch)

        newAggregatorPod={"toCore":toCore,"toAccess":toAccess}

        aggregatorPods.append(newAggregatorPod)
    
    # Create Access Switches
    for x in range(1, accessSwitchCount):
        #nextSwitchNum=nextNodeNum+coreSwitchCount+aggregatorPodCount*aggregatorPodSwitchCount

        newAccessSwitch=createSwitch(str(nextSwitchNum),"c0", "s" + str(nextSwitchNum), nextSwitchNum, "default", "100", "100")
        nextSwitchNum += 1

        accessSwitches.append(newAccessSwitch)

    return (coreSwitches, aggregatorPods, accessSwitches)

def createHosts(hostCount):
    hosts = []
    nextHostNum = 1

    for x in range(1,hostCount):
        newHost = createHost(str(nextHostNum), "h"+str(nextHostNum), nextHostNum, "host", "300", "200")

    return hosts

def createSmall():
    coreSwitchCount=4

    # Create Controllers
    controllers = [createController("c0", "remoteIP", "remotePort")]

    # Create Switches
    switches = createSwitches(coreSwitchCount)
    
    # Create Hosts
    hostsCount = pow(coreSwitchCount, 2)
    hosts = createHosts(hostsCount)

    # Create Links
    # TODO
    links = []

    # CreateApplication
    application = createApplication()

    # Gather the parts
    with open('_small.mn', 'w') as outfile:
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