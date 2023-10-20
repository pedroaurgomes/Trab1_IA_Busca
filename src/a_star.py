from queue import PriorityQueue

from utils import getPath

def aStar(actors, source, target):

    queue = PriorityQueue()
    queue.put((0, 0, source))
    steps = 0

    visited = {}

    # dictionary to store the parent of each node, so we can reconstruct the path 
    parent = {} 

    while not queue.empty():
        value, cost, current = queue.get()
        steps += 1

        if current == target:
            return {
                'path': getPath(parent, source, target, actors),
                'cost': cost,
                'steps': steps
            }

        for neighbor in actors[current].neighbors:
            
            g = cost + 1
            h = 0 if len(actors[target].genres) == 0 else - len(actors[neighbor].genres.intersection(actors[target].genres))/len(actors[target].genres)
            
            if visited.get(neighbor) is None or visited[neighbor] > g+h:
                queue.put((g+h, g, neighbor))
                visited[neighbor] = g+h
                parent[neighbor] = current
    
    return {
        'cost': -1
    }