import sys
from src.parser import read_config_file
from src.maze_generator import MazeGenerator
from src.file_manager import save_file
from src.errors import InvalidParameterError, InvalidConfigurationError
from src.errors import InvalidValueError

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2 or sys.argv[1] != "config.txt":
            raise InvalidParameterError("Error: Expected config.txt file")
        maze_config = read_config_file(sys.argv[1])
        maze = MazeGenerator(maze_config)
        maze.generate()
        save_file(maze)
        while (True):
            print()
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Toggle animation")
            print("5. Quit")
            choice = input("Choice? (1-5): ")
            try:
                choice = int(choice)
                if choice < 1 or choice > 5:
                    raise ValueError("Choice invalid. "
                                     "Please choose between 1-5")
                if choice == 1:
                    maze.regenerate()
                elif choice == 2:
                    maze.toggle_path()
                    maze.print_grid()
                elif choice == 3:
                    maze.toggle_color()
                    maze.print_grid()
                elif choice == 4:
                    maze.toggle_animation()
                    maze.print_grid()
                else:
                    sys.exit()
            except ValueError as error:
                print(f"\n{error}")
    except FileNotFoundError:
        print("File not found")
    except (SyntaxError, TypeError, InvalidParameterError,
            InvalidConfigurationError, InvalidValueError,
            ValueError, AttributeError) as error:
        print(error)
    except (KeyError) as error:
        print(f"ALGORITHM not found {error}")
    except (KeyboardInterrupt, EOFError):
        print()
        print("KeyboardInterrupt - Exiting program...")
