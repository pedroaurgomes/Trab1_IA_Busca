import csv
import os
import random
import json
import matplotlib.pyplot as plt

from a_star import aStar
from bfs import bfs
from utils import printPath
from analysis import experimentAnalysis, graphAnalysis

class Actor():
    """
    Represents a node in a graph for an actor.

    Attributes:
    - actor_id (int/str): A unique identifier for the actor.
    - name (str): The name of the actor.
    - neighbors (set): A set of actor_ids representing other actors who have co-starred 
                       in a movie with this actor. It helps in representing the graph edges.
    - genres (set): A set of genres representing the different types of movies the actor 
                    has participated in.
    - movies (set): A set of movie IDs representing the movies in which the actor 
                    has participated.
    """
    def __init__(self,actor_id,name):
        self.actor_id = actor_id
        self.name = name
        self.neighbors = set() # lista de actor_id, teremos um dicionário: id=>objeto actor
        self.genres = set()
        self.movies = set()


def parseCsv(filename):
    content = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(reader)
        for row in reader:
            data = {}
            for i in range(len(header)):
                data[header[i]] = row[i]
            content.append(data)
    return content

def buildGraph():
    movie_cast = {} # movie_id -> actors_id of the movie
    actors = {} # actor_id -> actor object
    movie_genres = {} # movie_id -> genres of the movie
    movie_names = {} # movie_id -> movie name

    current_directory = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the currently executing script
    parent_directory = os.path.dirname(current_directory)

    actor_data_csv_filepath = os.path.join(parent_directory, "Data", "data_actors_final.csv")  # Constructs the path
    movie_data_csv_filepath = os.path.join(parent_directory, "Data", "data_movies_final.csv")  # Constructs the path

    actors_data = parseCsv(actor_data_csv_filepath)
    movies_data = parseCsv(movie_data_csv_filepath)

    # Build a dictionary of movie names and genres
    for movie in movies_data:
        movie_id = movie['tconst']
        movie_names[movie_id] = movie['primaryTitle']
        movie_genres[movie_id] = movie['genres'].split(',')

    # Build the nodes and the actors dictionary
    for actor_row in actors_data:
        actor = Actor(actor_row["nconst"], actor_row["primaryName"])
        actors[actor.actor_id] = actor
        
        if actor_row["knownForTitles"] == '\\N':
            continue
        
        actor_row["knownForTitles"] = actor_row["knownForTitles"].split(',')
        for title in actor_row["knownForTitles"]:
            if title not in movie_names:
                continue
            
            actor.movies.add(movie_names[title])
            movie_cast.setdefault(title, []).append(actor.actor_id)
            actor.genres.update(movie_genres[title])

    for movie_name, cast in movie_cast.items():
        # Add edges between all pairs of actors in this movie
        for i in range(len(cast)):
            for j in range(i+1, len(cast)):
               actors[cast[i]].neighbors.add(actors[cast[j]].actor_id)
               actors[cast[j]].neighbors.add(actors[cast[i]].actor_id)

    return actors

def runExperiments(actors, n):

    exp = 1
    results = []

    while(exp <= n):

        # get a random source and target
        source_id = random.choice(list(actors.keys()))
        target_id = random.choice(list(actors.keys()))

        # run and print the results
        print("Experiment ", exp, ":")
        print("Source: ", actors[source_id].name)
        print("Target: ", actors[target_id].name)
        print("BFS results:")
        bfsResult = bfs(actors, source_id, target_id)
        printPath(bfsResult)
        print("A* results:")
        aStarResult = aStar(actors, source_id, target_id)
        printPath(aStarResult)
        print("\n")

        

        results.append({
            'source': actors[source_id].name,
            'target': actors[target_id].name,
            'bfs': bfs(actors, source_id, target_id),
            'a_star': aStar(actors, source_id, target_id)
        })

        exp += 1

    # write results to a json file
    with open('results.json', 'w') as outfile:
        json.dump(results, outfile)



actors = buildGraph()
runExperiments(actors, 100)
graphAnalysis(actors)
experimentAnalysis()