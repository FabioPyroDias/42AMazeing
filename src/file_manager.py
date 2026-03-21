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
                file.write(str(value), )
            file.write("\n")
        file.write(f"{maze.entry[0]}, {maze.entry[1]}\n")
        file.write(f"{maze.exit[0]}, {maze.exit[1]}\n")
        index = 0
        while index < len(maze.path) - 1:
            current_cell = maze.path[index]
            next_cell = maze.path[index + 1]
            if current_cell[0] - next_cell[0] > 0:
                file.write("W")
            elif current_cell[0] - next_cell[0] < 0:
                file.write("E")
            elif current_cell[1] - next_cell[1] > 0:
                file.write("N")
            elif current_cell[1] - next_cell[1] < 0:
                file.write("S")
            index += 1
    file.close()
