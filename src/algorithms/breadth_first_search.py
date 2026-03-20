from src.maze import Maze


def find_path(maze: Maze):
    queue = [maze.entry]
    visited = set()
    registry = {}
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
