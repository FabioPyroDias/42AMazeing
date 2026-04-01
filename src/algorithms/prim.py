from src.maze_generator import MazeGenerator
import random


def generate(maze: MazeGenerator) -> None:
    """
    Generate a maze using Prim's algorithm.

    Starting from an initial cell, adds its walls to a list.

    While there are walls in that list:
    - Select a random wall
    - If the wall divides visited and unvisited cells:
    - Remove the wall
    - Mark the new cell as visited
    - Add its walls to the list

    Args:
        maze (MazeGenerator): The maze instance to be modified. The function
            directly updates its grid structure.

    Notes:
        - The function relies on:
            maze.get_neighbours() to retrieve valid adjacent cells.
            maze.remove_wall() to carve passages.
        - If animation is enabled (maze.animating), the maze is printed
          after each wall removal step.
    """

    random.seed(maze.seed)
    maze.animate()

    # This set will record the cells already visited, ensuring there's no
    #   cells visited more than once.
    visited = set()

    # This list tracks candidate walls between visited and unvisited cells.
    frontier = []

    # In the beginning, only the maze entry's neighbours are considered
    #   in the frontier.
    entry = maze.entry
    visited.add(entry)
    neighbours = maze.get_neighbours(entry)
    for neighbour in neighbours:
        frontier.append((entry, neighbour))

    # At each step:
    # 1. A random edge (current cell, neighbour) is selected from the frontier.
    # 2. If the neighbour has not been visited,
    #   the wall between them is removed.
    # 3. The neighbour is marked as visited and
    #   its neighbours are added to the frontier.
    # This process continues until there are no more frontier edges, resulting
    #   in a fully connected maze.
    while len(frontier) > 0:
        chosen_pair = random.choice(frontier)
        current, cell_neighbour = chosen_pair
        if cell_neighbour not in visited:
            maze.remove_wall(current, cell_neighbour)
            visited.add(cell_neighbour)
            neighbours = maze.get_neighbours(cell_neighbour)
            for neighbour in neighbours:
                if neighbour not in visited:
                    frontier.append((cell_neighbour, neighbour))
        frontier.remove(chosen_pair)
        maze.animate()
