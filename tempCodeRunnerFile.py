# TESTING CODE
from time import time
from grid_utils import find_groups, convert_block_to_points, find_outside_points

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
groups = find_groups(grid=grid, num_rows=num_rows, num_cols=num_columns) # type: ignore
new_groups = []
for group in groups:
        new_group = []
        for block in group:
            new_group.append(convert_block_to_points(block))
        new_groups.append(new_group)


out_points = find_outside_points(groups=groups)

for i, group in enumerate(new_groups):
    print(f"Group {i}: {group}")
    print(f"Outside points: {out_points[i]}")
t_1 = time()
print(t_1-t_0)

# [(0, 4), (1, 4), (0, 6), (2, 5), (2, 6)]
# [(0, 4), (1, 4), (1, 5), (0, 6), (2, 5), (2, 6)]