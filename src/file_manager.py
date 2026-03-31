from src.maze_generator import MazeGenerator


def save_file(maze: MazeGenerator):
    """
    Save the generated maze to a file using the required output format.

    Each cell is encoded as a single hexadecimal digit representing
    which walls are closed:
        - Bit 0: North
        - Bit 1: East
        - Bit 2: South
        - Bit 3: West

    The maze is written row by row, followed by:
        - An empty line
        - Entry coordinates
        - Exit coordinates
        - The shortest path from entry to exit, encoded as directions
          using the letters N, E, S, W.

    Args:
        maze (MazeGenerator): The maze instance containing the grid,
            entry and exit points, output filename, and shortest path.

    Notes:
        - The output file is overwritten if it already exists.
    """

    with open(maze.output, 'w') as file:
        for row in range(maze.height):
            for col in range(maze.width):
                # Sum the bit values of each wall and convert it to hex.
                # Furthermore, exclude the "0b" indicator from the hex value.
                value = (8 * maze.grid[row][col][3] +
                         4 * maze.grid[row][col][2] +
                         2 * maze.grid[row][col][1] +
                         maze.grid[row][col][0])
                value = hex(value)[2:]
                file.write(str(value))
            file.write("\n")
        file.write("\n")
        # Write both maze entry and maze exit coordinates.
        file.write(f"{maze.entry[0]}, {maze.entry[1]}\n")
        file.write(f"{maze.exit[0]}, {maze.exit[1]}\n")
        index = 0
        # Convert shortest path from entry to exit to encoded directions.
        # Taking into account the current cell:
        # - If the subtraction of the x coordinate of current cell with
        #       next cell is negative, traveled right. Encoded E (East).
        # - If the subtraction of the x coordinate of current cell with
        #       next cell is positive, traveled left. Encoded W (West).
        # - If the subtraction of the y coordinate of current cell with
        #       next cell is negative, traveled upwards. Encoded N (North).
        # - If the subtraction of the y coordinate of current cell with
        #       next cell is positive, traveled downwards. Encoded S (South).
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
        file.write("\n")
    file.close()
