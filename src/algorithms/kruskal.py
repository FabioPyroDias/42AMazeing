from src.maze import Maze


def generate(maze: Maze) -> None:
    sets = {}
    for row in maze.height:
        for col in maze.width:
            sets[(row, col)] = {(row, col)}

    walls = []
    