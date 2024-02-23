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

def dfs(start, end):
    # Begin your code (Part 2)
    graph, distance = openFile()
    visited = set()
    visited.add(start)
    stack = [start]
    parent = {start: -1}

    while stack:
        node = stack.pop() # pop last element (first in last out)
        if node == end: # if reached the destination 
            path = findPath(end, parent) # find the corresponding path using parent-child relationship
            dist = findDistance(path, distance) # calculate the distance between each node
            return path, dist, len(visited)
        
        for adj in graph.get(node, []): # if not reached the destination
            if adj not in visited: # make sure the adjacent node has not been visited
                stack.append(adj) # put it at the top of stack
                visited.add(adj) # mark the node as visited
                parent[adj] = node # remember its parent-child relationship

    return [], 0, len(visited) # return these if no route is found
    # End your code (Part 2)


if __name__ == '__main__':
    # dfs(2270143902, 1079387396)
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
