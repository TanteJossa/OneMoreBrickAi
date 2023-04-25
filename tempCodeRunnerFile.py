# TESTING CODE
from time import time
from grid_utils import convert_grid

# suppose this is the 8x7 grid as a list of lists, in which each inner list represents a row
grid = [
    [1, 2, 3, 4, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

num_rows = len(grid)
num_columns = len(grid[0])


t_0 = time()
x = convert_grid(grid, num_rows, num_columns)
for group in x:
    for g in group:
        for line in g:
            print(line)
t_1 = time()
print(t_1-t_0)

print(x)