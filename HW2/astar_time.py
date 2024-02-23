import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'

def myFunc(e):
    return e['g'] + e['h']

def openFile(end):
    graph = {} # start : [end1, end2, ...]
    distance = {} # (start, end) : dist
    time = {}
    h1 = {}
    h2 = {}
    h3 = {}
    sl = 80 # estimated speed limit
    with open(edgeFile, newline='') as csvfile:
        rows = csv.DictReader(csvfile)
        for row in rows:
            s = int(row['start'])
            e = int(row['end'])
            d = float(row['distance'])
            sp = float(row['speed limit'])
            if s not in graph:
                graph[s]=[] # create a list for s if it has not been seen yet
            graph[s].append(e) # add the edge
            distance[s, e] = d # add the distance of the edge
            time[s, e] = (d/sp)*3.6 # add the time of travel of the edge
    with open(heuristicFile, newline='') as csvfile: # heuristic numbers
        rows = csv.DictReader(csvfile)
        for row in rows:
            n = int(row['node'])
            d1 = float(row['1079387396'])
            d2 = float(row['1737223506'])
            d3 = float(row['8513026827'])
            h1[n] = d1/(sl/3.6)
            h2[n] = d2/(sl/3.6)
            h3[n] = d3/(sl/3.6)
    if end == 1079387396: h = h1
    elif end == 1737223506: h = h2
    elif end == 8513026827: h = h3
    return graph, distance, h, time

def findPath(end, parent):
    path = []
    current = end
    while current != -1: # parent of start = -1
        path.append(current) # append the current node to path
        current = parent[current] # and move onto its parent
    path.reverse() # reverse the order so it's the correct way
    return path

def findTime(path, time):
    t = 0
    for i in range(len(path)-1):
        node = path[i]
        next_node = path[i+1]
        if(time.get(node, next_node)): # if there exists a path
            t += time[node, next_node] # then add on to the distance
    return t

def astar_time(start, end):
    # Begin your code (Part 6)
    graph, distance, h, time = openFile(end)
    p_queue = [{'node': start, 'g': 0, 'h': 0}]
    closed_list = []
    parent = {}
    parent[start] = -1
    num_visited = 0

    while p_queue:
        l = p_queue.pop(0)
        node = l['node']
        g_node = l['g']

        if node == end: # if reached the destination 
            path = findPath(end, parent) # find the corresponding path using parent-child relationship
            dist = findTime(path, time) # calculate the time between each node
            return path, dist, num_visited
        
        for adj in graph.get(node, []): # if not reached the destination
            num_visited += 1 # update visted number
            g_adj = g_node + time[(node, adj)] # update distance of adjacent node
            h_adj = h[adj] # find the heuristic number of adj
            el = 0
            found = False
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
            if el: # if found element in closed list
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
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(1718165260, 8513026827)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
