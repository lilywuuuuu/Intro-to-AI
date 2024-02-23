import csv
edgeFile = 'edges.csv'

def openFile():
    graph = {} # start : [end1, end2, ...]
    distance = {} # (start, end) : dist

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
    return graph, distance

def findDistance(path, distance):
    dist = 0
    for i in range(len(path)-1):
        node = path[i]
        next_node = path[i+1]
        if(distance.get(node, next_node)): # if there exists a path
            dist += distance[node, next_node] # then add on to the distance
    return dist

def ucs(start, end):
    # Begin your code (Part 3)
    graph, distance = openFile()
    visited = set()
    visited.add(start)
    p_queue = [(0, [start])] # priority queue (cumulated distance, path)

    while p_queue:
        d, path = p_queue.pop(0) # pop the first item of priority queue (shortest cumulated distance)
        node = path[-1] # mark current node as the last node of this path
        visited.add(node) # mark this node as visited

        if node == end: # if reached the destination 
            dist = findDistance(path, distance) # calculate the distance between each node
            return path, dist, len(visited)

        for adj in graph.get(node, []): # if not reached the destination
            if adj not in visited: # make sure the adjacent node has not been visited
                new_path = list(path) # create new path
                new_path.append(adj) # add the adjacent node to its end
                p_queue.append((d + distance[node, adj], new_path)) # put it on pq with updated distance
                p_queue.sort() # sort it by distance so it is prioritized

    return [], 0, len(visited) # return these if no route is found
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(426882161, 1737223506)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')

