from src.maze import Maze
import random


def generate(maze: Maze):
    random.seed(maze.seed)
    entry = maze.entry

    visited = set()
    frontier = []

    visited.add(entry)
    neighbours = maze.get_neighbours(entry)
    for neighbour in neighbours:
        frontier.append((entry, neighbour))
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
