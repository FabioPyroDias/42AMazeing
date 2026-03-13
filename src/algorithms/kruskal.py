from src.maze import Maze
import random


def generate(maze: Maze) -> None:
    random.seed(maze.seed)
    sets = {}
    for row in range(maze.height):
        for col in range(maze.width):
            sets[(col, row)] = {(col, row)}

    walls = []
    for row in range(maze.height):
        for col in range(maze.width):
            if col + 1 < maze.width:
                walls.append(((col, row), (col + 1, row)))
            if row + 1 < maze.height:
                walls.append(((col, row), (col, row + 1)))

    random.shuffle(walls)

    for current, neighbour in walls:
        pathA = sets[current]
        pathB = sets[neighbour]
        if pathA is not pathB:
            maze.remove_wall(current, neighbour)
            new_path = pathA.union(pathB)
            for cell in new_path:
                sets[cell] = new_path
