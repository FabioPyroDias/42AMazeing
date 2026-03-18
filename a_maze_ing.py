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
                    raise ValueError("Choice invalid. Please choose between 1-4")
            except ValueError as error:
                print(error)
            if choice == 1:
                pass
            elif choice == 2:
                pass
            elif choice == 3:
                pass
            else:
                sys.exit()
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
    except KeyboardInterrupt as error:
        print(f"KeyboardInterrupt - Exiting program...")
