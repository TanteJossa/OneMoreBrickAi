# TESTING CODE
from time import monotonic_ns
from grid_utils import convert_grid, optimize_grid

# suppose this is the 8x7 grid as a list of lists, in which each inner list represents a row
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

num_rows = len(grid)
num_columns = len(grid[0])


t_0 = monotonic_ns()
for x in range(100000):
    y = convert_grid(grid, num_rows, num_columns)
    optimize_grid(y)

t_1 = monotonic_ns()

print(f'{(t_1-t_0)/100000} nanoseconds per iteration')
# print(optimize_grid(y))
