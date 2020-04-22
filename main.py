#!/bin/python

import json

# nodeNum is a number!
def createHostJson(number, hostname, nodeNum, sched, x, y):
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


def createLinkJson(dest, opts, src):
    return {
        "dest": dest,
        "opts": opts,
        "src": src
    }

# nodeNum is a number!
def createSwitchJson(number, controller, hostname, nodeNum, switchType, x, y):
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
def createControllerJson(hostname, remoteIP, remotePort):
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

def createApplicationJson():
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

def createMiniEditJson():
    return {
        "application": createApplicationJson(),
        "controllers": [
            createControllerJson("hostname", "remoteIP", 6653)
        ],
        "hosts": [
            createHostJson("1", "h1", 1, "", "300", "300")
        ],
        "links": [
            createLinkJson("dest", {}, "src")
        ],
        "switches": [
            createSwitchJson("1", "c0", "s1", 2, "default", "300", "200")
        ],
        "version": "2"
    }

if __name__ == "__main__":
    print("hallo")

    with open('export.json', 'w') as outfile:
        json.dump(createMiniEditJson(), outfile)