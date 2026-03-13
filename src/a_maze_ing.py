from src.parser import read_config_file
from src.maze import Maze
from src.algorithms import prim, kruskal, recursive_backtracking
from src.errors import InvalidParameterError, InvalidConfigurationError
from src.errors import InvalidValueError


ALGORITHMS = {
    "Prim": prim.generate,
    "Kruskal": kruskal.generate,
    "DFS": recursive_backtracking.generate
}


if __name__ == "__main__":
    try:
        maze_config = read_config_file("config.txt")
        print(maze_config)
        maze = Maze(maze_config)
        ALGORITHMS[maze_config.algorithm](maze)
        maze.print_grid()
    except FileNotFoundError:
        print("File not found")
    except SyntaxError:
        print("TODO: Nao sei o que isto faz")
    except InvalidParameterError as error:
        print(error)
    except InvalidConfigurationError as error:
        print(error)
    except InvalidValueError as error:
        print(error)
    except KeyError as error:
        print(f"ALGORITHM not found {error}")
