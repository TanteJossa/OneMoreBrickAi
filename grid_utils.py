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


def check_validity_grid(grid: list[list[int]]) -> bool:
    """
    Check if the given grid is valid.

    Args:
        - grid (list[list[int]]): A 2D list representing the grid.

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

def find_groups(grid: list[list[int]], num_rows: int=8, num_cols: int=7) -> list[list[tuple[int, int]]]:
    """
    Finds all groups of connected blocks in the provided grid that have values larger than 0.
        Uses depth-first search (dfs) algorithm to recursively search for connected blocks.
    
    Args:
        - grid (list[list[int]]): A 2D list representing the grid to search for connected blocks.
        - num_rows (int)=8: The number of rows in the grid.
        - num_cols (int)=7: The number of columns in the grid.
    
    Returns:
        list[list[tuple[int, int]]]: A list of lists, where each inner list represents a group of connected blocks.
            Each block is represented as a tuple of its row and column indices in the grid.

    Note: If the given grid is not an 8x7 grid it will give an error.
    """

    # check if the given grid is valid
    check_validity_grid(grid=grid)

    # make an empty list to store the groups of 1's, and a set to keep track of visited positions
    groups = []
    visited = set()

    # define our recursive helper function to perform depth-first search (dfs) on the grid
    def dfs(i: int, j: int, group: list) -> None:
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



def convert_block_to_points(block: tuple) -> list[tuple]:
    """
    A helper function to convert a block to the corresponding points.

    Args:
        block (tuple): A tuple in the form of (row, column).

    Returns:
        a list with tuples, in which each tuple represents a point (row, column)
            with the rows from 0-8 (inclusive) and the columns going from 0-7 (inclusive).

    Example usage:
        points = convert_block_to_points((3, 3))
            print(points)  # prints [(3, 3), (3, 4), (4, 3), (4, 4)]
    """

    row, col = block
    points = [(row, col), (row, col+1), (row+1, col), (row+1, col+1)]

    return points


def find_outside_points(groups: list[list[tuple[int, int]]]) -> list[list[tuple[int]]]:
    """
    Takes a list of connected blocks and returns a list of points that are on the outside.

    Args:
        groups (list[list[tuple[int]]]): A list of lists, where each inner list represents a group of connected blocks.
            Each block is represented as a tuple of its row and column indices in the grid.

    Returns:
        list[list[tuple[int]]]: A list of lists, where each inner list represents a group of end points.
            Each outside point is represented as a tuple of its row and column indices in the grid.
                with the rows from 0-8 (inclusive) and the columns going from 0-7 (inclusive).
    """
    new_groups = []

    # take all the blocks and turn them into points 
    for group in groups:
        new_group = []
        for block in group:
            new_group.append(convert_block_to_points(block))
        new_groups.append(new_group)
    
    
    # All the duplicate points are inside points so if you filter them out you have the inside points
    filtered_groups = []
    for group in new_groups:
        
        # make a seen dictionary to keep track of the duplicate points
        seen_dict = {}

        for block in group:
            for point in block:
                if point not in seen_dict:
                    seen_dict[point] = 1
                else:
                    seen_dict[point] += 1
                
        # If there is a duplicate point, that point cannot be in the filtered group
        filtered_group = [tup for tup in seen_dict if seen_dict[tup] == 1]
        filtered_groups.append(filtered_group)

    return filtered_groups



# TESTING CODE
from time import time

# suppose this is the 8x7 grid as a list of lists, in which each inner list represents a row
grid = [
    [2, 3, 0, 0, 1, 3, 0],
    [4, 8, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 8, 0],
    [9, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

num_rows = len(grid)
num_columns = len(grid[0])


t_0 = time()
groups = find_groups(grid=grid, num_rows=num_rows, num_cols=num_columns)

for group in groups:
    print(group)
t_1 = time()
print(t_1-t_0)