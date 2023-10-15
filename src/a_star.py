from queue import PriorityQueue

from utils import getPath

def aStar(actors, source, target):

    # create priority queue that sorts by the highest priority
    # the priority is the sum of the cost and the heuristic

    queue = PriorityQueue()
    queue.put((0, 0, source))
    steps = 0

    visited = {}
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