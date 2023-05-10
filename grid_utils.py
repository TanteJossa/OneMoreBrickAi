"""
Provides the functionalty to make the lines when given the grid.

The functions that come with this module are:
    - check_validity_grid(grid, num_rows, num_cols): checks if the given grid is valid
    - convert_grid(grid, num_rows, num_cols): converts the given grid into a list of lines
    - convert_to_line(point, type): converts the given point into a line
    - optimize_grid(converted_grid): optimizes the given grid by removing unnecessary lines

The assumptions made are:
    - 0: represents nothing
    - 1: represents a square
    - 2: represents a triangle with the upper-right corner empty
    - 3: represents a triangle with the bottom-right corner empty
    - 4: represents a triangle with the upper-left corner empty
    - 5: represents a triangle with the bottom-left corner empty
    - 6: represents a circle

This module requires itertools from std::lib

"""


import itertools


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
                                                               tuple[tuple[int, int], tuple[int, int]]]: # type: ignore
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
        up_left = (point[0], 7 - point[1] + 1)
        up_right = (point[0] + 1, 7 - point[1] + 1)
        down_left = (point[0], 7 - point[1])
        down_right = (point[0] + 1, 7 - point[1])
        return ((up_left, up_right), (up_right, down_right), (down_right, down_left), (down_left, up_left)) # type: ignore (this is a square)
    
    # if the object is a triangle with the upper-right corner empty
    elif type == 2:
        up_left = (point[0], 7 - point[1] + 1)
        down_left = (point[0], 7 - point[1])
        down_right = (point[0] + 1, 7 - point[1])
        return ((up_left, down_right), (down_right, down_left), (down_left, up_left))
    
    # if the object is a triangle with the bottom-right corner empty
    elif type == 3:
        up_left = (point[0], 7 - point[1] + 1)
        up_right = (point[0] + 1, 7 - point[1] + 1)
        down_left = (point[0], 7 - point[1])
        return ((up_left, up_right), (up_right, down_left), (down_left, up_left))

    # if the object is a triangle with the upper-left corner empty
    elif type == 4:
        up_right = (point[0] + 1, 7 - point[1] + 1)
        down_left = (point[0], 7 - point[1])
        down_right = (point[0] + 1, 7 - point[1])
        return ((down_left, up_right), (up_right, down_right), (down_right, down_left))
    
    # if the object is a triangle with the bottom-left corner empty
    elif type == 5:
        up_left = (point[0], 7 - point[1] + 1)
        up_right = (point[0] + 1, 7 - point[1] + 1)
        down_right = (point[0] + 1, 7 - point[1])
        return ((up_left, up_right), (up_right, down_right), (down_right, up_left))
    
    # if the object is a circle
    # elif type == 6:
    #     raise TypeError("Circles aren't supported yet!")
    
    # the object isn't recognized
    # else:
    #     raise TypeError("The given type isn't recognized!")


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
            if grid[i][j] <= 0 or grid[i][j] == 6:
                pass
            else:
                all_lines.append(((j, 8 - i), convert_to_line(point=(j, i), type=grid[i][j]))) # (j, i) is the point on the grid (x, y)

    return all_lines


