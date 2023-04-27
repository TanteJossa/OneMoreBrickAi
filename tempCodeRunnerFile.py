# TESTING CODE
from time import monotonic_ns
from grid_utils import convert_grid, optimize_grid
import itertools

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

x = 1
t_0 = monotonic_ns()
for i in range(x):
    y = convert_grid(grid, num_rows, num_columns)

t_1 = monotonic_ns()

# print(f'{(t_1-t_0)/x}')

start_point_left = (0, 0)
end_point_left = (0, 8)
end_points_left = [((0, i-1), (0, i)) for i in range(1, end_point_left[1] + 1)]

start_point_right = (7, 0)
end_point_right = (7, 8)
end_points_right = [((7, i-1), (7, i)) for i in range(1, end_point_right[1] + 1)]    

start_point_up = (0, 8)
end_point_up = (7, 8)
end_points_up = [((i-1, 8), (i, 8)) for i in range(1, end_point_up[0] + 1)]

end_points = end_points_left + end_points_right + end_points_up

del end_point_up, end_point_right, end_point_left, start_point_up, start_point_right, start_point_left

print(end_points)

points = [    {'start': (0, 0), 'end': (0, 8), 'end_points': [((0, i-1), (0, i)) for i in range(1, 9)]},
    {'start': (7, 0), 'end': (7, 8), 'end_points': [((7, i-1), (7, i)) for i in range(1, 9)]},
    {'start': (0, 8), 'end': (7, 8), 'end_points': [((i-1, 8), (i, 8)) for i in range(1, 8)]},
]

end_points_1 = list(itertools.chain.from_iterable(item['end_points'] for item in points))
print(end_points_1)
print(end_points==end_points_1)