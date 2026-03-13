from src.maze import Maze
import random


def generate(maze: Maze):
    random.seed(maze.seed)
    visited = set()
    carve_path(maze, visited, maze.entry)


def carve_path(maze: Maze, visited: set, cell: tuple):
    if cell not in visited:
        visited.add(cell)
        neighbours = maze.get_neighbours(cell)
        random.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour not in visited:
                maze.remove_wall(cell, neighbour)
                carve_path(maze, visited, neighbour)
