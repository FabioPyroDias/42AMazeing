from .maze_generator import MazeGenerator


"""
mazegen - Maze Generator Package

This package provides a reusable MazeGenerator class for creating,
manipulating, and solving mazes.

Key methods:
- generate(): Build the maze with the selected algorithm.
- make_imperfect(): Introduce loops into the maze (optional).
- toggle_path(): Show/hide the solution path.
- toggle_color(): Change the color theme.
- toggle_animation(): Enable/disable generation animation.
"""

"""
mazegen - Maze Generator Package

This package provides a reusable `MazeGenerator` class for creating,
configuring, and solving grid-based mazes.

Basic usage:
    from mazegen import MazeGenerator

    maze = MazeGenerator({
        "WIDTH": 20,
        "HEIGHT": 20,
        "ENTRY": (0, 0),
        "EXIT": (11, 11),
        "ALGORITHM": "Prim",
        "PERFECT": True
    })

    maze.generate()

Configuration parameters:
    WIDTH (int): Maze width (3-30)
    HEIGHT (int): Maze height (3-30)
    ENTRY (tuple[int, int]): Entry cell coordinates
    EXIT (tuple[int, int]): Exit cell coordinates
    ALGORITHM (str): Generation algorithm ("Prim", "Kruskal", "DFS")
    PERFECT (bool): Whether the maze has no loops
    SEED (int): Random seed for reproducibility (optional)

Key features:
    - Multiple generation algorithms:
        * Prim's algorithm
        * Kruskal's algorithm
        * Depth-First Search (recursive backtracking)
    - Shortest path computation (Breadth-First Search)
    - Optional imperfect mazes (loops)
    - Terminal visualization with color themes
    - Animation support

Key methods:
    generate():
        Generate the maze and compute the solution path.

    regenerate():
        Reset and generate a new maze with a new random seed.

    make_imperfect():
        Introduce loops into the maze.

    toggle_path():
        Show or hide the solution path in the display.

    toggle_color():
        Cycle through available color themes.

    toggle_animation():
        Enable or disable animation.

    set_properties(properties: dict):
        Update maze configuration and regenerate it.

Accessing results:
    maze.grid:
        Internal representation of the maze structure.

    maze.path:
        List of (x, y) coordinates representing the shortest path
        from entry to exit.
"""

__all__ = ["MazeGenerator"]