def optimize_grid(converted_grid: list[tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]) -> list[tuple[tuple[int, int],    # type: ignore
                                                                                                                tuple[int, int]],
                                                                                                                tuple[int, int]]:   # type: ignore
    """
    Optimize the given grid.

    Args:
        - converted_grid (list[tuple[tuple[int, int], tuple[int, int]], tuple[int, int]]): A list of tuples representing the lines on the grid.

    Returns:
        - A list of tuples representing the grid.

    Example:
        1.  There is a duplicate line in the grid:

            # suppose this is the 7x8 grid as a list of lists, in which each inner list represents a row
            grid = [
                [1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ]
            
            The lines received from the function are:
            (((0, 8), (1, 8)), ((1, 8), (1, 7)), ((1, 7), (0, 7)), ((0, 7), (0, 8)))
            (((1, 8), (2, 8)), ((2, 8), (2, 7)), ((2, 7), (1, 7)), ((1, 7), (1, 8)))

            Now the following lines are the same so them both would be a waste of resources, we only return one ((1, 8), (1, 7)), ((1, 7), (1, 8))
            (((0, 8), (1, 8)), ((1, 8), (1, 7)), ((1, 7), (0, 7)), ((0, 7), (0, 8)))
            (((1, 8), (2, 8)), ((2, 8), (2, 7)), ((2, 7), (1, 7)))
            
        
        2.  A line spans multiple points
            
            # suppose we have the same grid as above
            
            The lines received from the function are (when partially optimized):
            (((0, 8), (1, 8)), ((1, 8), (1, 7)), ((1, 7), (0, 7)), ((0, 7), (0, 8)))
            (((1, 8), (2, 8)), ((2, 8), (2, 7)), ((2, 7), (1, 7)))

            Now ((0, 8), (1, 8)) and ((1, 8), (2, 8)), so we remove one and expend the other
            (((0, 8), (2, 8)), ((1, 8), (1, 7)), ((1, 7), (0, 7)), ((0, 7), (0, 8)))
            (((2, 8), (2, 7)), ((2, 7), (1, 7)))

        3. A line is at the end of the grid
            
            # suppose we have the same grid as above
            
            The lines received from the function are (when partially optimized):
            (((0, 8), (2, 8)), ((1, 8), (1, 7)), ((1, 7), (0, 7)), ((0, 7), (0, 8)))
            (((2, 8), (2, 7)), ((2, 7), (1, 7)))

            Now ((0, 8), (2, 8)), ((0, 7), (0, 8)) are at the end of the grid, so we remove them
            (((0, 8), (2, 8)), ((1, 8), (1, 7)), ((1, 7), (0, 7)), ((0, 7), (0, 8)))
            (((2, 8), (2, 7)), ((2, 7), (1, 7)))

    """
    

    # makes a list using dictionary and list comprehensions of all the outer lines on the grid
    points = [    {'start': (0, 0), 'end': (0, 8), 'end_points': [((0, i-1), (0, i)) for i in range(1, 9)]},
    {'start': (7, 0), 'end': (7, 8), 'end_points': [((7, i-1), (7, i)) for i in range(1, 9)]},
    # {'start': (0, 8), 'end': (7, 8), 'end_points': [((i-1, 8), (i, 8)) for i in range(1, 8)]},
    ]

    # just trust me
    end_points = list(itertools.chain.from_iterable(item['end_points'] for item in points)) 
    converted_grid_optimized_1 = []
    unique_lines = set()

    # iterate over each object in the input list
    for obj in converted_grid:
        # extract the coordinates tuple and add it to the filtered object list
        filtered_obj = {'point':  obj[0], 'lines': []}
        
        filtered_lines = []
        
        # iterate over each line tuple in the object
        for line in obj[1]:
            # (line[1], line[0]), because these are the same: ((1, 8), (1, 7)), ((1, 7), (1, 8))
            if line not in unique_lines and (line[1], line[0]) not in unique_lines and line not in end_points and (line[1], line[0]) not in end_points: # type: ignore
                # if not, add it to the unique set and the filtered object list
                unique_lines.add(line)
                filtered_lines.append(line) # type: ignore

                
        filtered_obj['lines'] = filtered_lines # type: ignore
        # add the filtered object to the filtered list
        converted_grid_optimized_1.append(filtered_obj)

        

    # TODO: if a line spans multiple points, then remove the it
    # seen = converted_grid_optimized_1
    # # suppose we have these two lines:
    # for line in converted_grid_optimized_1:
    #     seen.append(line)
    # seen_2 = converted_grid_optimized_1
    # print(seen)
    # print(seen_2)
    # ((0, 8), ((0, 8), (1, 8)), ((1, 8), (1, 7)), ((1, 7), (0, 7)))
    # ((1, 8), ((1, 8), (2, 8)), ((2, 8), (2, 7)), ((2, 7), (1, 7)))
    

    return converted_grid_optimized_1


def get_lines(grid):
    y = convert_grid(grid)
    return optimize_grid(y)
