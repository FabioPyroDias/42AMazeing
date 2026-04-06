from src.maze_generator import MazeGenerator
import random


def generate(maze: MazeGenerator) -> None:
    """
    Generate a maze using Kruskal's algorithm.

    Each cell starts as an independent set, meaning no cells are connected.
    All walls between adjacent cells are listed and shuffled randomly.

    For each wall:
    - Check the two cells separated by the wall
    - If they belong to different sets:
      - Remove the wall
      - Merge the two sets into one

    This ensures that no cycles are created during generation,
        producing a perfect maze.
    The algorithm continues until all cells belong to a single connected set.

    Args:
        maze (MazeGenerator): The maze instance where the grid will be
            modified in-place.

    Notes:
        - Each cell starts in its own set.
        - A list of all possible walls between adjacent cells is created
          and shuffled randomly.
        - For each wall, if the two cells belong to different sets, the
          wall is removed and the sets are merged.
        - If animation is enabled (maze.animating), the maze is printed
          after each wall removal step.
    """

    random.seed(maze.seed)
    maze.animate()

    # This dictionary will store all the connected cells to the current cell.
    # Each cell starts in its own set.
    sets = {}
    for row in range(maze.height):
        for col in range(maze.width):
            sets[(col, row)] = {(col, row)}

    # A list of all possible walls between adjacent cells is created.
    # To avoid duplicates, each cell appends both West and
    #   South walls, if possible.
    # These are represented by a tuple of both cells.
    walls = []
    for row in range(maze.height):
        for col in range(maze.width):
            if col + 1 < maze.width:
                walls.append(((col, row), (col + 1, row)))
            if row + 1 < maze.height:
                walls.append(((col, row), (col, row + 1)))

    random.shuffle(walls)

    # For each tuple, if they belong to different sets, the wall between
    #   both cells is removed and the sets are united.
    # The sets are updated on each cell that belongs to this new set.
    for current, neighbour in walls:
        pathA = sets[current]
        pathB = sets[neighbour]
        if maze.has_pattern:
            if current not in maze.pattern and neighbour not in maze.pattern:
                if pathA is not pathB:
                    maze.remove_wall(current, neighbour)
                    new_path = pathA.union(pathB)
                    for cell in new_path:
                        sets[cell] = new_path
                maze.animate()
