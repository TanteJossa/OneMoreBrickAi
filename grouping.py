"""
This module provides functions for working with a grid of integers and finding groups of connected values.

The main functions provided by this module are:

    - check_validity_grid(grid): Checks if the given grid is a valid 2D list of integers with 8 rows and 7 columns.
    - find_groups(grid, num_rows, num_cols): Finds all groups of connected values (integers greater than 0) in the given grid.

The find_groups function uses a recursive depth-first search algorithm to traverse the grid and find groups of connected values;
It returns a list of lists of tuples representing the positions of each value in each group.

Example usage:

    grid = [        
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 1, 1]
    ]

    groups = find_groups(grid, 8, 7)
    print(groups)  # prints [[(5, 5), (5, 6), (6, 5), (6, 6), (7, 5), (7, 6)]]


Note: This program assumes that integers greater than 0 should be grouped together.

The module does not require any dependencies to be installed.
"""

# suppose this is the 8x7 grid as a list of lists, in which each inner list represents a row
grid = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 1, 1]
]

num_rows = len(grid)
num_columns = len(grid[0])

def check_validity_grid(grid: list[list[int]]) -> bool:
    """
    Check if the given grid is valid.

    Args:
        - grid: A list of lists containing integers representing a rectangular grid of values.

    Returns:
        - A boolean indicating whether the grid is valid (i.e. has the correct number of rows and columns).

    Raises:
        - ValueError: If the number of rows in the grid is not equal to 8 or the number of columns in any row is not equal to 7.
    """

    # our 8x7 grid
    grid_format = (8, 7)

    # check if the grid has 8 rows
    if len(grid) != grid_format[0]:      
        ValueError("The provided list does not have the correct amount of rows; it has {} rows, but it should have {} rows!".format(len(grid), grid_format[0]))

    
    # check if every row has 7 columns
    for i, row in enumerate(grid):
        if len(row) != grid_format[1]:
            ValueError("The provided row does not have the correct amount of columns at row {}!".format(i))


    return True

def find_groups(grid: list[list[int]], num_rows: int, num_cols: int) -> list[list[tuple[int]]]:
    """
    Finds all groups of connected blocks in the provided grid that have values larger than 0.
    Uses depth-first search (dfs) algorithm to recursively search for connected blocks.
    
    Args:
        grid (list[list[int]]): A 2D list representing the grid to search for connected blocks.
        num_rows (int): The number of rows in the grid.
        num_cols (int): The number of columns in the grid.
    
    Returns:
        list[list[tuple[int]]]: A list of lists, where each inner list represents a group of connected blocks. 
        Each block is represented as a tuple of its row and column indices in the grid.

    Note: If the given grid is not an 8x7 grid it will give an error.
    """

    # check if the given grid is valid
    check_validity_grid(grid=grid)

    # make an empty list to store the groups of 1's, and a set to keep track of visited positions
    groups = []
    visited = set()

    # define our recursive helper function to perform depth-first search (dfs) on the grid
    def dfs(i, j, group) -> None:
        # check if the current position is out of bounds or has already been visited
        if i < 0 or i >= num_rows or j < 0 or j >= num_cols:
            return 
        if grid[i][j] == 0 or (i, j) in visited:
            return 
        
        # mark the current position as visited and add it to the current group
        visited.add((i, j))
        group.append((i, j))

        # recursively call dfs on the neighboring positions
        dfs(i+1, j, group)
        dfs(i-1, j, group)
        dfs(i, j+1, group)
        dfs(i, j-1, group)

    # loop through each position in the grid
    for i in range(num_rows):
        for j in range(num_cols):
            # if the position contains a 1 and has not been visited, find the connected group of 1's using dfs
            if grid[i][j] > 0 and (i, j) not in visited:
                group = []
                dfs(i, j, group)
                groups.append(group)
    # return the list of groups of 1's
    return groups


groups = find_groups(grid=grid, num_rows=num_rows, num_cols=num_columns)
print(groups)