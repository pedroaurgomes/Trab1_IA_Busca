
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

    current_directory = os.path.dirname(os.path.abspath(__file__))  # Gets the directory of the currently executing script
    parent_directory = os.path.dirname(current_directory)

    actor_data_csv_filepath = os.path.join(parent_directory, "Data", "compressed_actors_dataset.csv")  # Constructs the path
    movie_data_csv_filepath = os.path.join(parent_directory, "Data", "compressed_movies_dataset.csv")  # Constructs the path

    actors_data = parseCsv(actor_data_csv_filepath)
    movies_data = parseCsv(movie_data_csv_filepath)

    for actor_row in actors_data:
        actor = Actor(actor_row["nconst"], actor_row["primaryName"])
        actors[actor.actor_id] = actor
        for title in actor_row["knownForTitles"]:
            movie_cast.setdefault(title, []).append(actor.actor_id)




buildGraph()

# def main():
#     pass
#
# if __name__ == "__main__":
#     main()