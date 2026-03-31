*This project has been created as part of the 42 curriculum by fda-cruz, jreis-de*

## Description

A-Maze-ing consists of generating and solving a maze using graph algorithms.

A maze is represented by a grid of cells, where each cell has walls that are removed to create paths.

The maze is generated from a configuration file, which defines its dimensions, entry and exit points, and other constraints.

The program ensures that:
- A centered "42" pattern is enforced when possible
- Entry and exit exist, are valid, and are distinct.
- The maze is valid (at least one path exists between entry and exit)

Once generated, the maze is exported to a file using a hexadecimal wall representation.

The project also includes visualization features such as terminal rendering.

## Requirements

Make sure `make` is installed on your system:

```bash
sudo apt install make
```

Python 3.10 or higher is required. Check your version with:

```bash
python3 --version
```

A virtual environment (amazeing) will be created automatically during installation. This ensures project dependencies are isolated.

## Instructions

### Instalation
To install project dependencies, simply run `make install` in the terminal.
This will:
- Create a virtual environment amazeing
- Install required Python packages (flake8, mypy, etc.)

### Execution
Run the program with `make run`.
A menu will appear with a set of actions:
1. Re-generate maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Toggle animation
5. Quit.

Choose one of these options (1-5) and press `Enter`.

## Technical Overview

### Configuration File
The program requires a configuration file to generate the maze.
It must contain one `KEY=VALUE` pair per line.
Lines starting with `#` are commented and ignored.

| Key | Description | Type | Example |
|:-----|:--------:|------:|:----:|
| WIDTH | Maze width (number of cells) | **int** | 20 |
| HEIGHT | Maze height | **int** | 15 |
| ENTRY | Entry coordinates (x, y) | **(int, int)** | 0, 0 |
| EXIT | Exit coordinates (x, y) | **(int, int)** | 19, 14 |
| OUTPUT_FILE | Output filename | **str** | maze_txt |
| PERFECT | Is the maze perfect? | **bolean** | True |

Optional keys (can be used for reproducibility):

| Key | Description | Type | Example |
|:-----|:--------:|------:|:----:|
| SEED | Random seed to allow reproducibility | **int** | 42 |
| ALGORITHM | Maze generation algorithm to use | **Prim / Kruskal / DFS** | Prim |

A default configuration file `config_file.txt` is included in the repository.

### Maze Requirements
Each cell has between 0 and 4 walls (N, E, S, W).
The maze must be valid:
- Entry and exit exist, are different, and within maze bounds.
- Full connectivity: no isolated cells (except the "42" pattern).
- External borders must be walled.
- Neighboring cells must have coherent walls (if one has a wall, the adjacent cell must reflect it).

Corridors cannot exceed 2 cells in width or height, large open areas are forbidden.

A visible "42" pattern must exist if the maze size allows it. If not, an error is printed.

If PERFECT=True, the maze must have exactly one path between entry and exit.

Random generation must be reproducible via the SEED key.

### Maze Generation Algorithms
In this project, three maze generation algorithms are available:

- Prim
- Kruskal
- Depth First Search (DFS)

### Prim
Starting from an initial cell, adds its walls to a list.

While there are walls in that list:
- Select a random wall
- If the wall divides visited and unvisited cells:
  - Remove the wall
  - Mark the new cell as visited
  - Add its walls to the list

### Kruskal
Each cell starts as an independent set, meaning no cells are connected.

All walls between adjacent cells are listed and shuffled randomly.

For each wall:
- Check the two cells separated by the wall
- If they belong to different sets:
  - Remove the wall
  - Merge the two sets into one

This ensures that no cycles are created during generation, producing a perfect maze.
The algorithm continues until all cells belong to a single connected set.

### Depth First Search (DFS)
Starting from the initial cell, randomly visits a neighbouring cell on the vertical or horizontal axis and removes the wall between them.
This neighbour becomes the new current cell and the process continues recursively.
When a cell has no unvisited neighbours, the algorithm backtracks to the previous cell.

### Algorithm Choice
Depth-First Search (DFS) was chosen as the primary algorithm due to its simplicity and efficiency in generating perfect mazes.

Prim and Kruskal were also implemented as alternative strategies to explore different maze structures and compare algorithmic approaches.

### Imperfect Maze
To introduce loops, additional walls are removed using a controlled strategy:

- Only cells with limited open walls are considered
- A minimum number of walls are removed
- Additional openings are added randomly

### Pathfinding Algorithm
The maze is solved using a fourth algorithm, Breadth First Search (BFS).

A list is used as a queue, to explore the maze level by level.
Each visited cell stores its parent and once the exit is reached, the path is reconstructed from exit to entry.

This guarantees the shortest path.

### Output File Format
The maze is written to the output file using one hexadecimal digit per cell, encoding which walls are closed:

| Bit | Direction |
|------:|:----:|
|0 | North |
|1 | East |
|2 | South |
|3 | West |

Closed walls are represented by 1 while open walls are represented by 0.
Cells are stored row by row, one row per line.
After an empty line, three lines are appended:
1. Entry coordinates
2. Exit coordinates
3. Shortest path from entry to exit using letters N, E, S, W.

All lines must end with a newline `\n`.

### Reusability

### Project Management

## Resources