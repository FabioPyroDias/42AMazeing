# mazegen

## Description

Reusable maze generator module.

It supports multiple generation algorithms (Prim, Kruskal, DFS), optional imperfections, pathfinding, and animated rendering.

## Installation

```bash
pip install ./mazegen-*.whl
# or
pip install ./mazegen-*.tar.gz
```

## Basic usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator({
    "WIDTH": 20,
    "HEIGHT": 20,
    "ENTRY": (0, 0),
    "EXIT": (19, 19),
    "ALGORITHM": "Prim",
    "PERFECT": True,
    "SEED": 42
})

maze.generate()
```

## Key methods

- generate():
    Generate the maze and compute the solution path.
- regenerate():
    Reset and generate a new maze with a new random seed.
- make_imperfect():
    Introduce loops into the maze.
- toggle_path():
    Show or hide the solution path in the display.
- toggle_color():
    Cycle through available color themes.
- toggle_animation():
    Enable or disable animation.
- set_properties(properties: dict):
    Update maze configuration and regenerate it.


## Algorithms
| Algorithm | Usage | Description |
| --------- | ----- | ----------- |
| Prim | Maze Generation | Randomized Prim's algorithm builds the maze by expanding from a starting cell using a frontier of walls. |
| Kruskal | Maze Generation | Treats the maze as a graph and removes walls while avoiding cycles using disjoint sets. |
| Depth First Search (DFS) | Maze Generation | Recursive backtracking that explores as far as possible before backtracking. |
| Breadth First Search (BFS) | Path Finding | Finds the shortest path from entry to exit. |
