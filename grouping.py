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
    # our 8x7 grid
    grid_format = (8, 7)

    # check if the grid has 8 rows
    if len(grid) != grid_format[0]:      
        ValueError("The provided list does not have the correct amount of rows!")

        return False
    
    # check if every row has 7 columns
    for i, row in enumerate(grid):
        if len(row) != grid_format[1]:
            ValueError("The provided row does not have the correct amount of columns at row {}!", i)

            return False

    return True

def find_groups(grid: list[list[int]], num_rows: int, num_cols: int) -> list[list[tuple[int]]]:
     # check if the given grid is valid
    if not check_validity_grid(grid=grid):
        ValueError("The given grid is invalid!")

    # make an empty list to store the groups of 1's, and a set to keep track of visited positions
    groups = []
    visited = set()

    # define our recursive helper function to perform depth-first search (dfs) on the grid
    def dfs(i, j, group) -> None:
        # check if the current position is out of bounds or has already been visited
        if i < 0 or i >= num_rows or j < 0 or j >= num_cols:
            return None
        if grid[i][j] == 0 or (i, j) in visited:
            return None
        
        # mark the current position as visited and add it to the current group
        visited.add((i, j))
        group.append((i, j))

        # recursively call dfs on the neighboring positions
        dfs(i+1, j, group)
        dfs(i-1, j, group)
        dfs(i, j+1, group)
        dfs(i, j-1, group)

        return None

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


def get_lines() -> list[list[int]]:

    return None  # type: ignore


groups = find_groups(grid=grid, num_rows=num_rows, num_cols=num_columns)
print(groups)