import RouteVar
import Stop
import Path
import json
from RouteVarQuery import *
from StopQuery import StopQuery
from PathQuery import PathQuery
from LoadData import *
from Coordinate import *
from Graph import *
from geojson import *
import time
import FunctionCalling
from ContractionHierarchies import *
from TNR import *

RouteVarsList = loadRouteVars()
StopsList = loadStops()
PathsList = loadPaths()
StopsIdList = getStopsIdList(StopsList)
StopsIndices = getStopsIndices(StopsIdList)
StopsIdDict = getStopsIdDict(StopsList)

Edges = generateEdges(RouteVarsList, StopsList, PathsList, StopsIndices)
#Edges = readOriginalEdges()
#Edges = readEdges()

#PreprocessedEdges = readPreprocessedEdges()
#print(Edges)
#G = Graph.Graph(14, len(Edges), StopsIdList, StopsIndices, Edges)
G = Graph.Graph(len(StopsIndices), len(Edges), StopsIdList, StopsIndices, OriginalEdges= Edges)
CH = ContractionHierarchies.ContractionHierarchies(G)
CH.Preprocessing(forTNR= True)
#print(G.Rank)

TNR = TNR(G)
TNR.TNR_Preprocessing(100, CH)
result = TNR.TNR_Query(1769, 2447)
print(result[0], result[1], result[2])
"""G.saveOriginalEdges()
CH = ContractionHierarchies(G)
CH.Preprocessing()
start = time.time()
res = CH.BidirectionalSearch(2521, 124)
end = time.time()
geojson.generatePath(res[2], 'Testing/path.geojson')
print(res[0], end - start)"""