import os
import random
import time


PATTERN_42 = [
    (-3, -2), (1, -2), (2, -2), (3, -2),
    (-3, -1), (3, -1),
    (-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
    (-1, 1), (1, 1),
    (-1, 2), (1, 2), (2, 2), (3, 2)
]


class MazeGenerator():
    """
    Maze generator class.

    This class encapsulates all logic related to maze creation, manipulation,
        visualization, and solving.

    It supports multiple generation algorithms (Prim, Kruskal, DFS),
        optional imperfections, pathfinding, and animated rendering.

    Attributes:
        width (int): Width of the maze.
        height (int): Height of the maze.
        entry (tuple[int, int]): Entry cell coordinates.
        exit (tuple[int, int]): Exit cell coordinates.
        seed (int): Random seed used for reproducibility.
        algorithm (str): Maze generation algorithm name.
        perfect (bool): Whether the maze should be perfect (no loops).
        grid (list): Internal grid representation of the maze.
        path (list): Shortest path from entry to exit.
        animating (bool): Whether generation is animated.
    """

    def __init__(self, configs: dict) -> None:
        """
        Initialize the maze generator with configuration parameters.

        Args:
            configs (dict): Dictionary containing configuration values such as:
                WIDTH, HEIGHT, ENTRY, EXIT, SEED, ALGORITHM, etc.

        Notes:
            - Default values are used if keys are missing.
            - A special "42" pattern may be embedded
                in the maze if size allows.
            - Raises ValueError if entry or exit conflict with the pattern.
        """

        self.width = configs.get("WIDTH", 11)
        self.height = configs.get("HEIGHT", 11)
        self.entry = configs.get("ENTRY", (0, 0))
        self.exit = configs.get("EXIT", (10, 10))
        self.output = configs.get("OUTPUT_FILE", "maze_txt")
        self.perfect = configs.get("PERFECT", True)
        self.seed = configs.get("SEED", 42)
        self.algorithm = configs.get("ALGORITHM", "Prim")

        self.grid = [
            [[1, 1, 1, 1] for _ in range(self.width)]
            for _ in range(self.height)
        ]

        self.has_pattern = self.width > 10 and self.height > 10
        if not self.has_pattern:
            print("The '42' pattern is omitted. Size does not allow it")

        #Changing 42 pattern coordinates to center it
        self.pattern = [(x + self.width // 2, y + self.height // 2) for x, y in PATTERN_42]
        if self.has_pattern and (self.entry in self.pattern or self.exit in self.pattern):
            raise ValueError("Value Error: Entry or Exit in 42 Pattern")

        self.display_path = False

        self.current_color = 0
        self.colors = {
            0: {
                "walls": "\033[97;107m\u2588\033[0m",
                "42": "\033[90;100m\u2588\033[0m",
                "entry": "\033[37;45m \033[0m",
                "exit": "\033[31;41m \033[0m",
                "path": "\033[37;46m \033[0m"
            },
            1: {
                "walls": "\033[91;41m\u2588\033[0m",
                "42": "\033[97;107m\u2588\033[0m",
                "entry": "\033[92;102m \033[0m",
                "exit": "\033[95;105m \033[0m",
                "path": "\033[94;104m \033[0m"
            }
        }

        self.animating = False

    def generate(self) -> None:
        """
        Generate the maze using the selected algorithm.

        This method:
            1. Selects the generation algorithm.
            2. Builds the maze structure.
            3. Optionally introduces imperfections (loops).
            4. Computes the shortest path from entry to exit.
            5. Displays the maze.

        Args:
            None

        Returns:
            None

        Notes:
            - Algorithms are dynamically imported to avoid circular imports.
            - The maze is modified in-place.
        """

        from src.algorithms import prim, kruskal, recursive_backtracking
        ALGORITHMS = {
            "Prim": prim.generate,
            "Kruskal": kruskal.generate,
            "DFS": recursive_backtracking.generate
        }

        ALGORITHMS[self.algorithm](self)
        if not self.perfect:
            self.make_imperfect()

        from src.algorithms.breadth_first_search import find_path
        self.path = find_path(self)
        self.print_grid()

    def regenerate(self) -> None:
        """
        Reset and generate a new maze with a new random seed.

        This method:
            - Clears the current grid.
            - Generates a new random seed.
            - Rebuilds the maze.

        Args:
            None

        Returns:
            None

        Notes:
            - If animation is enabled,
                the path display is disabled during regeneration.
        """

        self.reset()
        self.seed = random.randint(0, 2147483647)
        if self.animating:
            self.display_path = False
        self.generate()

    def remove_wall(self, current: tuple, neighbour: tuple) -> None:
        """
        Remove the wall between two adjacent cells.

        Args:
            current (tuple[int, int]): Current cell coordinates.
            neighbour (tuple[int, int]): Adjacent cell coordinates.

        Returns:
            None

        Notes:
            - Updates both cells to maintain consistency.
        """

        if current[0] - neighbour[0] < 0:
            self.grid[current[1]][current[0]][1] = 0
            self.grid[neighbour[1]][neighbour[0]][3] = 0
        elif current[0] - neighbour[0] > 0:
            self.grid[current[1]][current[0]][3] = 0
            self.grid[neighbour[1]][neighbour[0]][1] = 0
        elif current[1] - neighbour[1] < 0:
            self.grid[current[1]][current[0]][2] = 0
            self.grid[neighbour[1]][neighbour[0]][0] = 0
        elif current[1] - neighbour[1] > 0:
            self.grid[current[1]][current[0]][0] = 0
            self.grid[neighbour[1]][neighbour[0]][2] = 0

    def get_neighbours(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Return valid neighbouring cells (ignoring walls).

        Args:
            cell (tuple[int, int]): The reference cell.

        Returns:
            list[tuple[int, int]]: List of adjacent valid cells.

        Notes:
            - Respects maze boundaries.
            - Excludes cells belonging to the "42" pattern if active.
        """

        neighbours = []
        if cell[0] - 1 >= 0:
            if self.has_pattern:
                if (cell[0] - 1, cell[1]) not in self.pattern:
                    neighbours.append((cell[0] - 1, cell[1]))
            else:
                neighbours.append((cell[0] - 1, cell[1]))
        if cell[1] - 1 >= 0:
            if self.has_pattern:
                if (cell[0], cell[1] - 1) not in self.pattern:
                    neighbours.append((cell[0], cell[1] - 1))
            else:
                neighbours.append((cell[0], cell[1] - 1))
        if cell[0] + 1 < self.width:
            if self.has_pattern:
                if (cell[0] + 1, cell[1]) not in self.pattern:
                    neighbours.append((cell[0] + 1, cell[1]))
            else:
                neighbours.append((cell[0] + 1, cell[1]))
        if cell[1] + 1 < self.height:
            if self.has_pattern:
                if (cell[0], cell[1] + 1) not in self.pattern:
                    neighbours.append((cell[0], cell[1] + 1))
            else:
                neighbours.append((cell[0], cell[1] + 1))
        return neighbours

    def get_connected_neighbours(self, cell: tuple[int, int]) -> list:
        """
        Return neighbouring cells that are directly connected
            (no wall between).

        Args:
            cell (tuple[int, int]): The reference cell.

        Returns:
            list[tuple[int, int]]: List of reachable adjacent cells.
        """

        neighbours = []
        if not self.grid[cell[1]][cell[0]][0]:
            neighbours.append((cell[0], cell[1] - 1))
        if not self.grid[cell[1]][cell[0]][1]:
            neighbours.append((cell[0] + 1, cell[1]))
        if not self.grid[cell[1]][cell[0]][2]:
            neighbours.append((cell[0], cell[1] + 1))
        if not self.grid[cell[1]][cell[0]][3]:
            neighbours.append((cell[0] - 1, cell[1]))
        return neighbours

    def make_imperfect(self):
        """
        Introduce loops into the maze by removing additional walls.

        This transforms a perfect maze into an imperfect one
            by randomly opening extra connections.

        Notes:
            - Ensures a minimum number of additional openings.
            - Avoids over-opening cells with too many connections.
            - Supports animation if enabled.
        """

        minimum_walls = 3
        current_walls = 0
        for row in range(self.height):
            for col in range(self.width):
                # If current cell belongs to 42 pattern, skip this cell
                if self.has_pattern and (col, row) in self.pattern:
                    continue
                current_cell = self.grid[row][col]
                open_walls = len([wall for wall in current_cell if wall == 0])
                # If current cell has more than 2 open walls, skip it
                if open_walls > 2:
                    continue
                # Get all the neighbours and only those who are not connected
                # to the current cell are considered
                neighbours = [cell for cell in self.get_neighbours((col, row)) if cell not in self.get_connected_neighbours((col, row))]
                if len(neighbours) == 0:
                    continue
                neighbour = random.choice(neighbours)
                if current_walls < minimum_walls:
                    self.remove_wall((col, row), neighbour)
                    current_walls += 1
                    if self.animating:
                        self.print_grid()
                        time.sleep(0.05)
                else:
                    # 20% chance of opening the wall between them
                    if random.randint(0, 100) < 20:
                        self.remove_wall((col, row), neighbour)
                        if self.animating:
                            self.print_grid()
                            time.sleep(0.05)

    def toggle_path(self) -> None:
        """
        Toggle visibility of the solution path.
        """

        self.display_path = not self.display_path

    def toggle_color(self) -> None:
        """
        Cycle through available color themes.
        """

        self.current_color += 1
        self.current_color = self.current_color % len(self.colors)

    def toggle_animation(self) -> None:
        """
        Enable or disable animation during maze generation.
        """
        self.animating = not self.animating

    def print_grid(self) -> None:
        """
        Render the maze to the terminal.

        Args:
            None

        Returns:
            None

        This method prints:
            - Walls
            - Entry and exit points
            - Optional solution path
            - Optional "42" pattern

        Notes:
            - Uses ANSI escape codes for coloring.
            - Clears the terminal before rendering.
            - Rendering logic is tightly coupled to grid structure.
        """

        # Clear terminal
        os.system('clear')

        # Although this method seems very confusing the idea is quite simple.
        # Each cell has overlapping walls between them and their neighbours.
        #
        #   W W W    W W W
        #   W   W    W   W
        #   W W W    W W W
        #
        #   W W W    W W W
        #   W   W    W   W
        #   W W W    W W W
        #
        # To avoid repetition, each cells prints
        #   their top left, top, and left wall.
        # The cells in the last column
        #   also print the top right and right wall.
        # The cells in the last row
        #   also print the bottom left and bottom wall.
        #
        # The walls might be closed or open.
        # In case they're open, they might connect cells in the shortest
        #   solved path.
        # A check is needed to change the render in that space
        #
        #   W P W    W W W
        #   W   P    P   W
        #   W W W    W P W
        #
        #   W W W    W P W
        #   W   P    P   W
        #   W P W    W W W
        #
        # Cell render priority:
        # Each cell can be:
        # - Entry
        # - Exit
        # - Path
        # - 42 Pattern
        # - Slot
        #
        # To avoid repeating prints, a simple if/elif/else condition is made:
        # First check if the cell is the maze entry followed by the maze exit
        # Next if it's in the shortest path, followed by the 42 pattern
        # And finally, if none of these are true, print it as a normal cell.

        row = 0
        while row < self.height:
            col = 0
            # Print the top walls
            while col < self.width:
                # Print the top left wall
                print(self.colors[self.current_color]["walls"], end="")

                # In case there's a wall, print it.
                # Otherwise:
                # 1. Check if display path is active and if the cell is
                #   in the path. If so:
                #   1.1. Check wether the cell is in the beginning of the path,
                #       the end or in between.
                #   1.2. If the previous cell, next cell or both cells "row"
                #       coordinate is minus 1 unit.
                #       This means the open wall between the current and
                #           the neighbour cell is part of the path
                if self.grid[row][col][0]:
                    print(self.colors[self.current_color]["walls"], end="")
                else:
                    if self.display_path and (col, row) in self.path:
                        current_index = self.path.index((col, row))
                        # The current cell is the first in the path
                        if current_index == 0:
                            next_cell = self.path[current_index + 1]
                            if next_cell[1] == row - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                # Since the wall is open, even if it isn't
                                # connected to the path, there needs to
                                # be an open space printed, representing the
                                # open wall.
                                print(" ", end="")
                        # The current cell is the last in the path
                        elif current_index == len(self.path) - 1:
                            previous_cell = self.path[current_index - 1]
                            if previous_cell[1] == row - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                # Since the wall is open, even if it isn't
                                # connected to the path, there needs to
                                # be an open space printed, representing the
                                # open wall.
                                print(" ", end="")
                        # The current cell is between entry and exit
                        #   in the path.
                        else:
                            previous_cell = self.path[current_index - 1]
                            next_cell = self.path[current_index + 1]
                            if previous_cell[1] == row - 1 or next_cell[1] == row - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                # Since the wall is open, even if it isn't
                                # connected to the path, there needs to
                                # be an open space printed, representing the
                                # open wall.
                                print(" ", end="")
                    else:
                        # If the wall is open but the current cell
                        #   doesn't belong to the path, print the open wall.
                        print(" ", end="")

                # Reached the final column, needs to print the top right wall.
                if col == self.width - 1:
                    print(self.colors[self.current_color]["walls"])
                col += 1

            col = 0
            while col < self.width:
                # Print the left wall
                if self.grid[row][col][3]:
                    print(self.colors[self.current_color]["walls"], end="")
                else:
                    # Same logic as before, but this time it's applied to
                    # the left wall instead of the upper one.
                    if self.display_path and (col, row) in self.path:
                        current_index = self.path.index((col, row))
                        if current_index == 0:
                            next_cell = self.path[current_index + 1]
                            if next_cell[0] == col - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                print(" ", end="")
                        elif current_index == len(self.path) - 1:
                            previous_cell = self.path[current_index - 1]
                            if previous_cell[0] == col - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                print(" ", end="")
                        else:
                            previous_cell = self.path[current_index - 1]
                            next_cell = self.path[current_index + 1]
                            if previous_cell[0] == col - 1 or next_cell[0] == col - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                print(" ", end="")
                    else:
                        print(" ", end="")

                # Print the slot itself.
                if self.entry[0] == col and self.entry[1] == row:
                    print(self.colors[self.current_color]["entry"], end="")
                elif self.exit[0] == col and self.exit[1] == row:
                    print(self.colors[self.current_color]["exit"], end="")
                elif self.display_path and (col, row) in self.path:
                    print(self.colors[self.current_color]["path"], end="")
                elif self.has_pattern and (col, row) in self.pattern:
                    print(self.colors[self.current_color]["42"], end="")
                else:
                    print(" ", end="")

                # Reached the final column, needs to print the right wall.
                if col == self.width - 1:
                    print(self.colors[self.current_color]["walls"])
                col += 1

            # Reached the final row, needs to print the lower walls.
            if row == self.height - 1:
                col = 0
                while col < 2 * self.width + 1:
                    print(self.colors[self.current_color]["walls"], end="")
                    col += 1
                print()
            row += 1

    def reset(self):
        """
        Reset the maze grid to its initial state (all walls intact).
        """

        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = [1, 1, 1, 1]
