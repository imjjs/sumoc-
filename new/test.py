import ctypes
import traci
from threading import Lock
import socket
import subprocess
import os
import time
import sys

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


PORT_LOCK = Lock()
DEVNULL = open(os.devnull, "w")

selected_intersections =  ["Controller202407913" , "Controller1443088096", "Controller202514078", "Controller3010263944", "Controller1443088101"];
phaseCodes = {
"Controller202407913":["GGGggGGGGgrrrr", "yyyggyyyygrrrr", "rrrGGrrrrGrrrr", "rrryyrrrryrrrr", "rrrrrrrrrrGGGG", "rrrrrrrrrryyyy"],
"Controller1443088096":["GGGGggrrGGGGggrrrr", "yyyyggrryyyyggrrrr", "rrrrGGrrrrrrGGrrrr", "rrrryyrrrrrryyrrrr", "GrrrrrGGrrrrrrGGgg", "yrrrrryyrrrrrryygg", "rrrrrrrrrrrrrrrrGG", "rrrrrrrrrrrrrrrryy"],
"Controller202514078":["GGGGggrrrrGGGGggrrrr", "yyyyggrrrryyyyggrrrr", "rrrrGGrrrrrrrrGGrrrr", "rrrryyrrrrrrrryyrrrr", "rrrrrrGGggrrrrrrGGgg", "rrrrrryyggrrrrrryygg", "rrrrrrrrGGrrrrrrrrGG", "rrrrrrrryyrrrrrrrryy"],
"Controller3010263944":["GGggrrrrrGGggrrrrr", "yyggrrrrryyggrrrrr", "rrGGrrrrrrrGGrrrrr", "rryyrrrrrrryyrrrrr", "rrrrGGGggrrrrGGGgg", "rrrryyyggrrrryyygg", "rrrrrrrGGrrrrrrrGG", "rrrrrrryyrrrrrrryy"],
"Controller1443088101":["GGGggrrrrGGGggrrrr", "yyyggrrrryyyggrrrr", "rrrGGrrrrrrrGGrrrr", "rrryyrrrrrrryyrrrr", "rrrrrGGggrrrrrGGgg", "rrrrryyggrrrrryygg", "rrrrrrrGGrrrrrrrGG", "rrrrrrryyrrrrrrryy"]
};

intersection_info = {
    "Controller1443088096": {
        "PhaseToState": {
            "0": "1100",
            "1": "1100",
            "2": "1100",
            "3": "0000",
            "4": "1011",
            "5": "0001",
            "6": "0001",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S32",
            "S33",
            "S34",
            "S35"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller1443088101": {
        "PhaseToState": {
            "0": "1100",
            "1": "1100",
            "2": "1100",
            "3": "0000",
            "4": "0011",
            "5": "0011",
            "6": "0011",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S1",
            "S2",
            "S4",
            "S3"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller202270699": {
        "PhaseToState": {
            "0": "0110",
            "1": "0110",
            "2": "0110",
            "3": "0000",
            "4": "1001",
            "5": "1001",
            "6": "1001",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S18",
            "S16",
            "S17",
            "S19"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller202305800": {
        "PhaseToState": {
            "0": "0110",
            "1": "0110",
            "2": "0110",
            "3": "0000",
            "4": "1001",
            "5": "1001",
            "6": "1001",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S30",
            "S29",
            "S28",
            "S31"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller202407913": {
        "PhaseToState": {
            "0": "011",
            "1": "011",
            "2": "011",
            "3": "000",
            "4": "100",
            "5": "000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5"
        ],
        "sensors": [
            "S11",
            "S10",
            "S9"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller202514063": {
        "PhaseToState": {
            "0": "1010",
            "1": "1010",
            "2": "1010",
            "3": "0000",
            "4": "0101",
            "5": "0101",
            "6": "0101",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S20",
            "S22",
            "S21",
            "S23"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller202514074": {
        "PhaseToState": {
            "0": "0110",
            "1": "0110",
            "2": "0110",
            "3": "0000",
            "4": "1111",
            "5": "1000",
            "6": "1000",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S6",
            "S8",
            "S7",
            "S5"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller202514078": {
        "PhaseToState": {
            "0": "1010",
            "1": "1010",
            "2": "1010",
            "3": "0000",
            "4": "0101",
            "5": "0101",
            "6": "0101",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S13",
            "S14",
            "S12",
            "S15"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller3010263944": {
        "PhaseToState": {
            "0": "1100",
            "1": "1100",
            "2": "1100",
            "3": "0000",
            "4": "0011",
            "5": "0011",
            "6": "0011",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "S24",
            "S25",
            "S27",
            "S26"
        ],
        "threshold1": 3,
        "threshold2": 4
    }
}
sensor_num = {'S1':2, 'S2':2, 'S3':2, 'S4':3, 'S9':3, 'S10':3, 'S11':2, 'S12':3, 'S13':3, 'S14':2, 'S15':1, 'S24':2, 'S25':2, 'S26':2, 'S27':2, 'S32':3, 'S33':3, 'S34':2, 'S35':1}
test = ctypes.cdll.LoadLibrary('build/libtest.so')

def get_open_port(howMany=1):
    """Return a list of n free port numbers on localhost"""
    results = []
    sockets = []
    i=0
    while i < howMany:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        # work out what the actual port number it's bound to is
        addr, port = s.getsockname()
        if port < 40000:
            s.close()
            continue
        results.append(port)
        sockets.append(s)
        i += 1
    for s in sockets:
        s.close()

    return results

def generator_ports():
    PORT_LOCK.acquire()
    ports = get_open_port(1)
    PORT_LOCK.release()
    return ports[0]


def durationAndDistance(port):
    xmlfile = open("tripinfo" + str(port) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalDuration = 0
    totalDistance = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalDuration += float(child.attrib['duration'])
        totalDistance += float(child.attrib['routeLength'])
    xmlfile.close()
    #os.remove("tripinfo" + str(port) + ".xml")
    return totalDistance/ totalDuration


def avgSpeed(filename):
    xmlfile = open(filename, 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalSpeed = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalSpeed += float(child.attrib['routeLength'])/float(child.attrib['duration'])
    avgspeed = totalSpeed * 1.0 / carNumber

    xmlfile.close()

    return avgspeed

def simulationProcess(paraList, sumoMap):
    port = generator_ports()
    sumoProcess = subprocess.Popen(
        ["sumo", "-c", sumoMap, "--tripinfo-output", "tripinfo" + str(port) + ".xml",
         "--remote-port", str(port)], stdout= DEVNULL, stderr = DEVNULL)
    time.sleep(10)

    traci.init(port)
    int_array = (ctypes.c_int * len(paraList))(*paraList)
    test.test_init(len(paraList), int_array)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        for i in selected_intersections:
            sensors = intersection_info[i]['sensors']
            for s in sensors:
                data = 0
                for t in range(sensor_num[s]):
                    data += traci.areal.getLastStepVehicleNumber(s + '#' + str(t))
                # data = traci.multientryexit.getLastStepVehicleNumber(s)
                #print "data:" + str(data) + ', sensor:' + str(s)
                test.handleTrafficSensorInput(s, data, i)
            res = test.nextClockTick(i)
            ltState = phaseCodes[i][res]
            traci.trafficlights.setRedYellowGreenState('tl' + i[10:], ltState)
            #test.debug()


    traci.close()
    sumoProcess.wait()
    time.sleep(10)

    return avgSpeed("tripinfo" + str(port) + ".xml")

if __name__ == '__main__':
    print  simulationProcess([0,5,2,3,7,4,1,6,4,9], '../sumo/Vanderbilt.sumo.cfg')