import sys
from src.parser import read_config_file
from src.maze import Maze
from src.algorithms import prim, kruskal, recursive_backtracking
from src.file_manager import save_file
from src.errors import InvalidParameterError, InvalidConfigurationError
from src.errors import InvalidValueError


ALGORITHMS = {
    "Prim": prim.generate,
    "Kruskal": kruskal.generate,
    "DFS": recursive_backtracking.generate
}


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2 or sys.argv[1] != "config.txt":
            raise InvalidParameterError("Error: Expected config.txt file")
        maze_config = read_config_file(sys.argv[1])
        maze = Maze(maze_config)
        ALGORITHMS[maze_config.algorithm](maze)
        maze.print_grid()
        save_file(maze)
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
