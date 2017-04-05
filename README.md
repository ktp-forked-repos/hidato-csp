# Hidato CSP

An analysis and exploration of forming the logic puzzle Hidato as an instance of a Constraint Satisfaction Problem.

## Table of Contents

- [View the Puzzle Bank](#view-the-puzzle-bank)
- [Solve arbitrary puzzles](#solve-arbitrary-puzzles)
- [Compare Propagators](#compare-propagators)
- [Compare Heuristics](#compare-heuristics)

## View the Puzzle Bank

All the puzzles are borrowed from the website [Puzzles and Brains](http://www.puzzlesandbrains.com/Hidatomain.php). They are all stored in the file `puzzle_bank.py`. The puzzles are separated into `a_level`, `b_level`, `c_level`, `d_level` and `e_level` puzzles, with `a_level` being the easiest puzzles, and `e_level` being the hardest. Each category has 8 6x6 puzzles, for example the 4th puzzle in `c_level` is named `c4` and is a 6x6 hidato puzzle. The only exception is `e_level` which only has a single very hard 7x7 puzzle.

Each puzzle is represented by a list of lists, or in other words: a 2-dimensional array. For example, here is `b3`:

```python
b3 = [
  [3, None, 1, 9, None, 11],
  [6, None, None, None, 10, 13],
  [None, None, 18, 34, None, None],
  [None, 27, 33, 19, 35, None],
  [29, 32, 26, None, 23, 36],
  [31, None, 25, None, None, 22]
]
```

## Solve Arbitrary Puzzles

We have provided the file `run.py` to allow you to solve an arbitrary puzzle from the `puzzle_bank`. For example, if you would like to solve board `c6`, enter the following command

`python3 run.py c6`

If you would like to solve multiple puzzles back-to-back, simply list the boards you want to solve.

`python3 run.py a1 a3 b1 b2 b7 c1 a8`

To note, `run.py` uses our Forward Checking Propagator and the Smallest Current Domain Heuristic.

## Compare Propagators

We have written three different propagators that we could potentially use to solve our CSP. This leads to the question: which propagator is better?

In our [report](./report.md) we provide an analysis of Backtracking, Forward Checking and Generalized Arc Consistency. This analysis uses graphs that were created from running different propagators against our `puzzle_bank`. If you would like to reproduce our results, run the command:

`python3 generate_propagator_comparison.py`

Before you do, be warned that it will take about half an hour to finish (board e1 alone takes 12 minutes). Also note that we only allow Backtracking to run on `a_level` and `b_level` boards because we don't want to have to wait for days. We use trend lines to estimate how Backtracking would perform on more difficult boards.

## Compare Heuristics

Another interesting part in our CSP is how we select which variable to assign next. We do this using a heuristic. However there are a couple different options for heuristics, which again leads to the question: which heuristic is best?

We have three potential heuristics for Hidato. Smallest Current Domain, Next In Line and Random. Smallest Current Domain selects the variable with the least amount of potential locations it can be placed. Next In Line always selects the variable with the lowest value not yet assigned. Random selects a random variable.

This idea is explored in our [report](./report.md), and again relies on data created by running our CSP with different heuristics on our `puzzle_bank`. To reproduce our results, run the command:

`python3 generate_heuristic_comparison.py`

Again, be warned that this also will take a decent amount of time to complete.
