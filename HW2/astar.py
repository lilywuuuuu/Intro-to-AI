import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def myFunc(e):
    return e['g'] + e['h']

def openFile(end):
    graph = {} # start : [end1, end2, ...]
    distance = {} # (start, end) : dist
    h1 = {}
    h2 = {}
    h3 = {}
    with open(edgeFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            s = int(row['start'])
            e = int(row['end'])
            d = float(row['distance'])
            if s not in graph: # create a list for s if it has not been seen yet
                graph[s]=[]
            graph[s].append(e) # add the edge
            distance[s, e] = d # add the distance of the edge
    with open(heuristicFile, newline='') as csvfile: # heuristic numbers
        rows = csv.DictReader(csvfile)
        for row in rows:
            n = int(row['node'])
            d1 = float(row['1079387396'])
            d2 = float(row['1737223506'])
            d3 = float(row['8513026827'])
            h1[n] = d1
            h2[n] = d2
            h3[n] = d3
    if end == 1079387396: h = h1
    elif end == 1737223506: h = h2
    elif end == 8513026827: h = h3
    return graph, distance, h

def findPath(end, parent):
    path = []
    current = end
    while current != -1: # parent of start = -1
        path.append(current) # append the current node to path
        current = parent[current] # and move onto its parent
    path.reverse() # reverse the order so it's the correct way
    return path

def findDistance(path, distance):
    dist = 0
    for i in range(len(path)-1):
        node = path[i]
        next_node = path[i+1]
        if(distance.get(node, next_node)): # if there exists a path
            dist += distance[node, next_node] # then add on to the distance
    return dist

def astar(start, end):
    # Begin your code (Part 4)
    graph, distance, h = openFile(end)
    p_queue = [{'node': start, 'g': 0, 'h': 0}] # priority queue (node, g, h)
    closed_list = []
    parent = {start: -1} # parent of start is -1
    num_visited = 0 # remember the number of visited nodes

    while p_queue:
        l = p_queue.pop(0) # pop off first item of priority queue
        node = l['node'] 
        g_node = l['g']

        if node == end:
            if node == end: # if reached the destination 
                path = findPath(end, parent) # find the corresponding path using parent-child relationship
                dist = findDistance(path, distance) # calculate the distance between each node
                return path, dist, num_visited
        
        for adj in graph.get(node, []): # if not reached the destination
            num_visited += 1 # update visited number
            g_adj = g_node + distance[node, adj] # update distance of adjacent node
            h_adj = h[adj] # find the heuristic number of adj
            found = False 
            el = 0
            for element in p_queue:
                if element['node'] == adj: 
                    el = element
            if el: # if found element in pq
                if(g_adj + h_adj > el['g'] + el['h']): 
                    # if the f of the found element is less than the one found here
                    # then don't update the node
                    found = True
            for element in closed_list:
                if element['node'] == adj:
                    el = element
            if el: # if found element in the closed list
                if(g_adj + h_adj > el['g'] + el['h']):
                    # if the f of the found element is less than the one found here
                    # then don't update the node
                    found = True
            if not found: # if no node is found in the lists or they're greater in distance
                p_queue.append({'node': adj, 'g': g_adj, 'h': h_adj}) # add new node to pq
                p_queue.sort(key=myFunc) # sort pq by f
                parent[adj] = node # remember its parent-child relationship

        closed_list.append(l) # append node to closed list

    return [], 0, num_visited # return these if no route is found
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
