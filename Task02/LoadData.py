import csv
import json
import Graph
from RouteVar import *
from Stop import *
from Path import *
from PathQuery import *
from Coordinate import *
from StopQuery import *
from collections import defaultdict

INF = float('inf')

def loadRouteVars():
    RouteVarsList = []
    with open("data/vars.json", 'r', encoding= 'utf8') as f:
        for line in f:
            data = json.loads(line.strip())
            for route_var in data:
                RouteVarsList.append(
                    RouteVar(
                            route_var['RouteId'],
                            route_var["RouteVarId"],
                            route_var["RouteVarName"],
                            route_var["RouteVarShortName"],
                            route_var["RouteNo"],
                            route_var["StartStop"],
                            route_var["EndStop"],
                            route_var["Distance"],
                            route_var["Outbound"],
                            route_var["RunningTime"],
                            )
                )
    return RouteVarsList

def loadStops():
    StopsList = []
    with open("data/stops.json", 'r', encoding= 'utf8') as f:
        for line in f:
            data = json.loads(line.strip())
            for stop in data["Stops"]:
                StopsList.append(
                    Stop(data["RouteId"], data["RouteVarId"], **stop)
                )
    return StopsList

def loadPaths():
    PathsList = []
    with open("data/paths.json", 'r', encoding= 'utf8') as f:
        for line in f:
            data = json.loads(line.strip())
            PathsList.append(
                Path(**data)
            )
    return PathsList

def getStopsIdList(StopsList):
    StopsIdList = []
    for stop in StopsList:
        StopsIdList.append(stop.getStopId())
    return list(set(StopsIdList))

def getStopsIndices(StopsIdList):
    return {
        StopsIdList[i] : i for i in range(len(StopsIdList))
    }

def getStopsIdDict(StopsList):
    StopsIdDict = {}
    for stop in StopsList:
        StopsIdDict[stop.getStopId()] = stop
    return StopsIdDict

def generateEdges(RouteVarsList, StopsList, PathsList, StopsIndices):
    Edges = {}
    NumEdges = 0
    for route_var in RouteVarsList:
        StopsListQuery = StopQuery(StopQuery(StopsList).searchByRouteId(str(route_var.getRouteId()))).searchByRouteVarId(str(route_var.getRouteVarId()))
        PathsListQuery = PathQuery(PathQuery(PathsList).searchByRouteId(str(route_var.getRouteId()))).searchByRouteVarId(str(route_var.getRouteVarId()))
        speed = route_var.getDistance() / (route_var.getRunningTime() * 60.00)

        first = StopsIndices[StopsListQuery[0].getStopId()]
        RouteVarPath = PathsListQuery[0]
        Longtitudes = RouteVarPath.getLng()
        Lattitudes = RouteVarPath.getLat()
        NumOfCoor = len(Longtitudes)
        stop_idx = 0
        for stop in StopsListQuery[1:]:
            MinDist = INF
            second = StopsIndices[stop.getStopId()]
            y0, x0 = convertLngLatToXY(stop.getLng(), stop.getLat())
            j = 0
            for i in range(stop_idx, NumOfCoor):
                y, x = convertLngLatToXY(Longtitudes[i], Lattitudes[i])
                cur_dist = distance(x, y, x0, y0)
                if cur_dist < MinDist:
                    MinDist = cur_dist
                    j = i
            stop_dist = 0
            coor_path = [(Longtitudes[stop_idx], Lattitudes[stop_idx])]
            while stop_idx < j:
                y1, x1 = convertLngLatToXY(Longtitudes[stop_idx], Lattitudes[stop_idx])
                y2, x2 = convertLngLatToXY(Longtitudes[stop_idx + 1], Lattitudes[stop_idx + 1])
                stop_dist = stop_dist + distance(x1, y1, x2, y2)
                coor_path.append((Longtitudes[stop_idx + 1], Lattitudes[stop_idx + 1]))
                stop_idx = stop_idx + 1
            if (first, second) not in Edges or Edges[(first, second)][1] > stop_dist / speed:
                Edges[(first, second)] = (stop_dist, stop_dist / speed, -1, [], coor_path)
            NumEdges = NumEdges + 1
            first = second
            #print(f"{NumEdges} generated")
    return Edges

def readOriginalEdges():
    Edges = {}
    with open("data/OriginalEdges.json", 'r') as f:
        for line in f:
            edge = json.loads(line)
            Edges[(edge[0], edge[1])] = (-1, edge[2], edge[3], edge[4], edge[5])
            if edge[2] == -1:
                print("error")
    return Edges

def readPreprocessedEdges():
    Edges = []
    with open("data/PreprocessedEdges.json", 'r') as f:
        for line in f:
            data = json.loads(line)
            Edges.append(data)
    return Edges

def readEdges():
    Edges = {}
    with open("Testing/TestGraph.json", 'r') as f:
        for line in f:
            edge = json.loads(line)
            Edges[(edge[0], edge[1])] = (-1, edge[2], -1, [], [])
            if edge[2] == -1:
                print("error")
    return Edges
