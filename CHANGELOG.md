# Changelog

Track the changes that have been made to the project over time.

## Version 0.0 (2024-08-09 - ****-**-**)

### 0.0.4 (2024-09-01)

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

### 0.0.3 (2024-08-28)

- Refactor generation code to have line drawing in generator base class
- Add simple genetic algorithm code for generating tessellation
- Add notebook to demonstrate the genetic algorithm tessellation generation code

### 0.0.2 (2024-08-15)

- Added RNG tessellation generation code and drawing code
- Added notebook to demonstrate the tessellation generation code

### 0.0.1 (2024-08-09)

- Initial commit / project setup