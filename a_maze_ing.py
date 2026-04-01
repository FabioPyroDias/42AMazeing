import os
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
            print("5. Set maze properties")
            print("6. Reset maze properties")
            print("7. Get maze properties")
            print("8. Help")
            print("9. Quit")
            choice_str = input("Choice? (1-9): ")
            try:
                choice = int(choice_str)
                if choice < 0 or choice > 9:
                    raise ValueError("Choice invalid. "
                                     "Please choose between 1-9")
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
                    if maze.animating:
                        valid = False
                        while not valid:
                            speed = input("Set Animation Speed (very slow, "
                                          "slow, normal, fast, very fast): ")
                            if speed in ["very slow", "slow", "normal",
                                         "fast", "very fast"]:
                                valid = True
                            if not valid:
                                print("Invalid speed input.\n")
                        maze.set_speed(speed)
                    maze.print_grid()
                elif choice == 5:
                    valid = False
                    while not valid:
                        try:
                            width = int(input("WIDTH (3-30): "))
                            height = int(input("HEIGHT (3-30): "))
                            entry0 = int(input(f"ENTRY x coordinate "
                                               f"(0-{width - 1}):"))
                            entry1 = int(input(f"ENTRY y coordinate "
                                               f"(0-{height - 1}):"))
                            exit0 = int(input(f"EXIT x coordinate "
                                              f"(0-{width - 1}):"))
                            exit1 = int(input(f"EXIT y coordinate "
                                              f"(0-{height - 1}):"))
                            perfect = input("PERFECT (True or False): ")
                            if perfect not in ["True", "False"]:
                                raise ValueError("PERFECT must be either "
                                                 "True or False")
                            algorithm = input("ALGORITHM "
                                              "(Prim, Kruskal, DFS): ")
                            if algorithm not in ["Prim", "Kruskal", "DFS"]:
                                raise ValueError("ALGORITHM must be either "
                                                 "Prim, Kruskal or DFS")
                            properties = {
                                "WIDTH": width,
                                "HEIGHT": height,
                                "ENTRY": (entry0, entry1),
                                "EXIT": (exit0, exit1),
                                "PERFECT": perfect,
                                "ALGORITHM": algorithm
                            }
                            maze.set_properties(properties)
                            valid = True
                        except (TypeError, ValueError) as error:
                            print(error)
                            answer_valid = False
                            while not answer_valid:
                                value = input("Do you wish to continue "
                                              "setting properties? (Y / N): ")
                                if value == "Y":
                                    answer_valid = True
                                elif value == "N":
                                    answer_valid = True
                                    valid = True
                                    maze.print_grid()
                                else:
                                    print("Invalid Answer")
                elif choice == 6:
                    maze.reset_properties()
                elif choice == 7:
                    os.system('clear')
                    print("Properties:")
                    print(maze)
                elif choice == 8:
                    os.system('clear')
                    print("(1) Re-generate a new maze:\n"
                          "Generates a new maze.\n"
                          "If (5) \"Set properties\" were not defined, "
                          "a random seed will be selected and the properties "
                          "will remain the same as the config file.\n")
                    print("(2) Show/Hide path from entry to exit:\n"
                          "Toggles maze solution visibility.\n")
                    print("(3) Rotate maze colors:\n"
                          "Switch between two sets of colors. "
                          "These changes are applied to walls, "
                          "path, entry, exit and, if it's visible, "
                          "42 pattern.\n")
                    print("(4) Toggle animation:\n"
                          "Enables or disables maze generation animation.\n"
                          "If enabled, choose the refresh terminal speed "
                          "for the animation.\n")
                    print("(5) Set maze properties:\n"
                          "Overwrites the maze properties of the "
                          "config file.\n"
                          "These changes are not written to "
                          "the config file.\n")
                    print("(6) Reset maze properties:\n"
                          "Sets the maze properties to the original values "
                          "of the config file.\n")
                    print("(7) Get maze status:\n"
                          "Displays the current maze information.\n")
                    print("(8) Help:\n"
                          "Where you are.\n")
                    print("(9) Quit:\n"
                          "Close the program.\n")
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
