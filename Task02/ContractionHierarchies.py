from Graph import *
import heapq

class ContractionHierarchies():
    def __init__(self, graph : Graph) -> None:
        self.G = graph
        self.INF = graph.INF
        self.NumNodes = graph.NumNodes
        self.Rank = graph.Rank
        self.Dist = [self.INF] * self.NumNodes
        self.Node_level = [0] * graph.NumNodes
        self.contracted = [False] * graph.NumNodes
        self.NodesOrder = [(0, 0)] * self.NumNodes
        self.Shortcuts = []
        self.ProcessingNodes = []
        self.is_contracting = False
        self.Settled = [False] * self.NumNodes
        self.queue = [[]] * 2
        self.dist = [[self.INF] * self.NumNodes] * 2
        self.visited = [[False] * self.NumNodes] * 2
        self.trace = [[-1] * self.NumNodes] * 2

    def getNodesOrder(self):
        for node in range(self.NumNodes):
            importance = self.contractNode(node)
            self.NodesOrder[node] = (importance, node)
        heapq.heapify(self.NodesOrder)

    def getInEdges(self, u):
        return self.G.adj[1][u]
    
    def getOutEdges(self, u):
        return self.G.adj[0][u]
    
    def getSumContractedNeighborsAndNodeLevel(self, node):
        contracted_neighbors = 0
        level = 0

        incoming = self.getInEdges(node)
        outgoing = self.getOutEdges(node)

        for in_edge in incoming:
            if self.Rank[in_edge[1]] != self.INF:
                contracted_neighbors += 1
                if self.Node_level[in_edge[1]] > level:
                    level = self.Node_level[in_edge[1]]
        
        for out_edge in outgoing:
            if self.Rank[out_edge[1]] != self.INF:
                contracted_neighbors += 1
                if self.Node_level[out_edge[1]] > level:
                    level = self.Node_level[out_edge[1]]
        
        return contracted_neighbors + level + 1

    def updateNeighborsNodeLevel(self, node):
        incoming = self.getInEdges(node)
        outcoming = self.getOutEdges(node)

        node_level = self.Node_level[node] + 1

        for in_edge in incoming:
            if self.Node_level[in_edge[1]] < node_level:
                self.Node_level[in_edge[1]] = node_level

        for out_edge in outcoming:
            if self.Node_level[out_edge[1]] < node_level:
                self.Node_level[out_edge[1]] = node_level
    
    def contractNode(self, node):
        self.Shortcuts.clear()

        incoming = self.getInEdges(node)
        outgoing = self.getOutEdges(node)
        
        cover_shortcuts = 0
        numShortcuts = 0
       
        for in_edge in incoming:
            if self.Rank[in_edge[1]] < self.Rank[node] or not outgoing:
                continue

            #Find distance from in_node to all local nodes
            self.LocalDijkstra(in_edge[1], self.G.max_in[node] + self.G.max_out[node], node)
            #print(in_node, self.Dist)
            shortcut_added = False
            for out_edge in outgoing:

                if self.Rank[out_edge[1]] < self.Rank[node] or in_edge[1] == out_edge[1]:
                    continue

                if self.Dist[out_edge[1]] > in_edge[0] + out_edge[0]:
                    numShortcuts += 1
                    shortcut_added = True
                    if self.is_contracting:
                        path = in_edge[3].copy()
                        path.append(node)
                        path.extend(out_edge[3])
                        should_add = True
                        coor_path = in_edge[4].copy()
                        coor_path.extend(out_edge[4])
                        for i, shortcut in enumerate(self.Shortcuts):
                            if shortcut[0] == in_edge[1] and shortcut[1] == out_edge[1]:
                                if shortcut[2] > in_edge[0] + out_edge[0]:
                                    self.Shortcuts[i] = (in_edge[1], out_edge[1], in_edge[0] + out_edge[0], path, coor_path)
                                should_add = False
                        if should_add:
                            self.Shortcuts.append((in_edge[1], out_edge[1], in_edge[0] + out_edge[0], path, coor_path))
            
            if shortcut_added:
                cover_shortcuts += 1
            for visited_node in self.ProcessingNodes:
                self.Dist[visited_node] = self.INF
                self.Settled[visited_node] = False
            self.ProcessingNodes = []
        
        importance = numShortcuts - len(incoming) - len(outgoing) + cover_shortcuts + self.getSumContractedNeighborsAndNodeLevel(node) 
       
        return importance
    
    def LocalDijkstra(self, start, limit, contract_node):
        queue = []
        queue.append((0, start))
        self.ProcessingNodes.append(start)
        self.Dist[start] = 0

        while queue:
            u_distance, u = heapq.heappop(queue)

            if self.Dist[u] > limit:
                break

            if self.Settled[u]:
                continue
            
            self.Settled[u] = True
            neighbors = self.getOutEdges(u)

            for edge in neighbors:

                if self.Rank[edge[1]] < self.Rank[contract_node] or edge[1] == contract_node:
                    continue
                
                if self.Dist[edge[1]] > self.Dist[u] + edge[0]:
                    self.Dist[edge[1]] = self.Dist[u] + edge[0]
                    heapq.heappush(queue, (self.Dist[edge[1]], edge[1]))
                    self.ProcessingNodes.append(edge[1])

    def removeEdges(self):
        numEdge = 0
        for i in range(self.G.NumNodes):
            for j in range(len(self.G.adj[0][i]) -1, -1, -1):
                if self.Rank[i] > self.Rank[self.G.adj[0][i][j][1]]:
                    self.G.adj[0][i].pop(j)
                    continue
                self.G.adj[0][i][j] = (self.G.adj[0][i][j][0], self.G.adj[0][i][j][1], numEdge, self.G.adj[0][i][j][3], self.G.adj[0][i][j][4])
                numEdge += 1
                self.G.ListEdges.append((i, self.G.adj[0][i][j][1], self.G.adj[0][i][j][0], self.G.adj[0][i][j][3], self.G.adj[0][i][j][4]))
            for j in range(len(self.G.adj[1][i]) -1, -1, -1):
                if self.Rank[i] > self.Rank[self.G.adj[1][i][j][1]]:
                    self.G.adj[1][i].pop(j)
                    continue
                self.G.adj[1][i][j] = (self.G.adj[1][i][j][0], self.G.adj[1][i][j][1], numEdge, self.G.adj[1][i][j][3], self.G.adj[1][i][j][4])
                numEdge += 1
                self.G.ListEdges.append((self.G.adj[1][i][j][1], i, self.G.adj[1][i][j][0], self.G.adj[1][i][j][3], self.G.adj[1][i][j][4]))
                
    def Preprocessing(self, forTNR = False):
        start = time.time()
        self.getNodesOrder()
        cur_rank = 0
        self.is_contracting = True
        while self.NodesOrder:
            importance, node = heapq.heappop(self.NodesOrder)
            check_importance = self.contractNode(node)
            if len(self.NodesOrder) == 0 or check_importance <= self.NodesOrder[0][0]:
                for shortcut in self.Shortcuts:
                    self.G.addEdge(shortcut[0], shortcut[1], shortcut[2], path= shortcut[3], list_coor= shortcut[4])
                self.updateNeighborsNodeLevel(node)
                self.Rank[node] = cur_rank
                cur_rank += 1
            else:
                heapq.heappush(self.NodesOrder, (check_importance, node))
        #if not forTNR:
        self.removeEdges()
        end = time.time()
        self.G.isCHed = True
        #print(f"Number of Edges after preprocessing: {len(self.G.ListEdges)}")
        print(f"CH preprocessed in: {round(end - start, 4)} seconds")

    def getPath(self, estimate, middle_node, forward_trace, backward_trace):
        if estimate == self.INF or middle_node == -1:
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
        end = time.time()
        #print(f"Get path in {end - start} seconds")
        return path, path_coor
        
    def BidirectionalSearch(self, start, end):
        forward_queue = []
        backward_queue = []
        forward_dist = [self.INF] * self.NumNodes
        backward_dist = [self.INF] * self.NumNodes
        forward_dist[start] = 0
        backward_dist[end] = 0
        forward_visited = [False] * self.NumNodes
        backward_visited = [False] * self.NumNodes
        heapq.heappush(forward_queue, (0, start))
        heapq.heappush(backward_queue, (0, end))
        estimate = self.INF
        middle_node = -1
        forward_trace = [-1] * self.NumNodes
        backward_trace = [-1] * self.NumNodes
        search_space = 0
        
        while forward_queue or backward_queue:
            if forward_queue:
                dist, u = heapq.heappop(forward_queue)
                forward_visited[u] = True
                search_space += 1
                #0: weight, 1: neighbor, 2: edge index, 3: path
                #check for condition to process
                in_neighbors = self.getInEdges(u)
                to_process = True
                """for in_edge in in_neighbors:
                    if forward_dist[u] > forward_dist[in_edge[1]] + in_edge[0]:
                        to_process = False
                        break"""
                
                #process a node if needed
                if to_process and forward_dist[u] <= estimate:
                    out_neighbors = self.getOutEdges(u)
                    for out_edge in out_neighbors:
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
                search_space += 1
                #check for condition to process
                out_neighbors = self.getOutEdges(u)
                to_process = True
                """for out_edge in out_neighbors:
                    if backward_dist[u] > backward_dist[out_edge[1]] + out_edge[0]:
                        to_process = False
                        break"""
                
                #process a node if needed
                if to_process and backward_dist[u] <= estimate:
                    in_neighbors = self.getInEdges(u)
                    for in_edge in in_neighbors:
                        if backward_dist[in_edge[1]] > backward_dist[u] + in_edge[0]:
                            backward_dist[in_edge[1]] = backward_dist[u] + in_edge[0]
                            heapq.heappush(backward_queue, (backward_dist[in_edge[1]], in_edge[1]))
                            backward_trace[in_edge[1]] = in_edge[2]

                #check if the node u has been visited in the backward search:
                if forward_visited[u] and forward_dist[u] + backward_dist[u] < estimate:
                    estimate = forward_dist[u] + backward_dist[u]
                    middle_node = u
        path, path_coor = self.getPath(estimate, middle_node, forward_trace, backward_trace)
        return (estimate, path, path_coor, search_space)

        