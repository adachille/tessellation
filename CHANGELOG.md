# Changelog

Track the changes that have been made to the project over time.

## Version 0.1 (2024-09-15 - ****-**-**)

### 0.1.1 (2024-09-29) - Refactor to use Point dataclass

- Refactor code to use a `Point` dataclass rather than a tuple of ints
- Fix a minor bug in the `00_rng_tessellation.ipynb` where we were passing in `side_len`
  as an arg to the `generate` method rather than in the class `init` method.

### 0.1.0 (2024-09-15) - Release of 0.1

This release marks the first release of the project in which the tooling is in a
realistically usable state. A user could run the RNGGenerator or GAGenerator and obtain
interesting, if not fairly simple square tessellations.

## Version 0.0 (2024-08-09 - 2024-09-15)

In version 0.0, the project was set up with basic functionality for generating
tessellations.

### 0.0.6 (2024-09-15) - Add pylint

- Add pylint to the project and make updates to address pylint issues

### 0.0.5 (2024-09-02) - Add tests for basic tessellation generation and bug fixes

- Bug fixes
    - Fix a bug where the drawer would not tessellate properly if the number of shapes
      was even.
    - Fix an off-by-1 indexing bug in `generator._draw_line`
    - Fix a bug in `generator._draw_line` where the last point would not be drawn
    - Added minor typing + `__eq__` functions to `TessellationGenome`, and
      `TessellationPhenome`
- Add tests
    - Add tests for basic generation code: `Drawer` , `Generator`, `GenerationResult`,
      `RNGGenerator`
    - Add tests for genetic algorithm code in files: `ga_generator.py`, `genome.py`,
      `heuristic.py`, `mutate.py`, `problem.py`

### 0.0.4 (2024-09-01) - Add functionality to genetic algorithm tesselation generation

- Add `GATessellationGenerator` class to handle genetic algorithm tessellation generation
- Add functionality to `GenerationResult` to be saved to and read from json
- Refactor tessellation generation
    - Move `Generator.tessellate` to be a method in `Drawer` - since it fits better
    - Move `Action` and `GenerationResult` classes out of `generator.py` and into their
      own classes
    - Add `TessellationType` to track what type of tessellation a `GenerationResult`
      holds.
- Updated notebook code to reflect changes in the codebase
- Added tessellation saving/loading functionality to example notebooks

### 0.0.3 (2024-08-28) - Add basic genetic algorithm tessellation generation

- Refactor generation code to have line drawing in generator base class
- Add simple genetic algorithm code for generating tessellation
- Add notebook to demonstrate the genetic algorithm tessellation generation code

### 0.0.2 (2024-08-15) - Add RNG tessellation generation

- Added RNG tessellation generation code and drawing code
- Added notebook to demonstrate the tessellation generation code

### 0.0.1 (2024-08-09) - Initial project setup

- Initial commit / project setup