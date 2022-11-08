import random
import pandas as pd

def RandomGrid():
    df = pd.read_csv('D:\MS Robotics\Foundations of AI CS5100\Project\Sudoku\sudoku.csv')
    num = random.randint(2, 1000000)
    rand_grid = df.iloc[num, 0]

    numbers = []
    numbers[:] = rand_grid
    full_grid = [int(x) for x in numbers]
    grid = list()
    grid_size = 9
    for i in range(0, len(numbers), grid_size):
        grid.append(full_grid[i:i + grid_size])

    return grid


