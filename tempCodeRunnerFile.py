# TESTING CODE
from time import monotonic_ns
from grid_utils import get_engine_lines, convert_grid

# suppose this is the 7x8 grid as a list of lists, in which each inner list represents a row
grid = [
    [1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0]
]

num_rows = len(grid)
num_columns = len(grid[0])

# CODE TO TEST PREFORMANCE
t_0 = monotonic_ns()
for x in range(100000):
    convert_grid(grid)

t_1 = monotonic_ns()

print(f'{(t_1-t_0)/100000} nanoseconds per iteration')
# print(get_engine_lines(grid))