"""
Provides the functionalty to make the lines when given the grid.

The functions that come with this module are:
    - check_validity_grid(grid, num_rows, num_cols): checks if the given grid is valid
    - convert_grid(grid, num_rows, num_cols): converts the given grid into a list of lines
    - convert_to_line(point, type): converts the given point into a line

The assumptions made are:
    - 0: represents nothing
    - 1: represents a square
    - 2: represents a triangle with the upper-right corner empty
    - 3: represents a triangle with the bottom-right corner empty
    - 4: represents a triangle with the upper-left corner empty
    - 5: represents a triangle with the bottom-left corner empty
    - 6: represents a circle

This module does not have any dependencies

"""



def check_validity_grid(grid: list[list[int]], num_rows: int=8, num_cols: int=7) -> bool:
    """
    Checks if the given grid is valid.

    Args:
        - grid (list[list[int]]): A 2D list representing the grid.

    Returns:
        - A boolean indicating whether the grid is valid (i.e. has the correct int of rows and columns).

    Raises:
        - ValueError: If the int of rows in the grid is not equal to the amount of rows or the int of columns in any row is not equal to the amount of columns.
    """

    # our 8x7 grid
    grid_format = (num_rows, num_cols)

    # check if the grid has 8 rows
    if len(grid) != grid_format[0]:      
        ValueError("The provided list does not have the correct amount of rows; it has {} rows, but it should have {} rows!".format(len(grid), grid_format[0]))

    
    # check if every row has 7 columns
    for i, row in enumerate(grid):
        if len(row) != grid_format[1]:
            ValueError("The provided row does not have the correct amount of columns at row {}!".format(i))


    return True

def convert_to_line(point: tuple[int, int], type: int) -> tuple[tuple[tuple[int, int], tuple[int, int]], 
                                                               tuple[tuple[int, int], tuple[int, int]], 
                                                               tuple[tuple[int, int], tuple[int, int]]]:
    """
    Convert the given point into a line.

    Args:
        - point (tuple[int, int]): A tuple representing the point.
        - type (int): The type of object needs to be converted

    Returns:
        - A tuple representing the lines.
    """
    
    # if the object is a square
    if type == 1:
        up_left = (point[0] + 1, point[1])
        up_right = (point[0] + 1, point[1] + 1)
        down_left = (point[0], point[1])
        down_right = (point[0], point[1] + 1)
        return ((up_left, up_right), (up_right, down_right), (down_right, down_left), (down_left, up_left)) # type: ignore (this is a square)
    
    # if the object is a triangle with the upper-right corner empty
    elif type == 2:
        up_left = (point[0] + 1, point[1])
        down_left = (point[0], point[1])
        down_right = (point[0], point[1] + 1)
        return ((up_left, down_right), (down_right, down_left), (down_left, up_left))
    
    # if the object is a triangle with the bottom-right corner empty
    elif type == 3:
        up_left = (point[0] + 1, point[1])
        up_right = (point[0] + 1, point[1] + 1)
        down_left = (point[0], point[1])
        return ((up_left, up_right), (up_right, down_left), (down_left, up_left))

    # if the object is a triangle with the upper-left corner empty
    elif type == 4:
        down_left = (point[0], point[1])
        up_right = (point[0] + 1, point[1] + 1)
        down_right = (point[0] + 1, point[1])
        return ((down_left, up_right), (up_right, down_right), (down_right, down_left))
    
    # if the object is a triangle with the bottom-left corner empty
    elif type == 5:
        up_left = (point[0] + 1, point[1])
        up_right = (point[0] + 1, point[1] + 1)
        down_right = (point[0], point[1] + 1)
        return ((up_left, up_right), (up_right, down_right), (down_right, up_left))
    
    # if the object is a circle
    elif type == 6:
        raise TypeError("Circles aren't supported yet!")
    
    # the object isn't supported
    else:
        raise TypeError("The given type isn't supported!")


def convert_grid(grid: list[list[int]], num_rows: int=8, num_cols: int=7) -> list[tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]: # type: ignore
    """
    Convert the given grid into a list of tuples.

    Args:
        - grid (list[list[int]]): A 2D list representing the grid.

    Returns:
        - A list of tuples representing the grid.

    Raises:
        - ValueError: If the given grid is not valid.
    """

    # check if the given grid is valid
    check_validity_grid(grid=grid, num_rows=num_rows, num_cols=num_cols)
    
    all_lines = []
    for i in range(num_rows):
        for j in range(num_cols):
            if grid[i][j] == 0:
                pass
            else:
                all_lines.append((convert_to_line(point=(i, j), type=grid[i][j]), (i, j))) # (i, j) is the point on the grid

    return all_lines
