import sys
from src.parser import read_config_file
from src.maze import Maze
from src.algorithms import prim, kruskal, recursive_backtracking
from src.file_manager import save_file
from src.errors import InvalidParameterError, InvalidConfigurationError
from src.errors import InvalidValueError
import random
from src.algorithms.breadth_first_search import find_path


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
        path = find_path(maze)
        maze.set_path(path)
        maze.print_grid()
        save_file(maze)
        while (True):
            print()
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            choice = input("Choice? (1-4): ")
            try:
                choice = int(choice)
                if choice < 1 or choice > 4:
                    raise ValueError("Choice invalid. "
                                     "Please choose between 1-4")
                if choice == 1:
                    maze.seed = random.randint(0, 2147483647)
                    maze.reset()
                    ALGORITHMS[maze_config.algorithm](maze)
                    path = find_path(maze)
                    maze.set_path(path)
                    maze.print_grid()
                elif choice == 2:
                    maze.toggle_path()
                    maze.print_grid()
                elif choice == 3:
                    maze.toggle_color()
                    maze.print_grid()
                else:
                    sys.exit()
            except ValueError as error:
                print(error)
    except FileNotFoundError:
        print("File not found")
    except SyntaxError as error:
        print(error)
    except InvalidParameterError as error:
        print(error)
    except InvalidConfigurationError as error:
        print(error)
    except InvalidValueError as error:
        print(error)
    except (KeyError) as error:
        print(f"ALGORITHM not found {error}")
    except (KeyboardInterrupt, EOFError):
        print()
        print("KeyboardInterrupt - Exiting program...")
