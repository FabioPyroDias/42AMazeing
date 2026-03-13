from src.maze import Maze


def save_file(maze: Maze):
    with open(maze.output, 'w') as file:
        for row in range(maze.height):
            for col in range(maze.width):
                value = (8 * maze.grid[row][col][3] +
                         4 * maze.grid[row][col][2] +
                         2 * maze.grid[row][col][1] +
                         maze.grid[row][col][0])
                value = hex(value)[2:]
                file.write(str(value))
            file.write("\n")
    file.close()
