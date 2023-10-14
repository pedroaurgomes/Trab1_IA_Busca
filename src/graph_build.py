
import csv
import os

class Actor():
    """"A node in the graph """
    def __init__(self,actor_id,name):
        self.actor_id = actor_id
        self.name = name
        self.neighbors = set() # lista de actor_id, teremos um dicionário: id=>objeto actor
        self.genres = set()


def parseCsv(filename):
    print("Tamo na parse")
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

    current_directory = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the currently executing script
    parent_directory = os.path.dirname(current_directory)

    actor_data_csv_filepath = os.path.join(parent_directory, "Data", "compressed_actors_dataset.csv")  # Constructs the path
    movie_data_csv_filepath = os.path.join(parent_directory, "Data", "compressed_movies_dataset.csv")  # Constructs the path

    actors_data = parseCsv(actor_data_csv_filepath)
    movies_data = parseCsv(movie_data_csv_filepath)

    for movie in movies_data:
        movie_id = movie['tconst']
        movie_genres[movie_id] = movie['genres'].split(',')

    for actor_row in actors_data:
        actor = Actor(actor_row["nconst"], actor_row["primaryName"])
        actors[actor.actor_id] = actor
        if actor_row["knownForTitles"] == '\\N':
            continue
        actor_row["knownForTitles"] = actor_row["knownForTitles"].split(',')
        for title in actor_row["knownForTitles"]:
            print(title)
            movie_cast.setdefault(title, []).append(actor.actor_id)
            if title in movie_genres:
                actor.genres.update(movie_genres[title])

    for movie_name, cast in movie_cast.items():
        # Add edges between all pairs of actors in this movie
        for i in range(len(cast)):
            for j in range(i+1, len(cast)):
               actors[cast[i]].neighbors.add(actors[cast[j]].actor_id)
               actors[cast[j]].neighbors.add(actors[cast[i]].actor_id)

    return actors


actors = buildGraph()
# print actors
for key, actor in actors.items():
    print(actor.name, actor.actor_id, actor.genres, actor.neighbors)

# def main():
#     pass
#
# if __name__ == "__main__":
#     main()