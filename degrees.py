import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    def search_algorithm(frontier, explored_set):
        """
        search algorithm function

        :param frontier: frontier
        :param explored_set: explored set

        :return: Node() object
        """

        search_return = Node(None, "init", None)  # initialise dummy node from search loop
        while True: # repeat
            # 1. If the frontier is empty, Stop. There is no solution to the problem.
            if len(frontier.frontier) == 0:
                break

            # 2. Remove a node from the frontier. This is the node that will be considered.
            w_node = frontier.remove() # get the working node from frontier

            # 3. If the node contains the goal state, Return the solution. Stop.
            if (w_node.state == target):
                search_return = w_node
                break

            # Else,
            else:
                # Expand the node(find all the new nodes that could be reached from this node),
                # and add resulting nodes to the frontier.

                # get all possible (movie_id, person_id) pairs
                next_frontier_d = neighbors_for_person(w_node.state)
                next_frontier_d = { # generate dictionary like
                    m_p[1]: m_p[0] # {person: movie}
                    for m_p in next_frontier_d # from all possible (movie_id, person_id) pairs
                    if m_p[1] != w_node.state # if person_id not same as working node
                }
                # generate nodes from {person: movie} dictionary and add them to frontier
                for p_id in next_frontier_d.keys():
                    add_node = Node(p_id, w_node, next_frontier_d[p_id]) # substantiate node to add
                    if not explored_set.contains_state(add_node.state): # check if the node is not in the explored set
                        frontier.add(add_node) # add node to frontier

                # Add the current node to the explored set.
                explored_set.add(w_node)

        return search_return


    def parse_output_list(last_node, return_list=[]):
        """
        function to recursively parse last_node into output

        :param last_node: last child node
        :param return_list: cumulative list to return

        :return: 2-d list of [(movie_id, person_id), ]
        """

        if last_node.parent == "init": # reached first node
            return return_list
        else:
            # append
            next_return = return_list.copy()
            next_return.append((last_node.action, last_node.state))
            # go to parent
            return parse_output_list(last_node.parent, next_return)


    ####
    # starting node
    ####
    node0 = Node(source, "init", "init") # substantiate

    ####
    # breadth-first search
    ####
    # substantiate frontier and explored set
    frontier_queue, explored_set_queue = QueueFrontier(), QueueFrontier()
    # add starting node to frontier
    frontier_queue.add(node0)
    # run search algorithm
    bfs_res = parse_output_list(search_algorithm(frontier_queue, explored_set_queue))

    return bfs_res


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
