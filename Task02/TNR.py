import Graph
import ContractionHierarchies
import heapq
import time
import json

class TNR():
    def __init__(self, graph: Graph.Graph) -> None:
        self.G = graph
        self.NumNodes = graph.NumNodes
        self.NumTN = 0
        self.TransitNodes = []
        self.isTransitNodes = [False for _ in range(self.NumNodes)]
        self.TransitIndex = [-1] * self.NumNodes
        self.TransitTable = []
        self.Voronoi = [-1] * self.NumNodes
        self.adj = [[[] for _ in range(self.NumNodes)], [[] for _ in range(self.NumNodes)]]
        #self.adj = self.G.adj
        for edge, weight in self.G.Edges.items():
            try:
                self.adj[0][edge[0]].append((edge[1], weight[1], weight[3], weight[4]))
                self.adj[1][edge[1]].append((edge[0], weight[1], weight[3], weight[4]))
            except:
                print(edge[0], edge[1])
                print(self.NumNodes)

        self.SearchSpace = [[{} for _ in  range(self.NumNodes)] for _ in range(2)]
        self.AccessNodeDistance = [[{} for _ in range(self.NumNodes)] for _ in range(2)]
    
    def getInEdges(self, node):
        return self.adj[1][node]
    
    def getOutEdges(self, node):
        return self.adj[0][node]    
    
    def getTransitNodes(self, numTN):
        index = 0
        for i in range(self.NumNodes):
            if self.G.Rank[i] >= self.NumNodes - numTN:
                self.TransitNodes.append(i)
                self.TransitIndex[i] = index
                self.isTransitNodes[i] = True
                index += 1
        #print(self.TransitNodes)
        self.NumTN = numTN
        self.TransitTable = [[self.G.INF for _ in range(self.NumTN)] for _ in range(self.NumTN)]

    def getTransitTable(self):
        for i in range(len(self.TransitNodes)):
            for j in range(len(self.TransitNodes)):
                if i == j:
                    self.TransitTable[i][j] = (0, [], [])
                else:
                    self.TransitTable[i][j] = self.getShortestPathWithoutTNR(self.TransitNodes[i], self.TransitNodes[j])
        #print(self.TransitTable)

    def getVoronoiRegions(self):
        queue = []
        distance = [self.G.INF] * self.NumNodes
        for idx, node in enumerate(self.TransitNodes):
            queue.append((0, node))
            self.Voronoi[node] = idx
            distance[node] = 0
        heapq.heapify(queue)
        visited = [False] * self.NumNodes
        while queue:
            _, node = heapq.heappop(queue)
            if visited[node]:
                continue
            visited[node] = True
            InEdges = self.getInEdges(node)
            for edge in InEdges:
                if distance[node] + edge[1] < distance[edge[0]]:
                    distance[edge[0]] = distance[node] + edge[1]
                    heapq.heappush(queue, (distance[edge[0]], edge[0]))
                    self.Voronoi[edge[0]] = self.Voronoi[node]

    def getPath(self, estimate, middle_node, forward_trace, backward_trace):
        if estimate == self.G.INF or middle_node == -1:
            return [], []
        path = []
        path_coor = []
        edge_idx = forward_trace[middle_node]
        #ListEdges: 0: from, 1: to, 2: weight, 3: path
        while edge_idx != -1:
            edge = self.G.ListEdges[edge_idx]
            path.extend(reversed(edge[3]))
            path.append(edge[0])
            path_coor.extend(reversed(edge[4]))
            edge_idx = forward_trace[edge[0]]
        path.reverse()
        path_coor.reverse()
        path.append(middle_node)
        edge_idx = backward_trace[middle_node]
        while edge_idx != -1:
            edge = self.G.ListEdges[edge_idx]
            path.extend(edge[3])
            path.append(edge[1])
            path_coor.extend(edge[4])
            edge_idx = backward_trace[edge[1]]
        #print(f"Get path in {end - start} seconds")
        return path, path_coor

    def getShortestPathWithoutTNR(self, start, end):
        forward_queue = []
        backward_queue = []
        forward_dist = [self.G.INF] * self.NumNodes
        backward_dist = [self.G.INF] * self.NumNodes
        forward_dist[start] = 0
        backward_dist[end] = 0
        forward_visited = [False] * self.NumNodes
        backward_visited = [False] * self.NumNodes
        heapq.heappush(forward_queue, (0, start))
        heapq.heappush(backward_queue, (0, end))
        estimate = self.G.INF
        middle_node = -1
        forward_trace = [-1] * self.NumNodes
        backward_trace = [-1] * self.NumNodes
        
        while forward_queue or backward_queue:
            if forward_queue:
                dist, u = heapq.heappop(forward_queue)
                forward_visited[u] = True
                
                in_neighbors = self.G.getInEdges(u)

                if forward_dist[u] <= estimate:
                    out_neighbors = self.G.getOutEdges(u)
                    for out_edge in out_neighbors:
                        if self.G.Rank[out_edge[1]] < self.G.Rank[u]:
                            continue
                        if forward_dist[out_edge[1]] > forward_dist[u] + out_edge[0]:
                            forward_dist[out_edge[1]] = forward_dist[u] + out_edge[0]
                            heapq.heappush(forward_queue, (forward_dist[out_edge[1]], out_edge[1]))
                            forward_trace[out_edge[1]] = out_edge[2]

                #check if the node u has been visited in the backward search:
                if backward_visited[u] and forward_dist[u] + backward_dist[u] < estimate:
                    estimate = backward_dist[u] + forward_dist[u]
                    middle_node = u
            
            if backward_queue:
                _, u = heapq.heappop(backward_queue)
                backward_visited[u] = True
                
                out_neighbors = self.G.getOutEdges(u)
                
                if backward_dist[u] <= estimate:
                    in_neighbors = self.G.getInEdges(u)
                    for in_edge in in_neighbors:
                        if self.G.Rank[in_edge[1]] < self.G.Rank[u]:
                            continue
                        if backward_dist[in_edge[1]] > backward_dist[u] + in_edge[0]:
                            backward_dist[in_edge[1]] = backward_dist[u] + in_edge[0]
                            heapq.heappush(backward_queue, (backward_dist[in_edge[1]], in_edge[1]))
                            backward_trace[in_edge[1]] = in_edge[2]

                #check if the node u has been visited in the backward search:
                if forward_visited[u] and forward_dist[u] + backward_dist[u] < estimate:
                    estimate = forward_dist[u] + backward_dist[u]
                    middle_node = u
        path = self.getPath(estimate, middle_node, forward_trace, backward_trace)
        return estimate, path[0], path[1]
    
    def getLocalityFilter(self):
        #Initialize a Max Heap with priority is the Rank of the nodes
        Nodes = [(-self.G.Rank[node], node) for node in range(self.NumNodes)]
        Nodes = sorted(Nodes)

        Visited = [[False for _ in range(self.NumNodes)] for _ in range(2)]

        #Compute for each node
        for e in Nodes:
            SourceNode = e[1]
            #Forward computation of the set of reachable Voronoi regions and Acess Nodes
            if not Visited[0][SourceNode]:
                SearchHeap = [(0, SourceNode)]
                
                distance = [self.G.INF for _ in range(self.NumNodes)]
                distance[SourceNode] = 0
                
                while SearchHeap:
                    dist, CurNode = heapq.heappop(SearchHeap)
                    if not self.isTransitNodes[CurNode]:
                        self.SearchSpace[0][SourceNode][self.Voronoi[CurNode]] = True

                        #If encountering a visited node, we will inherit all of its results
                        if Visited[0][CurNode]:
                            for node in self.SearchSpace[0][CurNode]:
                                self.SearchSpace[0][SourceNode][node] = True
                            for node in self.AccessNodeDistance[0][CurNode]:
                                self.AccessNodeDistance[0][SourceNode][node] = -1
                        else:
                            OutEdges = self.G.getOutEdges(CurNode)
                            for edge in OutEdges:
                                OutNode = edge[1]
                                Weight = edge[0]
                                if self.G.Rank[CurNode] < self.G.Rank[OutNode]:
                                    if distance[OutNode] > dist + Weight:
                                        distance[OutNode] = dist + Weight
                                        heapq.heappush(SearchHeap, (distance[OutNode], OutNode))

                    #Do not enlarge the Search Heap when a transit node is encountered
                    else:
                        self.AccessNodeDistance[0][SourceNode][CurNode] = -1

                #Compute the distance from The Source Node to each possible Access Node
                for AccessNode in self.AccessNodeDistance[0][SourceNode]:
                    self.AccessNodeDistance[0][SourceNode][AccessNode] = self.getShortestPathWithoutTNR(SourceNode, AccessNode)

                InvalidAccessNodes = set()
                for node1 in self.AccessNodeDistance[0][SourceNode]:
                    d1 = self.AccessNodeDistance[0][SourceNode][node1][0]
                    for node2 in self.AccessNodeDistance[0][SourceNode]:
                        if node1 == node2:
                            continue
                        d2 = self.AccessNodeDistance[0][SourceNode][node2][0]
                        if d1 + self.TransitTable[self.TransitIndex[node1]][self.TransitIndex[node2]][0] <= d2:
                            InvalidAccessNodes.add(node2)
                for node in InvalidAccessNodes:
                    del self.AccessNodeDistance[0][SourceNode][node]

                Visited[0][SourceNode] = True

            #Backward computation of the set of reachable Voronoi regions and Acess Nodes
            if not Visited[1][SourceNode]:
                SearchHeap = [(0, SourceNode)]
                
                distance = [self.G.INF for _ in range(self.NumNodes)]
                distance[SourceNode] = 0
                
                while SearchHeap:
                    dist, CurNode = heapq.heappop(SearchHeap)

                    if not self.isTransitNodes[CurNode]:
                        self.SearchSpace[1][SourceNode][self.Voronoi[CurNode]] = True

                        #If encountering a visited node, we will inherit all of its results
                        if Visited[1][CurNode]:
                            for node in self.SearchSpace[1][CurNode]:
                                self.SearchSpace[1][SourceNode][node] = True
                            for node in self.AccessNodeDistance[1][CurNode]:
                                self.AccessNodeDistance[1][SourceNode][node] = -1
                        else:
                            InEgdes = self.G.getInEdges(CurNode)
                            for edge in InEgdes:
                                InNode = edge[1]
                                Weight = edge[0]
                                if self.G.Rank[CurNode] < self.G.Rank[InNode]:
                                    if distance[InNode] > dist + Weight:
                                        distance[InNode] = dist + Weight
                                        heapq.heappush(SearchHeap, (distance[InNode], InNode))

                    #Do not enlarge the Search Heap when a transit node is encountered
                    else:
                        self.AccessNodeDistance[1][SourceNode][CurNode] = -1

                #Compute the distance from The Source Node to each possible Access Node
                for AccessNode in self.AccessNodeDistance[1][SourceNode]:
                    self.AccessNodeDistance[1][SourceNode][AccessNode] = self.getShortestPathWithoutTNR(AccessNode, SourceNode)

                InvalidAccessNodes = set()
                for node1 in self.AccessNodeDistance[1][SourceNode]:
                    d1 = self.AccessNodeDistance[1][SourceNode][node1][0]
                    for node2 in self.AccessNodeDistance[1][SourceNode]:
                        if node1 == node2:
                            continue
                        d2 = self.AccessNodeDistance[1][SourceNode][node2][0]
                        if d1 + self.TransitTable[self.TransitIndex[node2]][self.TransitIndex[node1]][0] <= d2:
                            InvalidAccessNodes.add(node2)
                for node in InvalidAccessNodes:
                    del self.AccessNodeDistance[1][SourceNode][node]

                Visited[1][SourceNode] = True
    
    def TNR_Preprocessing(self, numTN, CH : ContractionHierarchies.ContractionHierarchies):
        start = time.time()
        if numTN > self.NumNodes:
            return
        if self.G.isTNRed:
            return
        if not self.G.isCHed:
            CH.Preprocessing(forTNR= True)
        
        self.getTransitNodes(numTN)
        self.getVoronoiRegions()
        #CH.removeEdges()
        self.getTransitTable()
        self.getLocalityFilter()

        self.G.isTNRed = True
        self.G.isPreprocessed = True
        end = time.time()
        print(f"TNR preprocessed in: {round(end - start, 4)} seconds")
    
    def printVoronoi(self):
        print("Voronoi:")
        for node, V in enumerate(self.Voronoi):
            print(node, V)

    def TNR_Query(self, source, target):
        if not self.G.isTNRed:
            print("The graph has not been preprocessed using TNR!")
            return -1, []
        
        #Check for Local Query:
        if len(self.AccessNodeDistance[0][source]) == 0 or len(self.AccessNodeDistance[1][target]) == 0:
            #print("Local Search due to lack of access nodes")
            dist, path, path_coor = self.getShortestPathWithoutTNR(source, target)
            return dist, path, path_coor, True
        
        for target_access_node in self.SearchSpace[0][source]:
            if target_access_node in self.SearchSpace[1][target]:
                #("Local Search due to Overlapped Voronoi regions")
                dist, path, path_coor = self.getShortestPathWithoutTNR(source, target)
                return dist, path, path_coor, True
            
        #TNR query:
        best_forward = None
        best_backward = None
        minDist = self.G.INF
        for forward_node in self.AccessNodeDistance[0][source]:
            source_idx = self.TransitIndex[forward_node]
            for backward_node in self.AccessNodeDistance[1][target]:
                target_idx = self.TransitIndex[backward_node]
                proposed_dist = (self.AccessNodeDistance[0][source][forward_node][0] + 
                                 self.AccessNodeDistance[1][target][backward_node][0] + 
                                 self.TransitTable[source_idx][target_idx][0])
                if proposed_dist < minDist:
                    minDist = proposed_dist
                    best_forward = forward_node
                    best_backward = backward_node
        
        path = []
        path_coor = []
        if best_forward and best_backward:
            path.extend(self.AccessNodeDistance[0][source][best_forward][1])
            path_coor.extend(self.AccessNodeDistance[0][source][best_forward][2])
            path.extend(self.TransitTable[self.TransitIndex[best_forward]][self.TransitIndex[best_backward]][1][1:])
            path_coor.extend(self.TransitTable[self.TransitIndex[best_forward]][self.TransitIndex[best_backward]][2])
            path.extend(self.AccessNodeDistance[1][target][best_backward][1][1:])
            path_coor.extend(self.AccessNodeDistance[1][target][best_backward][2])

        return minDist, path, path_coor, False

    def saveTransitNodes(self):
        with open('data/TransitNodes.json', 'w') as f:
            json.dump(self.TransitNodes, f)
    
    def saveVoronoiRegions(self):
        with open('data/Voronoi.json', 'w') as f:
            json.dump(self.Voronoi, f)
    
    def saveTransitTable(self):
        with open('data/TransitTable.json', 'w') as f:
            json.dump(self.TransitTable, f)

    def saveSearchSpace(self):
        with open('data/SearchSpace.json', 'w') as f:
            json.dump(self.SearchSpace, f)
    
    def saveAccessNodeDistance(self):
        with open('data/AccessNodeDistance.json', 'w') as f:
            json.dump(self.AccessNodeDistance, f)

    def savePreprocessedData(self):
        self.saveTransitNodes()
        self.saveVoronoiRegions()
        self.saveTransitTable()
        self.saveSearchSpace()
        self.saveAccessNodeDistance()
        print("finish saving preprocessed data!")

    def loadTransitNodes(self):
        with open('data/TransitNodes.json', 'r') as f:
            self.TransitNodes = json.load(f)
        for idx, node in enumerate(self.TransitNodes):
            self.TransitIndex[node] = idx
            self.isTransitNodes[node] = True
    
    def loadVoronoiRegions(self):
        with open('data/Voronoi.json', 'r') as f:
            self.Voronoi = json.load(f)
    
    def loadTransitTable(self):
        with open('data/TransitTable.json', 'r') as f:
            self.TransitTable = json.load(f)

    def loadSearchSpace(self):
        tmp = {}
        with open('data/SearchSpace.json', 'r') as f:
            tmp = json.load(f)
        for node in range(len(tmp[0])):
            for key, val in tmp[0][node].items():
                self.SearchSpace[0][node][int(key)] = val
        for node in range(len(tmp[1])):
            for key, val in tmp[1][node].items():
                self.SearchSpace[1][node][int(key)] = val


    
    def loadAccessNodeDistance(self):
        tmp = None
        with open('data/AccessNodeDistance.json', 'r') as f:
            tmp = json.load(f)
        for node in range(len(tmp[0])):
            for key, val in tmp[0][node].items():
                self.AccessNodeDistance[0][node][int(key)] = val
        for node in range(len(tmp[1])):
            for key, val in tmp[1][node].items():
                self.AccessNodeDistance[1][node][int(key)] = val

    def loadPreprocessedData(self):
        self.loadTransitNodes()
        self.loadVoronoiRegions()
        self.loadTransitTable()
        self.loadSearchSpace()
        self.loadAccessNodeDistance()
        self.G.isTNRed = True
        print("finish loading preprocessed data!")