# function to get path from source to target
from ast import Return


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


def printPath(path = None):

  if(path['cost'] == -1):
    print("*---------------------*")
    print("Sorry, no edge found!")
    print("*---------------------*")
    return

  pathArray = path['path']

  print("Cost: ", path['cost'])
  print("Steps: ", path['steps'])

  print("*-----------------------------------*")
  
  for i in range(1, len(pathArray)):
    print("Actor: ", pathArray[i - 1][0])
    print("Movie: ", pathArray[i][1])
    print("Alongside with: ", pathArray[i][0])
    print("*-----------------------------------*")
