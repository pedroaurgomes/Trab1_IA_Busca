from queue import Queue
from utils import getPath


def bfs(actors, source, target):

    visited = set()

    queue = Queue()

    # dictionary to store the parent of each node, so we can reconstruct the path
    parent = {}

    queue.put((source, 0))
    visited.add(source)

    steps = 0

    while not queue.empty():

        actor_id, cost = queue.get()
        steps += 1

        if actor_id == target:
            return {
                'path': getPath(parent, source, target, actors),
                'cost': cost,
                'steps': steps
            }

        for neighbor in actors[actor_id].neighbors:
            if parent.get(neighbor) is None:
                queue.put((neighbor, cost+1))
                parent[neighbor] = actor_id
                visited.add(neighbor)

    return {
        'cost': -1
    }
