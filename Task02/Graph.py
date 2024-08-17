import RouteVar
import Stop
import Path
import geojson
from RouteVarQuery import RouteVarQuery
from StopQuery import StopQuery
from PathQuery import PathQuery
from collections import defaultdict
import json
import heapq
import time
import Coordinate

class Graph():
    INF = float('inf')

    def __init__(self, NumNodes, NumEdges, Stops, StopsIndices, OriginalEdges, PreprocessedEdges = None) -> None:
        self.NumNodes = NumNodes
        self.NumEdges = NumEdges
        self.Nodes = Stops
        self.StopsIndices = StopsIndices
        self.Edges = OriginalEdges
        self.Importance = [0] * NumNodes
        self.AdjList = defaultdict(list)
        self.adj = [[[] for _ in range(self.NumNodes)], [[] for _ in range(self.NumNodes)]]
        self.max_out = [0] * self.NumNodes
        self.max_in = [0] * self.NumNodes
        self.ListEdges = []
        self.isPreprocessed = PreprocessedEdges != None
        self.isCHed = PreprocessedEdges != None
        self.isTNRed = False
        self.Rank = [self.INF] * self.NumNodes
        for node, weight in OriginalEdges.items():
            self.AdjList[node[0]].append((node[1], weight[1]))
            if PreprocessedEdges == None:
                self.addEdge(node[0], node[1], weight[1], index= -1, path= weight[3], list_coor= weight[4])
        if PreprocessedEdges != None:
            self.ListEdges = [None] * (len(PreprocessedEdges[0]) + len(PreprocessedEdges[1]))
            for edge in PreprocessedEdges[0]:
                self.addEdge(edge[0], edge[1], edge[2], index= edge[3], path= edge[4], list_coor= edge[5], side= 0)
                self.ListEdges[edge[3]] = (edge[0], edge[1], edge[2], edge[4], edge[5])
            for edge in PreprocessedEdges[1]:
                self.addEdge(edge[0], edge[1], edge[2], index= edge[3], path= edge[4], list_coor= edge[5], side= 1)
                self.ListEdges[edge[3]] = (edge[0], edge[1], edge[2], edge[4], edge[5])

    def addEdge2(self, u, v, w, index = -1, path = []):
        existed = False
        for edge in self.adj[0][u]:
            if edge[1] == v:
                existed = True
                if edge[0] > w:
                    edge = (w, v, index, path)

        for edge in self.adj[1][v]:
            if edge[1] == u:
                existed = True
                if edge[0] > w:
                    edge = (w, u, index, path)

        if not existed:
            self.adj[0][u].append((w, v, index, path))
            self.adj[1][v].append((w, u, index, path))
            if w > self.max_out[u]:
                self.max_out[u] = w
            if w > self.max_in[v]:
                self.max_in[v] = w  

    def addEdge(self, u, v, w, index = -1, path= [], list_coor= [], side= None):
        if side == None or side == 0:
            self.adj[0][u].append((w, v, index, path, list_coor))
            if w > self.max_out[u]:
                self.max_out[u] = w
        if side == None or side == 1:
            self.adj[1][v].append((w, u, index, path, list_coor))
            if w > self.max_in[v]:
                self.max_in[v] = w                

    def getInEdges(self, u):
        return self.adj[1][u]
    
    def getOutEdges(self, u):
        return self.adj[0][u]
    
    def outputEdges(self):
        converted_data = {str(key): list(value) for key, value in self.Edges.items()}
        with open('Edges.json', 'w', encoding='utf8') as f:
            for key, value in converted_data.items():
                data = {key: value}
                json.dump(data, f, ensure_ascii=False)
                f.write("\n")

    def getNeighbors(self, node_idx):
        return self.AdjList[node_idx]

    def Dijkstra(self, start_node):
        distance = {}
        trace = {}
        distance[start_node] = 0
        trace[start_node] = -1
        heap = []
        heapq.heappush(heap, (0, start_node))
        visited = [False] * self.NumNodes
        while heap:
            p, node = heapq.heappop(heap)
            if visited[node]:
                continue
            visited[node] = True
            for neighbor, weight in self.AdjList[node]:
                if neighbor not in distance:
                    distance[neighbor] = self.INF
                proposed_dist = p + weight
                if distance[neighbor] > proposed_dist:
                    trace[neighbor] = node
                    distance[neighbor] = proposed_dist
                    heapq.heappush(heap, (distance[neighbor], neighbor))
        return (distance, trace)

    def updateImportance(self, trace):
        for node in trace.keys(): 
            k = trace[node]
            while k != -1 and trace[k] != -1:
                self.Importance[k] += 1
                k = trace[k]
                    
    def getShortestPathAllPairs(self, StopsIdList):
            max_time = 0
            max_node = -1
            min_time = 500
            min_node = -1
            total_time = 0
            with open("output/ShortestPathAllPairs.json", 'w', encoding= 'utf8') as fout:
                for u in range(self.NumNodes):
                    start = time.time()
                    result = self.Dijkstra(u)
                    end = time.time()
                    print(f'Calculated shortest path on {u} nodes')
                    node_time = end - start
                    if node_time > max_time:
                        max_time = node_time
                        max_node = StopsIdList[u]
                    if node_time < min_time:
                        min_time = node_time
                        min_node = StopsIdList[u]
                    #self.updateImportance(result[1])
                    total_time += node_time
                    for v in range(self.NumNodes):
                        if u != v and v in result[0]:
                            json.dump((StopsIdList[u], StopsIdList[v], result[0][v] if result[0][v] != self.INF else "INF"), fout, ensure_ascii=False)
                            fout.write('\n')
            print(f"Finished get shortest path all pairs with total time: {total_time} second")
            print(f"max_time: {max_time}, by node: {max_node}")
            print(f"min_time: {min_time}, by node: {min_node}")


    def getDijkstraShortestPath(self, StartStopId, EndStopId):
        if StartStopId not in self.StopsIndices or EndStopId not in self.StopsIndices:
            return
        start = self.StopsIndices[StartStopId]
        end = self.StopsIndices[EndStopId]
        distance = {}
        trace = {}
        distance[start] = 0
        trace[start] = -1
        heap = []
        heapq.heappush(heap, (0, start))
        visited = [False] * self.NumNodes
        path = []
        search_space = 0
        def generatePath(end_stop):
            if end_stop == -1:
                return
            generatePath(trace[end_stop])
            path.append(end_stop)
        while heap:
            p, node = heapq.heappop(heap)
            if node == end:
                generatePath(end)
                path_coordinates = []
                for i in range(len(path) - 1):
                    path_coordinates.extend(self.Edges[path[i], path[i + 1]][4])
                return (distance[end], path, path_coordinates, search_space)
            if visited[node]:
                continue
            visited[node] = True
            search_space += 1
            for neighbor, weight in self.AdjList[node]:
                if neighbor not in distance:
                    distance[neighbor] = self.INF
                proposed_dist = p + weight
                if distance[neighbor] > proposed_dist:
                    trace[neighbor] = node
                    distance[neighbor] = proposed_dist
                    heapq.heappush(heap, (proposed_dist, neighbor))
        return (self.INF, [], [], search_space)

    def AstarShortestPath(self, StopsIdDict, StopsIdList, StartStopId, EndStopId):
        if StartStopId not in self.StopsIndices or EndStopId not in self.StopsIndices:
            return
        start = self.StopsIndices[StartStopId]
        end = self.StopsIndices[EndStopId]
        distance = {}
        trace = {}
        distance[start] = 0
        trace[start] = -1
        heap = []
        cur_y, cur_x = Coordinate.convertLngLatToXY(StopsIdDict[StartStopId].getLng(), StopsIdDict[StartStopId].getLat())
        end_y, end_x =  Coordinate.convertLngLatToXY(StopsIdDict[EndStopId].getLng(), StopsIdDict[EndStopId].getLat())
        heapq.heappush(heap, (Coordinate.distance(cur_x, cur_y, end_x, end_y), start))
        visited = set()
        path = []

        def generatePath(end_stop):
            if end_stop == -1:
                return
            generatePath(trace[end_stop])
            path.append(end_stop)

        while heap:
            p, node = heapq.heappop(heap)
            if node == end:
                generatePath(end)
                path_coordinates = []
                path_len = len(path)
                for i in range(path_len - 1):
                    path_coordinates.extend(self.Edges[path[i], path[i + 1]][4])
                return (distance[end], path, path_coordinates)
            if node in visited:
                continue
            visited.add(node)
            id = StopsIdList[node]
            cur_y, cur_x = Coordinate.convertLngLatToXY(StopsIdDict[id].getLng(), StopsIdDict[id].getLat())
            potential = Coordinate.distance(cur_x, cur_y, end_x, end_y)
            for neighbor, weight in self.AdjList[node]:
                if neighbor not in distance:
                    distance[neighbor] = self.INF
                proposed_dist = p + weight - potential
                if distance[neighbor] > proposed_dist:
                    trace[neighbor] = node
                    distance[neighbor] = proposed_dist
                    neighbor_id = StopsIdList[neighbor]
                    neighbor_y, neighbor_x = Coordinate.convertLngLatToXY(StopsIdDict[neighbor_id].getLng(), StopsIdDict[neighbor_id].getLat())
                    heapq.heappush(heap, (proposed_dist + Coordinate.distance(neighbor_x, neighbor_y, end_x, end_y), neighbor))
        return None

    def findShortestPath(self, StartStopId, EndStopId):
        result = self.getDijkstraShortestPath(StartStopId, EndStopId)
        if result == None:
            print("No shortest path found!")
            return
        print(f"distance: {result[0]}")
        print(f"path: {result[1]}")
        with open("outputShortestPath.json", 'w', encoding= 'utf8') as jsonfile:
            json.dump(result[1], jsonfile, ensure_ascii= False)
            jsonfile.write("\n")
        geojson.generatePath(result[2], 'ShortestPath.geojson')

    def getMostImportantStops(self, StopsList, StopsIdList, k = 30):
        stops = [(self.Importance[i], i) for i in range(self.NumNodes)]
        stops = sorted(stops)
        i = len(stops) - 1
        result = []
        while i >= 0 and k > 0:
            Id = StopsIdList[stops[i][1]]
            print(f"{Id} : {stops[i][0]}")
            stop = StopQuery(StopsList).searchByStopId(Id)[0]
            result.append(stop)
            i -= 1
            k -= 1
        with open("TopStops.json", 'w', encoding= 'utf8') as jsonfile:
            for stop in result:
                json.dump(stop.__dict__, jsonfile, ensure_ascii= False)
                jsonfile.write("\n")
        print(f"most important stops have been printed to TopStops.json")
        return [stops[i][1] for i in range(self.NumNodes)]
    
    def Floyd_Warshall(self, StopsIdList):
        dist = [[self.INF] * self.NumNodes] * self.NumNodes
        for i in range(self.NumNodes):
            for j in range(self.NumNodes):
                if i == j:
                    dist[i][j] = 0
                elif (i, j) in self.Edges.keys():
                    dist[i][j] = self.Edges[(i, j)][0]
        i = j = k = 0
        for k in range(self.NumNodes):
            for i in range(self.NumNodes):
                for j in range(self.NumNodes):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
            print(f"Calculated {k}/{self.NumNodes}")
            
        with open('Floyd-Warshall.json', 'w', encoding= 'utf8') as jsonfile:
            for i in range(self.NumNodes):
                for j in range(self.NumNodes):
                    if i == j:
                        continue
                    json.dump((StopsIdList[i], StopsIdList[j], dist[i][j]), jsonfile, ensure_ascii= False)
                    jsonfile.write("\n")
        print("Shortest Paths all pairs by Floyd-Warshall have been printed to Floyd-Warshall.json")

    def saveOriginalEdges(self):
        with open('data/OriginalEdges.json', 'w') as json_f:
            for edge, weight in self.Edges.items():
                json.dump([edge[0], edge[1], weight[1], -1, weight[3], weight[4]], json_f)
                json_f.write("\n")
        print("Original edges saved successfully")

        
    def savePreprocessedEdges(self):
        with open('data/PreprocessedEdges.json', 'w') as json_f:
            adj0 = []
            adj1 = []
            for i in range(self.NumNodes):
                for j in range(len(self.adj[0][i])):
                    adj0.append([i, self.adj[0][i][j][1], self.adj[0][i][j][0], self.adj[0][i][j][2], self.adj[0][i][j][3], self.adj[0][i][j][4]])
            for i in range(self.NumNodes):
                for j in range(len(self.adj[1][i])):
                    adj1.append([self.adj[1][i][j][1], i, self.adj[1][i][j][0], self.adj[1][i][j][2], self.adj[1][i][j][3], self.adj[1][i][j][4]])
            json.dump(adj0, json_f)
            json_f.write("\n")
            json.dump(adj1, json_f)
        print("Preprocessed edges saved successfully")
    
    def saveNodesRank(self):
        with open('data/Rank.json', 'w') as f:
            json.dump(self.Rank, f)
    
    def loadRank(self):
        with open('data/Rank.json', 'r') as f:
            self.Rank = json.load(f)




                




