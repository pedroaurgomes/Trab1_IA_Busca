# function to get path from source to target
def getPath(parent, source, target, actors):
    path = []
    current = target
    while current != source:
        # get a commum movie between the current actor and its parent
        common_movie = list(actors[current].movies.intersection(actors[parent[current]].movies))
        path.append((actors[current].name, common_movie[0]))
        current = parent[current]
    common_movie = list(actors[current].movies.intersection(actors[parent[current]].movies))
    path.append((actors[current].name, common_movie[0]))
    path.reverse()
    return path
