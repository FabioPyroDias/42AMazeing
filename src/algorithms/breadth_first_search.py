from src.maze_generator import MazeGenerator


def find_path(maze: MazeGenerator) -> list[tuple[int, int]]:
    """
    Find the shortest path from the maze entry to the exit using
    Breadth-First Search (BFS).

    This function explores the maze starting from the entry cell and
    guarantees the shortest path (in number of steps) to the exit.

    Args:
        maze (MazeGenerator): The maze instance containing the grid,
            entry and exit positions, and connectivity information.

    Returns:
        list[tuple[int, int]]: A list of (x, y) coordinates representing
        the shortest path from entry to exit, inclusive. The first element
        is the entry point and the last is the exit point.

    Notes:
        - This function relies on `maze.get_connected_neighbours()` to
          determine accessible adjacent cells.
        - The algorithm uses a queue to ensure breadth-first traversal.
        - A registry (parent map) is used to reconstruct the path once
          the exit is reached.
    """

    # This list acts as queue. First In First Out (FIFO).
    # A new cell is added at the tail of the list and the very
    # first cell is removed.
    queue = [maze.entry]

    # This set will record the cells already visited, ensuring there's no
    # cells visited more than once.
    visited = set()

    # This dict will act as a map to track the path of each cell.
    # Key = Current Cell
    # Value = Previous Cell
    # The registry stores each cell's parent
    #   (the cell from which it was reached).
    # By tracing each cell back to its parent repeatedly, we reconstruct
    # the path from the exit to the entry.
    registry = {}

    # The algorithm follows these steps:
    # 1. Get current cell in the queue and get their connected neighbours
    #       (Cells that don't have a wall between them and the current cell)
    # 2. Add current cell to the visited set.
    # 3. For each neighbour, check if it hasn't been visited.
    # 4. Add neighbour to the visited set.
    # 5. Register the neighbour as the key and the current cell
    #        as the value in the registry.
    #        Again, this will keep track of the path so far.
    # 6. Append the neighbour cell to the queue.
    #        Eventually, this cell will be analyzed.
    # 7. Check in the neighbour is the maze exit. If it is:
    # 7.1.   The path between maze entry and maze exit starts to be created
    #            Initially, the path will start on the maze exit
    #            and transverse to the maze entry.
    # 7.2.   Accessing the keys and values of the register,
    #            all cells are added to the path.
    # 7.3.   The path is reversed. Now maze entry is the start
    #            and the end is the maze exit.
    while len(queue) != 0:
        current_cell = queue.pop(0)
        neighbours = maze.get_connected_neighbours(current_cell)
        visited.add(current_cell)
        for neighbour in neighbours:
            if neighbour in visited:
                continue
            visited.add(neighbour)
            registry[neighbour] = current_cell
            queue.append(neighbour)
            if neighbour == maze.exit:
                path = [neighbour]
                previous = neighbour
                while current_cell != maze.entry:
                    current_cell = registry[previous]
                    path.append(current_cell)
                    previous = current_cell
                path.reverse()
                return path
