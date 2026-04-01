from src.maze_generator import MazeGenerator
import random


def generate(maze: MazeGenerator) -> None:
    """
    Generate a maze using the Recursive Backtracking algorithm
    (Depth-First Search, DFS).

    Starts the recursive carving process from the maze entry point.

    Args:
        maze (MazeGenerator): The maze instance to be generated.

    Notes:
        - If animation is enabled (maze.animating), the maze is printed
          after each wall removal step.
    """

    random.seed(maze.seed)
    maze.animate()

    # This set will record the cells already visited, ensuring there's no
    #   cells visited more than once.
    visited: set[tuple[int, int]] = set()
    carve_path(maze, visited, maze.entry)


def carve_path(maze: MazeGenerator, visited: set[tuple[int, int]],
               cell: tuple[int, int]) -> None:
    """
    Recursively carve paths in the maze using Depth-First Search (DFS).

    Starting from the initial cell, randomly visits a neighbouring cell and
    removes the wall between them.
    This neighbour becomes the new current cell and the process
    continues recursively.
    When a cell has no unvisited neighbours,
    the algorithm backtracks to the previous cell.

    Args:
        maze (MazeGenerator): The maze being generated.
        visited (set): A set of already visited cells.
        cell (tuple[int, int]): The current cell being processed.

    Notes:
        - This is a recursive algorithm and may hit recursion limits
        for very large mazes. Max 30x30
    """

    if cell not in visited:
        visited.add(cell)
        neighbours = maze.get_neighbours(cell)
        random.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour not in visited:
                maze.remove_wall(cell, neighbour)
                maze.animate()
                carve_path(maze, visited, neighbour)
