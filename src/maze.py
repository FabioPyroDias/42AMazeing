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

    def get_neighbours(self, cell: tuple[int, int]) -> list[int]:
        neighbours = []
        if cell[0] - 1 >= 0:
            neighbours.append((cell[0] - 1, cell[1]))
        if cell[1] - 1 >= 0:
            neighbours.append((cell[0], cell[1] - 1))
        if cell[0] + 1 < self.width:
            neighbours.append((cell[0] + 1, cell[1]))
        if cell[1] + 1 < self.height:
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
                print(u'\u2588', end="")
                if self.grid[row][col][0]:
                    print(u'\u2588', end="")
                else:
                    print(" ", end="")
                if col == self.width - 1:
                    print(u'\u2588')
                col += 1
            col = 0
            while col < self.width:
                if self.grid[row][col][3]:
                    print(u'\u2588', end="")
                else:
                    print(" ", end="")

                if self.entry[0] == col and self.entry[1] == row:
                    print("\033[37;45m \033[0m", end="")
                elif self.exit[0] == col and self.exit[1] == row:
                    print("\033[31;41m \033[0m", end="")
                else:
                    print(" ", end="")
                if col == self.width - 1:
                    print(u'\u2588')
                col += 1
            if row == self.height - 1:
                col = 0
                while col < 2 * self.width + 1:
                    print(u'\u2588', end="")
                    col += 1
                print()
            row += 1

    def reset(self):
        for row in range(self.height):
            for col in range(self.width):
                self.grid[row][col] = [1, 1, 1, 1]
