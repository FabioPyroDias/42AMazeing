import random


PATTERN_42 = [
    (-3, -2), (1, -2), (2, -2), (3, -2),
    (-3, -1), (3, -1),
    (-3, 0), (-2, 0), (-1, 0), (1, 0), (2, 0), (3, 0),
    (-1, 1), (1, 1),
    (-1, 2), (1, 2), (2, 2), (3, 2)
]


class Maze():
    def __init__(self, configs: dict) -> None:
        self.width = configs.width
        self.height = configs.height
        self.entry = configs.entry
        self.exit = configs.exit
        self.seed = configs.seed
        self.output = configs.output
        self.grid = [
            [[1, 1, 1, 1] for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.has_pattern = self.width > 10 and self.height > 10
        try:
            if not self.has_pattern:
                raise ValueError
        except ValueError:
            print("The '42' pattern is omitted. Size does not allow it")
        self.pattern = [(x + self.width // 2, y + self.height // 2) for x, y in PATTERN_42]
        if self.has_pattern and (self.entry in self.pattern or self.exit in self.pattern):
            raise ValueError("Value Error: Entry or Exit in 42 Pattern")
        self.display_path = False
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
        self.current_color = 0

    def remove_wall(self, current: tuple, neighbour: tuple) -> None:
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
        minimum_walls = 0
        if self.width <= 5 and self.height <= 5:
            minimum_walls = 3
        elif self.width <= 10 and self.height <= 10:
            minimum_walls = 10
        else:
            minimum_walls = 30
        current_walls = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.has_pattern and (col, row) in self.pattern:
                    continue
                current_cell = self.grid[row][col]
                open_walls = len([wall for wall in current_cell if wall == 0])
                if open_walls > 2:
                    continue
                neighbours = [cell for cell in self.get_neighbours((col, row)) if cell not in self.get_connected_neighbours((col, row))]
                if len(neighbours) == 0:
                    continue
                neighbour = random.choice(neighbours)
                if current_walls < minimum_walls:
                    self.remove_wall
                    current_walls += 1
                else:
                    if random.randint(0, 100) < 20:
                        self.remove_wall((col, row), neighbour)


    def toggle_path(self) -> None:
        self.display_path = not self.display_path

    def set_path(self, path: list) -> None:
        self.path = path

    def toggle_color(self) -> None:
        self.current_color += 1
        self.current_color = self.current_color % len(self.colors)

    def print_grid_og(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                value = (8 * self.grid[row][col][0] +
                         4 * self.grid[row][col][1] +
                         2 * self.grid[row][col][2] +
                         self.grid[row][col][3])
                value = hex(value)[2:]
                print(value, end=" ")
            print()

    def print_grid(self) -> None:
        row = 0
        while row < self.height:
            col = 0
            while col < self.width:
                print(self.colors[self.current_color]["walls"], end="")
                if self.grid[row][col][0]:
                    print(self.colors[self.current_color]["walls"], end="")
                else:
                    if self.display_path and (col, row) in self.path:
                        current_index = self.path.index((col, row))
                        if current_index == 0:
                            next_cell = self.path[current_index + 1]
                            if next_cell[1] == row - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                print(" ", end="")
                        elif current_index == len(self.path) - 1:
                            previous_cell = self.path[current_index - 1]
                            if previous_cell[1] == row - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                print(" ", end="")
                        else:
                            previous_cell = self.path[current_index - 1]
                            next_cell = self.path[current_index + 1]
                            if previous_cell[1] == row - 1 or next_cell[1] == row - 1:
                                print(self.colors[self.current_color]["path"], end="")
                            else:
                                print(" ", end="")
                    else:
                        print(" ", end="")
                if col == self.width - 1:
                    print(self.colors[self.current_color]["walls"])
                col += 1
            col = 0
            while col < self.width:
                if self.grid[row][col][3]:
                    print(self.colors[self.current_color]["walls"], end="")
                else:
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
                if col == self.width - 1:
                    print(self.colors[self.current_color]["walls"])
                col += 1
            if row == self.height - 1:
                col = 0
                while col < 2 * self.width + 1:
                    print(self.colors[self.current_color]["walls"], end="")
                    col += 1
                print()
            row += 1

    def reset(self):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = [1, 1, 1, 1]
