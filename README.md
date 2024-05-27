## Crossword Puzzle Solver

This project is an implementation of a Constraint Satisfaction Problem (CSP) solver for crossword puzzles using backtracking search and constraint propagation techniques. The solver can generate solutions for crossword puzzles given the structure and a word list.

## Motivation

Solving crossword puzzles can be a challenging task, especially for larger puzzles with complex constraints. The motivation behind this project is to explore the application of Artificial Intelligence techniques, specifically CSP solvers, to efficiently solve crossword puzzles. By leveraging backtracking search and constraint propagation algorithms, the solver can find solutions that satisfy all the constraints imposed by the crossword structure and word list.

## Quick Start

1. Clone the repository and navigate to the correct directory:
```txt
git clone https://github.com/your-username/crossword-solver.git
cd crossword-solver
```
2. Install the required dependency (Pillow):
```txt
pip install Pillow
```
3. Run the solver with the provided structure and word files:
```txt
python generate.py data/structure.txt data/words.txt output.png
```

This command will attempt to solve the crossword puzzle defined by `data/structure.txt` and `data/words.txt`, and save the solution as `output.png`.

## Usage

The solver is implemented in the `CrosswordCreator` class, which takes a `Crossword` object as input. The `Crossword` class represents the structure and word list of the crossword puzzle.

To use the solver, follow these steps:

1. Create a `Crossword` object by providing the paths to the structure and word files:

```python
crossword = Crossword("data/structure.txt", "data/words.txt")
```
2. Create a CrosswordCreator instance with the Crossword object:
```python
creator = CrosswordCreator(crossword)
```
3. Solve the crossword puzzle by calling the solve method on the CrosswordCreator instance:
```python
assignment = creator.solve()
```
4. If a solution is found, you can print it or save it as an image file:
```python
if assignment is not None:
    creator.print(assignment)
    creator.save(assignment, "output.png")
else:
    print("No solution found.")
```

