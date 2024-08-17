import Graph
import ContractionHierarchies
import TNR
import time
import random
from LoadData import *

RouteVarsList = loadRouteVars()
StopsList = loadStops()
PathsList = loadPaths()
StopsIdList = getStopsIdList(StopsList)
StopsIndices = getStopsIndices(StopsIdList)
StopsIdDict = getStopsIdDict(StopsList)

opt = int(input("Load data from scratch (input 0) or load preprocessed data (input 1) ?"))
print("Loading data...")

Edges = None
PreprocessedEdges = None

if opt == 0:
    print("Building data from scratch...")
    Edges = generateEdges(RouteVarsList, StopsList, PathsList, StopsIndices)
else:
    print("Loading preprocessed data...")
    Edges = readOriginalEdges()
    PreprocessedEdges = readPreprocessedEdges()

G = Graph.Graph(len(StopsIndices), len(Edges), StopsIdList, StopsIndices, Edges, PreprocessedEdges= PreprocessedEdges)
CH_query = ContractionHierarchies.ContractionHierarchies(G)
TNR_query = TNR.TNR(G)
if opt == 1:
    G.loadRank()
    TNR_query.loadPreprocessedData()
    print("Preprocessed data loaded!")
else:
    print("Preprocessing the graph...")
TNR_query.TNR_Preprocessing(100, CH_query)

NumOfQuery = int(input("Number of Queries: "))
Tested = set()
Tested.add((-1, -1))
correct = 0
path_correct = 0
path_coor_correct = 0
total_CH_time = 0
total_Dijkstra_time = 0
total_TNR_time = 0
total_CH_searchspace = 0
total_Dijkstra_searchspace = 0
localSearch = 0
with open('Testing/test.txt', 'w', encoding= 'utf8') as f, open('Testing/path.txt', 'w', encoding= 'utf8') as fp:
    for i in range(NumOfQuery):
        source  = -1
        target = -1
        while source == target or (source, target) in Tested: 
            source = random.randint(0, 4396)
            target = random.randint(0, 4396)
        Tested.add((source, target))   

        #CH query
        start = time.time()
        CH_res = CH_query.BidirectionalSearch(source, target)
        end = time.time()
        CH_time = end - start
        total_CH_time += CH_time
        total_CH_searchspace += CH_res[3]

        #Dijkstra query
        start = time.time()
        D_res = G.getDijkstraShortestPath(StopsIdList[source], StopsIdList[target])
        end = time.time()
        D_time = end - start
        total_Dijkstra_time += D_time
        total_Dijkstra_searchspace += D_res[3]

        #TNR query
        local = False
        start = time.time()
        TNR_res = TNR_query.TNR_Query(source, target)
        end = time.time()
        if TNR_res[3]:
            localSearch += 1
        TNR_time = end - start
        total_TNR_time += TNR_time

        if round(TNR_res[0], 5) == round(D_res[0], 5) and round(TNR_res[0], 5) == round(CH_res[0], 5):
            correct += 1
        if TNR_res[1] == D_res[1] and TNR_res[1] == CH_res[1]:
            path_correct += 1
        if TNR_res[2] == D_res[2] and TNR_res[2] == CH_res[2]:
            path_coor_correct += 1
        fp.write(f"source: {source}, target: {target}:\n")
        fp.write(f"CH: {CH_res[1]}\n")
        fp.write(f"Dijkstra: {D_res[1]}\n")
        fp.write(f"TNR: {TNR_res[1]}\n")
        fp.write(f"CH: {CH_res[2]}\n")
        fp.write(f"Dijkstra: {D_res[2]}\n")
        fp.write(f"TNR: {TNR_res[2]}\n")
        f.write(f"source: {source}, target: {target}\n")
        f.write(f"CH: {round(CH_res[0], 5)}, time: {round(CH_time, 5)} seconds, search space: {CH_res[3]}\n")
        f.write(f"Dijkstra: {round(D_res[0], 5)}, time {round(D_time, 5)} seconds, search space: {D_res[3]}\n")
        f.write(f"TNR: {round(TNR_res[0], 5)}, time: {round(TNR_time, 5)} seconds\n")
print(f"Cost similarity: {correct}/{NumOfQuery} queries")
print(f"Path Similarity: {path_correct}/{NumOfQuery} queries")
print(f"Path Coordinates Similarity: {path_coor_correct}/{NumOfQuery} queries")
print(f"Total CH time: {total_CH_time} seconds, average time: {total_CH_time / NumOfQuery} seconds/query, average search space: {int(total_CH_searchspace / NumOfQuery)} nodes/query")
print(f"Total Dijkstra time: {total_Dijkstra_time} seconds, average time: {total_Dijkstra_time / NumOfQuery} seconds/query, average search space: {int(total_Dijkstra_searchspace / NumOfQuery)} nodes/query")
print(f"Total TNR time: {total_TNR_time} seconds, average time: {total_TNR_time / NumOfQuery} seconds/query")
print(f"Total Local Search for TNR: {localSearch}/{NumOfQuery}")

#saving queries
with open('Testing/queries.txt', 'w') as f:
    f.write(f"{NumOfQuery}\n")
    for test in Tested:
        if test == (-1, -1):
            continue
        f.write(f"{test[0]} {test[1]}\n")

        