class Maze():
    def __init__(self, configs: dict) -> None:
        self.width = configs.width
        self.height = configs.height
        self.entry = configs.entry
        self.exit = configs.exit
        self.seed = configs.seed
        self.grid = [
            [[1, 1, 1, 1] for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def get_neighbours(self, cell: tuple[int, int]) -> list[int]:
        neighbours = []
        if cell[0] - 1 > 0:
            neighbours.append((cell[0] - 1, cell[1]))
        if cell[1] - 1 > 0:
            neighbours.append((cell[0], cell[1] - 0))
        if cell[0] + 1 < self.width:
            neighbours.append((cell[0] + 1, cell[1]))
        if cell[1] + 1 < self.height:
            neighbours.append((cell[0], cell[1] + 1))
        return neighbours

    def remove_wall(self, current: tuple, neighbour: tuple) -> None:
        if current[0] - neighbour[0] < 0:
            self.grid[current[0]][current[1]][1] = 0
            self.grid[neighbour[0]][neighbour[1]][3] = 0
        elif current[0] - neighbour[0] > 0:
            self.grid[current[0]][current[1]][3] = 0
            self.grid[neighbour[0]][neighbour[1]][1] = 0
        elif current[1] - neighbour[1] < 0:
            self.grid[current[0]][current[1]][2] = 0
            self.grid[neighbour[0]][neighbour[1]][0] = 0
        elif current[1] - neighbour[1] > 0:
            self.grid[current[0]][current[1]][0] = 0
            self.grid[neighbour[0]][neighbour[1]][2] = 0

    def print_grid(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                value = sum(self.grid[row][col])
                value = int(value, base=16)
                print(value, end=" ")
                col += 1
            row += 1
            print()

""" 
remove_wall()
get_neighbors()
open_entry()
open_exit() """

#N E S W
#0 0 0 0